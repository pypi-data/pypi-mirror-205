from typing import Optional, Union
from .plotfish import *

api_key: Optional[str] = None
riverbed_url: str = "http://localhost:8000"  # TODO: make this the prod instance

rod = None

Number = Union[int, float]


def _proxy(method, *args, **kwargs):
    global rod
    if not rod:
        rod = FishingRod(riverbed_url, api_key)
    fn = getattr(rod, method)
    return fn(*args, **kwargs)


def line(plot_name: str, value: Number) -> None:
    _proxy("line", plot_name, value)


def counter(plot_name: str, change: Number) -> None:
    _proxy("counter", plot_name, change)


def increment(plot_name: str) -> None:
    _proxy("counter", plot_name, 1)


def progress_bar(plot_name: str, value: Number, total: Number) -> None:
    _proxy("progress_bar", plot_name, value, total)
