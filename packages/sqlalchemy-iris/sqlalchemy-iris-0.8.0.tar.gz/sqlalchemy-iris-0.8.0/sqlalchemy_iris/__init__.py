from sqlalchemy.dialects import registry as _registry

from . import base
from . import iris

from .base import BIGINT
from .base import BIT
from .base import DATE
from .base import DOUBLE
from .base import INTEGER
from .base import LONGVARBINARY
from .base import LONGVARCHAR
from .base import NUMERIC
from .base import SMALLINT
from .base import TIME
from .base import TIMESTAMP
from .base import TINYINT
from .base import VARBINARY
from .base import VARCHAR

base.dialect = dialect = iris.dialect

_registry.register("iris.iris", "sqlalchemy_iris.iris", "IRISDialect_iris")
_registry.register("iris.emb", "sqlalchemy_iris.embedded", "IRISDialect_emb")

__all__ = [
    "BIGINT",
    "BIT",
    "DATE",
    "DOUBLE",
    "INTEGER",
    "LONGVARBINARY",
    "LONGVARCHAR",
    "NUMERIC",
    "SMALLINT",
    "TIME",
    "TIMESTAMP",
    "TINYINT",
    "VARBINARY",
    "VARCHAR",
    "dialect",
]
