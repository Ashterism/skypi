from pathlib import Path
from typing import Any
import json
from datetime import datetime, timedelta


"""scaffolding done - will return to this if needed / when all complete"""

class AstroCache:
    """Simple file-based cache for astro session data."""

    def __init__(self, cache_file: str = "data/cache/astro_sessions.json", ttl_minutes: int = 15):
        self.cache_file = Path(cache_file)
        self.ttl_minutes = ttl_minutes

    def cache_exists(self) -> bool:
        return self.cache_file.exists()

    def is_fresh(self) -> bool:
        """Return True if cache file exists and is still within TTL."""
        if not self.cache_exists():
            return False

        cache_data = self.load_raw()
        generated_at = cache_data.get("generated_at")
        if not generated_at:
            return False

        generated_dt = datetime.fromisoformat(generated_at)
        age = datetime.now() - generated_dt
        return age < timedelta(minutes=self.ttl_minutes)

    def load_raw(self) -> dict[str, Any]:
        """Load raw JSON cache data from disk."""
        with self.cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_raw(self, payload: dict[str, Any]) -> None:
        """Save raw JSON cache data to disk."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with self.cache_file.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
