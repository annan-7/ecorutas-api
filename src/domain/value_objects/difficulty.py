from dataclasses import dataclass
from enum import StrEnum

from src.domain.exceptions.domain_exceptions import InvalidRouteError


class DifficultyLevel(StrEnum):
    FACIL = "facil"
    MODERADA = "moderada"
    DIFICIL = "dificil"
    EXPERTO = "experto"


@dataclass(frozen=True, slots=True)
class Difficulty:
    level: DifficultyLevel

    @classmethod
    def from_string(cls, value: str) -> "Difficulty":
        try:
            return cls(DifficultyLevel(value.lower()))
        except ValueError as exc:
            raise InvalidRouteError(f"Dificultad inválida: {value}") from exc

    @property
    def numeric_value(self) -> int:
        return {
            DifficultyLevel.FACIL: 1,
            DifficultyLevel.MODERADA: 2,
            DifficultyLevel.DIFICIL: 3,
            DifficultyLevel.EXPERTO: 4,
        }[self.level]
