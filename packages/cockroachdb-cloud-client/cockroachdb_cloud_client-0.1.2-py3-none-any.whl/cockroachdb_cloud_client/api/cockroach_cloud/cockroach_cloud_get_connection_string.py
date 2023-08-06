from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.cockroach_cloud_get_connection_string_os import CockroachCloudGetConnectionStringOs
from ...models.get_connection_string_response import GetConnectionStringResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    cluster_id: str,
    *,
    client: Client,
    database: Union[Unset, None, str] = "defaultdb",
    sql_user: Union[Unset, None, str] = UNSET,
    os: Union[Unset, None, CockroachCloudGetConnectionStringOs] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/clusters/{cluster_id}/connection-string".format(client.base_url, cluster_id=cluster_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["database"] = database

    params["sql_user"] = sql_user

    json_os: Union[Unset, None, str] = UNSET
    if not isinstance(os, Unset):
        json_os = os.value if os else None

    params["os"] = json_os

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, GetConnectionStringResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetConnectionStringResponse.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, GetConnectionStringResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cluster_id: str,
    *,
    client: Client,
    database: Union[Unset, None, str] = "defaultdb",
    sql_user: Union[Unset, None, str] = UNSET,
    os: Union[Unset, None, CockroachCloudGetConnectionStringOs] = UNSET,
) -> Response[Union[Any, GetConnectionStringResponse]]:
    """Get a formatted generic connection string for a cluster

    Args:
        cluster_id (str):
        database (Union[Unset, None, str]):  Default: 'defaultdb'.
        sql_user (Union[Unset, None, str]):
        os (Union[Unset, None, CockroachCloudGetConnectionStringOs]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetConnectionStringResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        client=client,
        database=database,
        sql_user=sql_user,
        os=os,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cluster_id: str,
    *,
    client: Client,
    database: Union[Unset, None, str] = "defaultdb",
    sql_user: Union[Unset, None, str] = UNSET,
    os: Union[Unset, None, CockroachCloudGetConnectionStringOs] = UNSET,
) -> Optional[Union[Any, GetConnectionStringResponse]]:
    """Get a formatted generic connection string for a cluster

    Args:
        cluster_id (str):
        database (Union[Unset, None, str]):  Default: 'defaultdb'.
        sql_user (Union[Unset, None, str]):
        os (Union[Unset, None, CockroachCloudGetConnectionStringOs]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetConnectionStringResponse]
    """

    return sync_detailed(
        cluster_id=cluster_id,
        client=client,
        database=database,
        sql_user=sql_user,
        os=os,
    ).parsed


async def asyncio_detailed(
    cluster_id: str,
    *,
    client: Client,
    database: Union[Unset, None, str] = "defaultdb",
    sql_user: Union[Unset, None, str] = UNSET,
    os: Union[Unset, None, CockroachCloudGetConnectionStringOs] = UNSET,
) -> Response[Union[Any, GetConnectionStringResponse]]:
    """Get a formatted generic connection string for a cluster

    Args:
        cluster_id (str):
        database (Union[Unset, None, str]):  Default: 'defaultdb'.
        sql_user (Union[Unset, None, str]):
        os (Union[Unset, None, CockroachCloudGetConnectionStringOs]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetConnectionStringResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        client=client,
        database=database,
        sql_user=sql_user,
        os=os,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cluster_id: str,
    *,
    client: Client,
    database: Union[Unset, None, str] = "defaultdb",
    sql_user: Union[Unset, None, str] = UNSET,
    os: Union[Unset, None, CockroachCloudGetConnectionStringOs] = UNSET,
) -> Optional[Union[Any, GetConnectionStringResponse]]:
    """Get a formatted generic connection string for a cluster

    Args:
        cluster_id (str):
        database (Union[Unset, None, str]):  Default: 'defaultdb'.
        sql_user (Union[Unset, None, str]):
        os (Union[Unset, None, CockroachCloudGetConnectionStringOs]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetConnectionStringResponse]
    """

    return (
        await asyncio_detailed(
            cluster_id=cluster_id,
            client=client,
            database=database,
            sql_user=sql_user,
            os=os,
        )
    ).parsed
