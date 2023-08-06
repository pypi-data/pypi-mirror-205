from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.delete_egress_rule_response import DeleteEgressRuleResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    idempotency_key: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/clusters/{cluster_id}/networking/egress-rules/{rule_id}".format(
        client.base_url, cluster_id=cluster_id, rule_id=rule_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["idempotency_key"] = idempotency_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, DeleteEgressRuleResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteEgressRuleResponse.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, DeleteEgressRuleResponse]]:
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
    idempotency_key: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, DeleteEgressRuleResponse]]:
    """Delete an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        idempotency_key (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteEgressRuleResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        rule_id=rule_id,
        client=client,
        idempotency_key=idempotency_key,
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
    idempotency_key: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, DeleteEgressRuleResponse]]:
    """Delete an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        idempotency_key (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteEgressRuleResponse]
    """

    return sync_detailed(
        cluster_id=cluster_id,
        rule_id=rule_id,
        client=client,
        idempotency_key=idempotency_key,
    ).parsed


async def asyncio_detailed(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    idempotency_key: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, DeleteEgressRuleResponse]]:
    """Delete an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        idempotency_key (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteEgressRuleResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        rule_id=rule_id,
        client=client,
        idempotency_key=idempotency_key,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cluster_id: str,
    rule_id: str,
    *,
    client: Client,
    idempotency_key: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, DeleteEgressRuleResponse]]:
    """Delete an existing egress rule

    Args:
        cluster_id (str):
        rule_id (str):
        idempotency_key (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteEgressRuleResponse]
    """

    return (
        await asyncio_detailed(
            cluster_id=cluster_id,
            rule_id=rule_id,
            client=client,
            idempotency_key=idempotency_key,
        )
    ).parsed
