"""Test openapi routes."""

import inspect
import logging
import re

import openapi_core
import tornado
from openapi_core.templating.paths.finders import APICallPathFinder

from mqs import server
from mqs.config import OPENAPI_SPEC

LOGGER = logging.getLogger(__name__)

logging.getLogger("parse").setLevel(logging.INFO)


def test_census_routes() -> None:
    """Check that all the routes have openapi schemas."""
    missing: list[tuple[str, str]] = []

    # match named groups: (?P<task_id>\w+)
    regular_id = rf"{re.escape(r'(?P<')}([^>]+){re.escape(r'>\w+)')}"

    # match named groups: (?P<task_id>[\w-]+)
    withdashes_id = rf"{re.escape(r'(?P<')}([^>]+){re.escape(r'>[\w-]+)')}"

    for handler in server.HANDLERS:
        route = (
            re.sub(
                rf"{regular_id}|{withdashes_id}",
                r"{\1}",  # replace w/ braces: {task_id}
                getattr(handler, "ROUTE"),
            )
            .rstrip("$")  # strip end
            .replace("\\", "")  # un-escape special chars
        )
        LOGGER.info(f"Checking route: {route}")

        implemented_rest_methods = [
            name
            # vars() only gets attrs defined explicitly by child class
            for name, attr in vars(handler).items()
            if inspect.isfunction(attr)
            and name.upper() in tornado.web.RequestHandler.SUPPORTED_METHODS
        ]
        for method in implemented_rest_methods:
            LOGGER.info(f"-> method: {method}")

            try:  # except error so we can see what all is missing w/o multiple test runs
                APICallPathFinder(OPENAPI_SPEC.spec, base_url=None).find(
                    method,
                    route,
                )
            except openapi_core.templating.paths.exceptions.PathNotFound:
                missing.append((route, method))
                LOGGER.info("----> not found")
            else:
                LOGGER.info("----> found")

    # log at end so these are easy to find
    for missed in missing:
        LOGGER.critical(f"not found in openapi schema: {missed}")
    assert not missing
