from flask_apscheduler import APScheduler

scheduler = APScheduler()

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()