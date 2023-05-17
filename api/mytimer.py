from datetime import datetime
import time

class MyTimer():
    def __init__(self):
        self.timestarted = None
        self.timepaused = None
        self.paused = False

    def start(self):
        self.timestarted = datetime.now()

    def pause(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            raise ValueError("Timer is already paused")
        self.timepaused = datetime.now()
        self.paused = True

    def resume(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if not self.paused:
            raise ValueError("Timer is not paused")
        pausetime = datetime.now() - self.timepaused
        self.timestarted = self.timestarted + pausetime
        self.paused = False

    def get(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            return self.timepaused - self.timestarted
        else:
            return datetime.now() - self.timestarted

    def stop(self):
        if self.timestarted is None:
            raise ValueError("Timer not started")
        elapsed_time = datetime.now() - self.timestarted
        print(f"Elapsed time: {elapsed_time}")
        self.timestarted = None

if __name__ == "__main__":
    t = MyTimer()
    while True:
        command = input("Enter command (start/stop): ")
        if command == "start":
            t.start()
            print("Timer started")
        elif command == "stop":
            t.stop()
            print("Timer stopped")
