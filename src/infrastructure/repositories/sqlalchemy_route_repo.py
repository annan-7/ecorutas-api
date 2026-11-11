from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.route import Route
from src.domain.exceptions.domain_exceptions import DuplicateRouteError
from src.domain.repositories.i_route_repository import IRouteRepository
from src.domain.value_objects.coordinates import Coordinates
from src.domain.value_objects.difficulty import Difficulty, DifficultyLevel
from src.domain.value_objects.route_type import RouteTypeVO
from src.infrastructure.database.models.route_model import RouteModel


class SQLAlchemyRouteRepository(IRouteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, route: Route) -> Route:
        model = self._to_model(route)
        self._session.add(model)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateRouteError(f"Ya existe la ruta '{route.name}'") from exc
        await self._session.refresh(model)
        return self._to_entity(model)

    async def save_many(self, routes: list[Route]) -> list[Route]:
        models = [self._to_model(route) for route in routes]
        self._session.add_all(models)
        try:
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateRouteError("Una o más rutas ya existen") from exc
        return [self._to_entity(model) for model in models]

    async def find_by_id(self, route_id: UUID) -> Route | None:
        model = await self._session.get(RouteModel, route_id)
        return self._to_entity(model) if model else None

    async def find_all(
        self,
        skip: int,
        limit: int,
        difficulty: DifficultyLevel | None = None,
        location: str | None = None,
    ) -> list[Route]:
        statement = select(RouteModel).where(RouteModel.is_active.is_(True))
        if difficulty:
            statement = statement.where(RouteModel.difficulty == difficulty.value)
        if location:
            statement = statement.where(RouteModel.location.ilike(f"%{location}%"))
        statement = statement.order_by(RouteModel.name).offset(skip).limit(limit)
        result = await self._session.execute(statement)
        return [self._to_entity(model) for model in result.scalars().all()]

    async def count(
        self,
        difficulty: DifficultyLevel | None = None,
        location: str | None = None,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(RouteModel)
            .where(RouteModel.is_active.is_(True))
        )
        if difficulty:
            statement = statement.where(RouteModel.difficulty == difficulty.value)
        if location:
            statement = statement.where(RouteModel.location.ilike(f"%{location}%"))
        return int((await self._session.execute(statement)).scalar_one())

    async def search_by_name(self, term: str) -> list[Route]:
        statement = select(RouteModel).where(
            RouteModel.name.ilike(f"%{term.strip()}%"),
            RouteModel.is_active.is_(True),
        )
        result = await self._session.execute(statement.order_by(RouteModel.name))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def delete(self, route_id: UUID) -> bool:
        model = await self._session.get(RouteModel, route_id)
        if model is None:
            return False
        await self._session.delete(model)
        await self._session.commit()
        return True

    @staticmethod
    def _to_model(route: Route) -> RouteModel:
        return RouteModel(
            id=route.id,
            name=route.name,
            description=route.description,
            interesting_fact=route.interesting_fact,
            image_url=route.image_url,
            location=route.location,
            distance_km=route.distance_km,
            difficulty=route.difficulty.level.value,
            route_type=route.route_type.value.value,
            duration_hours=route.duration_hours,
            latitude=route.coordinates.latitude if route.coordinates else None,
            longitude=route.coordinates.longitude if route.coordinates else None,
            altitude_meters=route.altitude_meters,
            is_active=route.is_active,
            created_at=route.created_at,
            updated_at=route.updated_at,
        )

    @staticmethod
    def _to_entity(model: RouteModel) -> Route:
        coordinates = None
        if model.latitude is not None and model.longitude is not None:
            coordinates = Coordinates(model.latitude, model.longitude)
        return Route(
            id=model.id,
            name=model.name,
            description=model.description,
            interesting_fact=model.interesting_fact,
            image_url=model.image_url,
            location=model.location,
            distance_km=model.distance_km,
            difficulty=Difficulty.from_string(model.difficulty),
            route_type=RouteTypeVO.from_string(model.route_type),
            duration_hours=model.duration_hours,
            coordinates=coordinates,
            altitude_meters=model.altitude_meters,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
