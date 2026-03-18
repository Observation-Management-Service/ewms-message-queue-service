"""Tests for querying about queues."""

import json
import os
import re
from pathlib import Path

import openapi_core
import pytest
import requests
from jsonschema_path import SchemaPath
from rest_tools.client import RestClient, utils
from rest_tools.client.utils import request_and_validate

_URL_V_PREFIX = "v1"
BROKER_TYPE = "rabbitmq"


_OPENAPI_JSON = Path(__file__).parent / "../../mqs/openapi.json"


async def query_for_schema(rc: RestClient) -> openapi_core.OpenAPI:
    """Get the OpenAPI schema."""
    resp = await request_and_validate(  # here we are asserting the endpoint's response
        rc,
        # only read json file for this request
        openapi_core.OpenAPI(SchemaPath.from_file_path(str(_OPENAPI_JSON))),
        "GET",
        "/v1/mqs/schema/openapi",
    )
    # check that the schema returned is the same as the one on disk
    with open(_OPENAPI_JSON, "rb") as f:
        for k in list(resp["info"].keys()):  # so to change size during iteration
            # check that the schema was populated correctly
            assert resp["info"][k], f"full info fields: {resp['info']!r}"
            # don't include extra 'info' fields populated @ runtime
            if k not in ("title", "version"):
                resp["info"].pop(k)
        # ...
        assert json.load(f) == resp
    return openapi_core.OpenAPI(SchemaPath.from_dict(resp))


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
