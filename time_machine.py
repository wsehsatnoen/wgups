import datetime, time
import threading

class TimeMachine:

    def __init__(self):
        self.time_simulation = datetime.time(hour=7, minute=30)
        self.increment = datetime.timedelta(minutes=1)
        self.simulation_thread = threading.Thread(target=self.simulation)
        self.running = True

    def simulation(self):
        while self.running:
            print(f"\r Current Time: {self.time_simulation}", flush=True, end="")
            time.sleep(2)
            new_time = (datetime.datetime.combine(datetime.date.today(), self.time_simulation) + datetime.timedelta(minutes=1)).time()
            self.time_simulation = new_time

    def run(self):
        self.simulation_thread.start()

    def stop(self):
        self.running = False

    def add_thirty(self):
        print("\nAdding 30 minutes...")
        new_time = (datetime.datetime.combine(datetime.date.today(), self.time_simulation) + datetime.timedelta(minutes=30)).time()
        self.time_simulation = new_time

    def get_simulation_time(self):
        return self.time_simulation


time_machine = TimeMachine()
print("Simulation Starting: \nPress enter to add 30 minutes:")
time_machine.run()

