"""Minimal imghdr compatibility for Python 3.14 removal.
Provides a simple `what()` function used by libraries to detect image type.
This is not a full implementation but recognizes common formats: jpeg, png, gif, webp.
"""
from typing import Optional

def _match(header: bytes, sig: bytes) -> bool:
    return header.startswith(sig)

def what(filename: Optional[str]=None, h: Optional[bytes]=None) -> Optional[str]:
    data = h
    if filename and h is None:
        try:
            with open(filename, 'rb') as f:
                data = f.read(32)
        except Exception:
            return None
    if not data:
        return None
    if _match(data, b"\xff\xd8\xff"):
        return 'jpeg'
    if _match(data, b"\x89PNG\r\n\x1a\n"):
        return 'png'
    if _match(data, b"GIF87a") or _match(data, b"GIF89a"):
        return 'gif'
    if _match(data, b"RIFF") and b"WEBP" in data[:16]:
        return 'webp'
    return None
