from heterogeneous_system_integrator.repository.base import BaseRepository


class BaseService:
    REPOSITORY_CLASS: BaseRepository = None
