import sys

if sys.version_info < (3, 8):
    from typing_extensions import Literal
    from typing_extensions import Protocol
else:
    from typing import Literal
    from typing import Protocol


if sys.version_info < (3, 10):
    from typing_extensions import TypeGuard
else:
    from typing import TypeGuard

__all__ = ["Literal", "Protocol", "TypeGuard"]
