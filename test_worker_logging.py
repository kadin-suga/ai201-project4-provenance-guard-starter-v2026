"""Unit tests for worker attempt-level structured logging."""

import unittest
from unittest.mock import patch

import database
import worker


class WorkerLoggingTests(unittest.TestCase):
    def setUp(self):
        self.job = {
            "job_id": "00000000-0000-0000-0000-000000000001",
            "creator_id": "logging-test",
            "input_text": "Enough ordinary text exists here for a worker logging test.",
            "attempts": 1,
        }

    @patch("worker.audit.log_run")
    @patch("worker.database.complete_job")
    @patch("worker.scoring.score_to_label", return_value=("human", "test label"))
    @patch("worker.scoring.combine_signals", return_value=0.3)
    @patch("worker.stylometry.style_signal", return_value=0.4)
    @patch("worker.detector.model_signal", return_value=0.2)
    def test_success_logs_named_input_output_and_duration(
        self, _model, _style, _combine, _label, complete, log_run
    ):
        complete.return_value = {"status": "completed"}

        self.assertTrue(worker.process_job(self.job, worker_id="test-worker"))

        logged = log_run.call_args.kwargs
        self.assertEqual(logged["input_text"], self.job["input_text"])
        self.assertEqual(logged["output"]["status"], "completed")
        self.assertGreaterEqual(logged["duration_ms"], 0)

    @patch("worker.audit.log_run")
    @patch("worker.database.complete_job")
    @patch("worker.scoring.score_to_label", return_value=("human", "test label"))
    @patch("worker.scoring.combine_signals", return_value=0.3)
    @patch("worker.stylometry.style_signal", return_value=0.4)
    @patch("worker.detector.model_signal", return_value=0.2)
    def test_stale_result_is_logged(
        self, _model, _style, _combine, _label, complete, log_run
    ):
        complete.side_effect = database.JobStateConflict("lease expired")

        self.assertFalse(worker.process_job(self.job, worker_id="stale-worker"))

        logged = log_run.call_args.kwargs
        self.assertEqual(logged["output"]["status"], "stale")
        self.assertIn("lease expired", logged["output"]["error"])


if __name__ == "__main__":
    unittest.main()
