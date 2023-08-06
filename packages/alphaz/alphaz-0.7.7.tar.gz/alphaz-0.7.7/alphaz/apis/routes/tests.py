# MODULES
import sqlalchemy


# CORE
from core import core

# MODELS
from ...models.database.users_definitions import Application
from ...models.tests import Levels

# UTILS
from ...utils.api import route, Parameter

# LIBS
from ...libs import test_lib, io_lib


API = core.api


@route(
    "/tests",
    parameters=[
        Parameter("category", ptype=str),
        Parameter("categories", ptype=list),
        Parameter("group", ptype=str),
        Parameter("groups", ptype=list),
        Parameter("name", ptype=str),
        Parameter("names", ptype=list),
        Parameter("run", ptype=bool),
        Parameter("file_path", ptype=str),
        Parameter("coverage", ptype=str),
        Parameter("load_from_db", ptype=bool),
        Parameter("stop", ptype=bool),
        Parameter("report", ptype=str),
        Parameter("coverage", ptype=str),
        Parameter("levels", ptype=list[Levels], default=[]),
    ],
)
def get_tests():
    return test_lib.get_tests_auto(**API.gets())


@route("/tests/coverage", parameters=[Parameter("file", required=True)])
def get_coverage_file():
    coverages = io_lib.unarchive_object(API["file"])
    return coverages


def test_null(update_date=None):
    return core.db.select(
        Application, optional_filters=[Application.update_date == update_date]
    )


@route(
    "test_null",
    parameters=[
        Parameter(
            "update_date",
            required=False,
            none_value=sqlalchemy.null(),
        )
    ],
)
def test():
    return test_null(**API.get_parameters())
