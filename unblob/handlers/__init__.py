from typing import List, Dict
from ..models import Handler
from .archive import zip, tar, gzip, rar


def _make_handler_map(*handlers: Handler) -> Dict[str, Handler]:
    return {h.NAME: h for h in handlers}


_ALL_MODULES_BY_PRIORITY: List[Dict[str, Handler]] = [
    _make_handler_map(zip),
]