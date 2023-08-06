# -*- coding: utf-8 -*-
"""Data classes."""
from typing import Any, Dict, Optional

from pydantic import BaseModel


class JSONRPCRequest(BaseModel):
    """JSON RPC request."""

    method: str
    parameters: Dict[str, Any]
    id: Optional[int] = None
