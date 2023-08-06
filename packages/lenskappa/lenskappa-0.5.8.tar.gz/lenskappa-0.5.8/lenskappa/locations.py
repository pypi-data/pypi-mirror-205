import lenskappa
from pathlib import Path

package_root = Path(lenskappa.__file__).parents[0]
LENSKAPPA_CONFIG_LOCATION = package_root / "config"

__all__ = ["LENSKAPPA_CONFIG_LOCATION"]
