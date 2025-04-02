"""Tests for querying about queues."""

import json
import os
import re

import openapi_core
import pytest
import requests
from jsonschema_path import SchemaPath
from rest_tools.client import RestClient, utils

_URL_V_PREFIX = "v1"
BROKER_TYPE = "rabbitmq"


async def query_for_schema(rc: RestClient) -> openapi_core.OpenAPI:
    """Grab the openapi schema from the rest server and check that it matches the json file."""
    resp = await rc.request("GET", f"/{_URL_V_PREFIX}/mqs/schema/openapi")
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

    workflow_id = "abc123"
    queue_aliases = ["queue1", "queue2", "queue3"]
    public = ["queue1", "queue3"]

    # reserve mq group
    resp = await utils.request_and_validate(
        rc,
        openapi_spec,
        "POST",
        f"/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group/reservation",
        {"queue_aliases": queue_aliases, "public": public},
    )
    mqgroup = resp["mqgroup"]
    assert mqgroup["workflow_id"] == workflow_id
    assert mqgroup["criteria"] is None
    og_mqprofiles = resp["mqprofiles"]
    assert len(og_mqprofiles) == len(queue_aliases)
    for mqprofile in og_mqprofiles:
        assert mqprofile["workflow_id"] == workflow_id
        assert mqprofile["timestamp"] == mqgroup["timestamp"]
        assert mqprofile["alias"] in queue_aliases
        assert mqprofile["is_public"] == bool(mqprofile["alias"] in public)
        assert not mqprofile["is_activated"]

    # check GET
    resp = await utils.request_and_validate(
        rc,
        openapi_spec,
        "GET",
        f"/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group",
    )
    assert resp == mqgroup
    # check GET
    for mqprofile in og_mqprofiles:
        resp = await utils.request_and_validate(
            rc,
            openapi_spec,
            "GET",
            f"/{_URL_V_PREFIX}/mqs/mq-profiles/{mqprofile['mqid']}",
        )
        assert resp == mqprofile
    # check GET for public mq profiles
    resp = await utils.request_and_validate(
        rc,
        openapi_spec,
        "GET",
        f"/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-profiles/public",
    )
    assert len(resp["mqprofiles"]) == len(public)
    assert resp["mqprofiles"] == [m for m in og_mqprofiles if m["alias"] in public]

    # activate mq group
    resp = await utils.request_and_validate(
        rc,
        openapi_spec,
        "POST",
        f"/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group/activation",
        {"criteria": {"priority": 99}},
    )
    assert resp["mqgroup"] == {**mqgroup, "criteria": {"priority": 99}}
    for i, resp_mqp in enumerate(resp["mqprofiles"]):
        for k, v in resp_mqp.items():
            match k:
                # newly update fields...
                case "is_activated":
                    assert v is True
                case "auth_token":
                    assert v is not None  # token generation is tested by test_jwks.py
                case "broker_type":
                    assert v == BROKER_TYPE
                case "broker_address":
                    assert (
                        v
                        == f'{os.environ["BROKER_QUEUE_USERNAME"]}@{os.environ["BROKER_URL"]}'
                    )
                # assert value has not changed
                case _:
                    assert v == og_mqprofiles[i][k]


async def test_100__mqgroup_activation__error_404(rc: RestClient) -> None:
    """Test erroneous calls--logical errors (type-checking done by openapi)."""
    openapi_spec = await query_for_schema(rc)

    workflow_id = "foobarbaz"
    with pytest.raises(
        requests.HTTPError,
        match=re.escape(
            f"No MQProfiles found for workflow id for url: {rc.address}/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group/activation"
        ),
    ) as e:
        await utils.request_and_validate(
            rc,
            openapi_spec,
            "POST",
            f"/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group/activation",
            {"criteria": {"priority": 99}},
        )
    assert e.value.response.status_code == 404


async def test_110__get_mqgroup__error_404(rc: RestClient) -> None:
    """Test erroneous calls--logical errors (type-checking done by openapi)."""
    openapi_spec = await query_for_schema(rc)

    workflow_id = "foobarbaz"
    with pytest.raises(
        requests.HTTPError,
        match=re.escape(
            f"MQGroup not found for url: {rc.address}/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group"
        ),
    ) as e:
        await utils.request_and_validate(
            rc,
            openapi_spec,
            "GET",
            f"/{_URL_V_PREFIX}/mqs/workflows/{workflow_id}/mq-group",
        )
    assert e.value.response.status_code == 404


async def test_200__get_mq_profile__error_404(rc: RestClient) -> None:
    """Test erroneous calls--logical errors (type-checking done by openapi)."""
    openapi_spec = await query_for_schema(rc)

    mqid = "foobarbaz"
    with pytest.raises(
        requests.HTTPError,
        match=re.escape(
            f"MQProfile not found for url: {rc.address}/{_URL_V_PREFIX}/mqs/mq-profiles/{mqid}"
        ),
    ) as e:
        await utils.request_and_validate(
            rc, openapi_spec, "GET", f"/{_URL_V_PREFIX}/mqs/mq-profiles/{mqid}"
        )
    assert e.value.response.status_code == 404
