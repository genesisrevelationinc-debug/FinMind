import unittest
from app.extensions import scheduler
from app import create_app

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_scheduler_running(self):
        self.assertTrue(scheduler.running)
        self.assertEqual(len(scheduler.get_jobs()), 1)