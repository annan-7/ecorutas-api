from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RouteCreated:
    route_id: UUID
    occurred_at: datetime
