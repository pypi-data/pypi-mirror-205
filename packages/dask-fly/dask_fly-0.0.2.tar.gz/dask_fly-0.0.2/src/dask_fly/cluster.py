import asyncio
from distributed.deploy.cluster import Cluster
from dask_fly.scheduler import FlyDaskScheduler


class FlyDaskCluster(Cluster):
    def __init__(self, app_name, scheduler_region, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_name = app_name
        self.scheduler = FlyDaskScheduler(app_name, scheduler_region)
        self.scheduler.create()
        self.workers = []

    def __del__(self):
        for worker in self.workers:
            worker.delete()
        self.scheduler.delete()

    async def ensure_scheduler(self):
        while self.scheduler_address is None or self.scheduler_address == "<Not Connected>":
            await asyncio.sleep(1)
