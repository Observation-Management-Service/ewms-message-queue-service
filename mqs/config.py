"""Config settings."""

import dataclasses as dc
import json
import logging
from pathlib import Path
from typing import Any

import jsonschema
import openapi_core
from jsonschema_path import SchemaPath
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename
from wipac_dev_tools import from_environment_as_dataclass, logging_tools

LOGGER = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------


@dc.dataclass(frozen=True)
class EnvConfig:
    """Environment variables."""

    HERE_URL: str

    # mongo address
    MONGODB_HOST: str  # "localhost"
    MONGODB_PORT: int  # 27017

    # here address
    REST_HOST: str  # "localhost"
    REST_PORT: int  # 8080

    # broker info
    BROKER_URL: str
    BROKER_TYPE: str
    # TODO: add BROKER_MGMT_URL

    # broker/mq auth
    # -> keys (by file)
    BROKER_QUEUE_AUTH_PUBLIC_KEY_FILE: Path
    BROKER_QUEUE_AUTH_PRIVATE_KEY_FILE: Path
    # -> meta
    BROKER_QUEUE_USERNAME: str = "user"
    BROKER_QUEUE_AUTH_TOKEN_EXP: int = 60 * 60 * 24
    BROKER_RESOURCE_SERVER_ID: str = ""
    BROKER_RESOURCE_SERVER_TYPE: str = ""

    # rest auth
    AUTH_AUDIENCE: str = ""
    AUTH_OPENID_URL: str = ""

    # mongo auth
    MONGODB_AUTH_PASS: str = ""  # empty means no authentication required
    MONGODB_AUTH_USER: str = ""  # None means required to specify

    # misc
    CI: bool = False  # github actions sets this to 'true'
    LOG_LEVEL: str = "DEBUG"
    LOG_LEVEL_THIRD_PARTY: str = "INFO"
    LOG_LEVEL_REST_TOOLS: str = "DEBUG"

    # backlog
    SKIP_BACKLOG_MIN_PRIORITY: int = 10
    BACKLOG_RUNNER_SHORT_DELAY: int = 15
    BACKLOG_RUNNER_DELAY: int = 5 * 60

    # schema
    DB_JSONSCHEMA_DIR: str = "schema/db"
    REST_OPENAPI_SPEC_FPATH: str = "schema/rest/openapi_spec.json"


ENV = from_environment_as_dataclass(EnvConfig)


# --------------------------------------------------------------------------------------


def _get_jsonschema_specs(dpath: Path) -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for fpath in dpath.iterdir():
        with open(fpath) as f:
            specs[fpath.stem] = json.load(f)  # validates keys
        LOGGER.info(f"validating JSON-schema spec for {fpath}")
        jsonschema.protocols.Validator.check_schema(specs[fpath.stem])
    return specs


# keyed by the mongo collection name
MONGO_COLLECTION_JSONSCHEMA_SPECS = _get_jsonschema_specs(
    Path(__file__).parent / ENV.DB_JSONSCHEMA_DIR
)


# --------------------------------------------------------------------------------------


def _get_openapi_spec(fpath: Path) -> openapi_core.OpenAPI:
    spec_dict, base_uri = read_from_filename(str(fpath))
    LOGGER.info(f"validating OpenAPI spec for {base_uri} ({fpath})")
    validate(spec_dict)  # no exception -> spec is valid
    return openapi_core.OpenAPI(SchemaPath.from_file_path(str(fpath)))


REST_OPENAPI_SPEC: openapi_core.OpenAPI = _get_openapi_spec(
    Path(__file__).parent / ENV.REST_OPENAPI_SPEC_FPATH
)
ROUTE_VERSION_PREFIX = (  # ex: v0
    "v" + REST_OPENAPI_SPEC.spec.contents()["info"]["version"].split(".", maxsplit=1)[0]
)


# --------------------------------------------------------------------------------------


# known cluster locations
KNOWN_CLUSTERS: dict[str, dict[str, str]] = {
    "sub-2": {
        "collector": "glidein-cm.icecube.wisc.edu",
        "schedd": "sub-2.icecube.wisc.edu",
    },
}
if ENV.CI:  # just for testing -- can remove when we have 2+ clusters
    KNOWN_CLUSTERS.update(
        {
            "test-alpha": {
                "collector": "COLLECTOR1",
                "schedd": "SCHEDD1",
            },
            "test-beta": {
                "collector": "COLLECTOR2",
                "schedd": "SCHEDD2",
            },
        }
    )


# --------------------------------------------------------------------------------------


def config_logging() -> None:
    """Configure the logging level and format.

    This is separated into a function for consistency between app and
    testing environments.
    """
    hand = logging.StreamHandler()
    hand.setFormatter(
        logging.Formatter(
            "%(asctime)s.%(msecs)03d [%(levelname)8s] %(name)s[%(process)d] %(message)s <%(filename)s:%(lineno)s/%(funcName)s()>",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logging.getLogger().addHandler(hand)
    logging_tools.set_level(
        ENV.LOG_LEVEL,  # type: ignore[arg-type]
        first_party_loggers=[__name__.split(".", maxsplit=1)[0]],
        third_party_level=ENV.LOG_LEVEL_THIRD_PARTY,  # type: ignore[arg-type]
        future_third_parties=[],
        specialty_loggers={
            "wipac-telemetry": "WARNING",
            "parse": "WARNING",  # from openapi
            "rest_tools": ENV.LOG_LEVEL_REST_TOOLS,  # type: ignore
        },
    )
