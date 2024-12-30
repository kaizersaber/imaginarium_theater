import time


class DualTimer:

    def __init__(self):
        self.reset()

    def end(self):
        self.elapsed_perf = time.perf_counter() - self.start_perf
        self.elapsed_proc = time.process_time() - self.start_proc
        self.elapsed_wait = self.elapsed_perf - self.elapsed_proc
        print("Season information written to seasons.csv")
        print(
            f"Wait time: {self.elapsed_wait:.2f} seconds\n"
            + f"Process time: {self.elapsed_proc:.2f} seconds\n"
            + f"Total time: {self.elapsed_perf:.2f} seconds"
        )

    def reset(self):
        self.start_perf = time.perf_counter()
        self.start_proc = time.process_time()
        self.elapsed_perf = None
        self.elapsed_proc = None
        self.elapsed_wait = None
