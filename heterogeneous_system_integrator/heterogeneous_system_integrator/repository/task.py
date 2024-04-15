from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask, PeriodicTask
from heterogeneous_system_integrator.repository.base import BaseRepository


class AsyncTaskRepository(BaseRepository):
    MODEL_CLASS = AsyncTask


class PlannedTaskRepository(BaseRepository):
    MODEL_CLASS = PlannedTask


class PeriodicTaskRepository(BaseRepository):
    MODEL_CLASS = PeriodicTask
