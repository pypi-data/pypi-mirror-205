from dask.distributed import Client
from dask_fly.worker import FlyDaskWorker


class FlyDaskClient(Client):
    def __init__(self, app_name, cluster, *args, **kwargs):
        self.app_name = app_name
        self.cluster = cluster
        # We need to initialize the Client instance first
        super().__init__("", *args, **kwargs)
        self.loop.run_until_complete(cluster.ensure_scheduler())
        self.set_as_default()
        self.scheduler_address = cluster.scheduler_address  # Update the scheduler address

    async def add_worker(self, region, name=None, memory=None, cpu=None):
        worker = FlyDaskWorker(self.app_name, region, name, memory, cpu)
        await worker.create()
        self.cluster.workers.append(worker)

    async def remove_worker(self, worker):
        await worker.delete()
        self.cluster.workers.remove(worker)
