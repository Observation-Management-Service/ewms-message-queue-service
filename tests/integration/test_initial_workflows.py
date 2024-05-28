"""Tests for querying about queues."""

import json
import os
import re

import openapi_core
import pytest
import requests
from jsonschema_path import SchemaPath
from rest_tools.client import RestClient, utils

ROUTE_VERSION_PREFIX = "v0"


async def query_for_schema(rc: RestClient) -> openapi_core.OpenAPI:
    """Grab the openapi schema from the rest server and check that it matches the json file."""
    resp = await rc.request("GET", f"/{ROUTE_VERSION_PREFIX}/schema/openapi")
    with open(
        f'{os.environ["GITHUB_WORKSPACE"]}/mqs/{os.environ["REST_OPENAPI_SPEC_FPATH"]}',
        "rb",
    ) as f:
        assert json.load(f) == resp
    openapi_spec = openapi_core.OpenAPI(SchemaPath.from_dict(resp))

    return openapi_spec


async def test_000(rc: RestClient) -> None:
    """Test normal initial workflow."""
    openapi_spec = await query_for_schema(rc)

    # get queues
    criteria = {"priority": 99, "n_queues": 5}
    resp = await utils.request_and_validate(
        rc,
        openapi_spec,
        "POST",
        f"/{ROUTE_VERSION_PREFIX}/mq-group",
        {"task_id": "a123", "criteria": criteria},
    )
    mqgroup = resp["mqgroup"]
    assert mqgroup["criteria"] == criteria
    mqprofiles = resp["mqprofiles"]
    assert len(mqprofiles) == criteria["n_queues"]

    # check GET
    resp = await utils.request_and_validate(
        rc,
        openapi_spec,
        "GET",
        f"/{ROUTE_VERSION_PREFIX}/mq-group/{mqgroup['mqgroup_id']}",
    )
    assert resp == mqgroup
    # check GET
    for mqprofile in mqprofiles:
        resp = await utils.request_and_validate(
            rc,
            openapi_spec,
            "GET",
            f"/{ROUTE_VERSION_PREFIX}/mq/{mqprofile['mqid']}",
        )
        assert resp == mqprofile


async def test_100__get_mqgroup__error_404(rc: RestClient) -> None:
    """Test erroneous calls--logical errors (type-checking done by openapi)."""
    openapi_spec = await query_for_schema(rc)

    mqgroup_id = "foobarbaz"
    with pytest.raises(
        requests.HTTPError,
        match=re.escape(
            f"MQGroup not found for url: {rc.address}/{ROUTE_VERSION_PREFIX}/mq-group/{mqgroup_id}"
        ),
    ) as e:
        await utils.request_and_validate(
            rc,
            openapi_spec,
            "GET",
            f"/{ROUTE_VERSION_PREFIX}/mq-group/{mqgroup_id}",
        )
    assert e.value.response.status_code == 404


async def test_110__get_mq__error_404(rc: RestClient) -> None:
    """Test erroneous calls--logical errors (type-checking done by openapi)."""
    openapi_spec = await query_for_schema(rc)

    mqid = "foobarbaz"
    with pytest.raises(
        requests.HTTPError,
        match=re.escape(
            f"MQProfile not found for url: {rc.address}/{ROUTE_VERSION_PREFIX}/mq/{mqid}"
        ),
    ) as e:
        await utils.request_and_validate(
            rc, openapi_spec, "GET", f"/{ROUTE_VERSION_PREFIX}/mq/{mqid}"
        )
    assert e.value.response.status_code == 404
