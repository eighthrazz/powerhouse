import schedule
import threading
import time

class Scheduler():
    func = None
    repeat_sec = None
    scheduler_running = None

    def __init__(self, func, repeat_sec):
        self.func = func
        self.repeat_sec = repeat_sec
        self.scheduler_running = False

    def __scheduler_thread(self):
        while 1:
            schedule.run_pending()
            time.sleep(1)

    def __run_threaded(self, job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    def start(self):
        if self.scheduler_running == False:
            self.__run_threaded(self.__scheduler_thread)
            self.scheduler_running = True
        schedule.every(self.repeat_sec).seconds.do(self.func).tag("tag")

    def stop(self):
        schedule.clear("tag")