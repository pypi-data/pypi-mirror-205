from datetime import datetime, timedelta
from . import scheduler
from .executer import ExecuterCaller

class ScheduledJob:

    def __init__(self, jobs: list) -> None:

        for job in jobs:
            self._run_job(job)

    def _run_job(self, job: dict) -> int:

        executer = job.pop('executer')
        scheduler.add_job(
            func=ExecuterCaller.instance().execute_command,
            args=[{'executer':executer}],
            **job
        )        
        return 1