import threading
import time
import schedule

notify = True


def notify_users():
    """TODO: notify all users every hour"""


def notify_users_job():
    schedule.every().hour.do(notify_users)
    while notify:
        schedule.run_pending()
        time.sleep(1)


notify_job = threading.Thread(target=notify_users_job)


def stop_notifying():
    global notify, notify_job
    notify = False
    notify_job.join()
    print("Notify job: stopped")


def start_notifying():
    global notify, notify_job
    notify = True
    notify_job.start()
    print("Notify job: started")
