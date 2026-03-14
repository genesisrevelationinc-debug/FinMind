import unittest
from backend.app import create_app
from apscheduler.schedulers.background import BackgroundScheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.scheduler = BackgroundScheduler()

    def test_job_registration(self):
        with self.app.app_context():
            self.scheduler.add_job(id='test_job', func=lambda: print("Test job running"), trigger='interval', minutes=1)
            self.assertIn('test_job', self.scheduler.get_jobs())

if __name__ == '__main__':
    unittest.main()