from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.cockroach_cloud_edit_egress_rule_edit_egress_rule_request import (
    CockroachCloudEditEgressRuleEditEgressRuleRequest,
)
from ...models.edit_egress_rule_response import EditEgressRuleResponse
from ...types import Response


def _get_kwargs(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    json_body: CockroachCloudEditEgressRuleEditEgressRuleRequest,
) -> Dict[str, Any]:
    url = "{}/api/v1/clusters/{cluster_id}/networking/egress-rules/{rule_id}".format(
        client.base_url, cluster_id=cluster_id, rule_id=rule_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, EditEgressRuleResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EditEgressRuleResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, response.json())
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, response.json())
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, response.json())
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, response.json())
        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, response.json())
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, EditEgressRuleResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    json_body: CockroachCloudEditEgressRuleEditEgressRuleRequest,
) -> Response[Union[Any, EditEgressRuleResponse]]:
    """Edit an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        json_body (CockroachCloudEditEgressRuleEditEgressRuleRequest): EditEgressRuleRequest is
            the input message to the EditEgressRule RPC. Example: {'cluster_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed100', 'ports': [443, 80], 'rule_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed2aa'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EditEgressRuleResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        rule_id=rule_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    json_body: CockroachCloudEditEgressRuleEditEgressRuleRequest,
) -> Optional[Union[Any, EditEgressRuleResponse]]:
    """Edit an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        json_body (CockroachCloudEditEgressRuleEditEgressRuleRequest): EditEgressRuleRequest is
            the input message to the EditEgressRule RPC. Example: {'cluster_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed100', 'ports': [443, 80], 'rule_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed2aa'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EditEgressRuleResponse]
    """

    return sync_detailed(
        cluster_id=cluster_id,
        rule_id=rule_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    json_body: CockroachCloudEditEgressRuleEditEgressRuleRequest,
) -> Response[Union[Any, EditEgressRuleResponse]]:
    """Edit an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        json_body (CockroachCloudEditEgressRuleEditEgressRuleRequest): EditEgressRuleRequest is
            the input message to the EditEgressRule RPC. Example: {'cluster_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed100', 'ports': [443, 80], 'rule_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed2aa'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EditEgressRuleResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        rule_id=rule_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    json_body: CockroachCloudEditEgressRuleEditEgressRuleRequest,
) -> Optional[Union[Any, EditEgressRuleResponse]]:
    """Edit an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        json_body (CockroachCloudEditEgressRuleEditEgressRuleRequest): EditEgressRuleRequest is
            the input message to the EditEgressRule RPC. Example: {'cluster_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed100', 'ports': [443, 80], 'rule_id':
            '35c4abb2-bb66-46d7-afed-25ebef5ed2aa'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EditEgressRuleResponse]
    """

    return (
        await asyncio_detailed(
            cluster_id=cluster_id,
            rule_id=rule_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
