from . import postgres
from . import dummy

SUPPORTED_DATABASES = {
    "Postgre": postgres.Postgres,
    "Dummy": dummy.DummyDB
}
