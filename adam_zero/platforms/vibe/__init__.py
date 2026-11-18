"""Vibe coding platform handlers."""

from adam_zero.platforms.vibe.bolt import BoltHandler
from adam_zero.platforms.vibe.lovable import LovableHandler
from adam_zero.platforms.vibe.replit import ReplitHandler
from adam_zero.platforms.vibe.v0 import V0Handler

REGISTRY: dict[str, type] = {
    "bolt": BoltHandler,
    "lovable": LovableHandler,
    "replit": ReplitHandler,
    "v0": V0Handler,
}

__all__ = ["BoltHandler", "LovableHandler", "ReplitHandler", "V0Handler", "REGISTRY"]
