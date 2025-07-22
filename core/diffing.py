from lib.primitives import Renderable
from typing import Dict
import zlib


class DiffEngine:

    def __init__(self):
        self.cache: Dict[str, int] = {}
        return

    def _to_bytes(self, renderable: Renderable) -> bytes:
        return repr(renderable).encode("utf-8")

    def _compute_crc32_checksum(self, data: bytes) -> int:
        return zlib.crc32(data)

    def diff(self, renderable: Renderable) -> bool:
        hashed: int = self._compute_crc32_checksum(self._to_bytes(renderable))
        if not renderable.id in self.cache:
            self.cache[renderable.id] = hashed
            return False
        is_diff = not (hashed == self.cache.get(renderable.id))
        self.cache[renderable.id] = hashed
        return is_diff
