"""Tests for querying about queues."""

import json
import os
import pathlib

import openapi_core
from jsonschema_path import SchemaPath
from rest_tools.client import RestClient, utils


async def query_for_schema(rc: RestClient) -> openapi_core.OpenAPI:
    """Grab the openapi schema from the rest server and check that it matches the json file."""
    resp = await rc.request("GET", "/schema/openapi")
    with open(
        pathlib.Path("../../wms") / os.environ["REST_OPENAPI_SPEC_FPATH"], "rb"
    ) as f:
        assert json.load(f) == resp
    openapi_spec = openapi_core.OpenAPI(SchemaPath.from_dict(resp))

    return openapi_spec


async def test_000(rc: RestClient) -> None:
    """Test normal initial workflow."""
    openapi_spec = await query_for_schema(rc)

    # get queues
    criteria = dict(priority=99, n_queues=5)
    resp = await utils.request_and_validate(
        rc, openapi_spec, "POST", "/mq-group", dict(criteria=criteria)
    )
    mqgroup = resp["mqgroup"]
    assert mqgroup["criteria"] == criteria
    mqprofiles = resp["mqprofiles"]
    assert len(mqprofiles) == criteria["n_queues"]

    # check GET
    resp = await utils.request_and_validate(
        rc, openapi_spec, "GET", f"/mq-group/{mqgroup['mqgroup_id']}"
    )
    assert resp == mqgroup
    # check GET
    for mqprofile in mqprofiles:
        resp = await utils.request_and_validate(
            rc, openapi_spec, "GET", f"/mq/{mqprofile['mqid']}"
        )
        assert resp == mqprofile
