import os
from typing import Any


def _get_float(name: str, default: float) -> float:
    val = os.getenv(name, "")
    try:
        return float(val) if val != "" else float(default)
    except ValueError:
        return float(default)


def _coerce_number(value: Any) -> Any:
    if isinstance(value, str) and value.strip() != "":
        try:
            f = float(value)
            return int(f) if f.is_integer() else f
        except ValueError:
            return value
    return value


def apply_profit_default(incoming: dict[str, Any] | None) -> dict[str, Any]:
    data: dict[str, Any] = {} if incoming is None else dict(incoming)
    if "profit_margin" not in data or data["profit_margin"] in (None, ""):
        data["profit_margin"] = _get_float("APP_DEFAULT_PROFIT_MARGIN", 20.0)
    else:
        data["profit_margin"] = _coerce_number(data["profit_margin"])
    return data
