from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.route import Route
from src.domain.value_objects.difficulty import DifficultyLevel


class IRouteRepository(ABC):
    @abstractmethod
    async def save(self, route: Route) -> Route: ...

    @abstractmethod
    async def save_many(self, routes: list[Route]) -> list[Route]: ...

    @abstractmethod
    async def find_by_id(self, route_id: UUID) -> Route | None: ...

    @abstractmethod
    async def find_all(
        self,
        skip: int,
        limit: int,
        difficulty: DifficultyLevel | None = None,
        location: str | None = None,
    ) -> list[Route]: ...

    @abstractmethod
    async def count(
        self,
        difficulty: DifficultyLevel | None = None,
        location: str | None = None,
    ) -> int: ...

    @abstractmethod
    async def search_by_name(self, term: str) -> list[Route]: ...

    @abstractmethod
    async def delete(self, route_id: UUID) -> bool: ...
