import asyncio
from datetime import datetime

class Periodic:

    def __init__(self, period_sec=0.025, semi_period_percent=50):
        self.period_sec = period_sec
        self.semi_period_percent = semi_period_percent
        self.semi_period_sec = period_sec * semi_period_percent / 100.0
        self.last_time = None

    async def wait_for_period_boundary(self):
        if not self.last_time:
            self.last_time = datetime.timestamp(datetime.now())
            return self.last_time
        while True:
            if self.last_time + self.period_sec < datetime.timestamp(datetime.now()):
                self.last_time = datetime.timestamp(datetime.now())
                return self.last_time

    async def wait_for_semi_period_boundary(self):
        if not self.last_time:
            self.last_time = datetime.timestamp(datetime.now())
            return
        while True:
            if self.last_time + self.semi_period_sec < datetime.timestamp(datetime.now()):
                return

if __name__ == '__main__':
    periodic  = Periodic()
    async def test():
        last_period_boundary = 0
        # last_period_boundary = datetime.timestamp(datetime.now())
        for i in range(10):
            period_boundary = await periodic.wait_for_period_boundary()
            print("{:0.6f}".format(period_boundary - last_period_boundary))
            await periodic.wait_for_semi_period_boundary()
            print("{:0.6f}".format(datetime.timestamp(datetime.now()) - period_boundary))
            last_period_boundary = period_boundary

    asyncio.run(test())


