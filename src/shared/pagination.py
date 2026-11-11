from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pagination:
    skip: int = 0
    limit: int = 20

    def __post_init__(self) -> None:
        if self.skip < 0:
            raise ValueError("skip no puede ser negativo")
        if not 1 <= self.limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100")
