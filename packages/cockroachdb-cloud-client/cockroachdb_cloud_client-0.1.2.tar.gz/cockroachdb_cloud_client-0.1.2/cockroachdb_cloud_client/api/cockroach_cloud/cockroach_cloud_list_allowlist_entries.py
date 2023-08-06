import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.cockroach_cloud_list_allowlist_entries_pagination_sort_order import (
    CockroachCloudListAllowlistEntriesPaginationSortOrder,
)
from ...models.list_allowlist_entries_response import ListAllowlistEntriesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    cluster_id: str,
    *,
    client: Client,
    pagination_page: Union[Unset, None, str] = UNSET,
    pagination_limit: Union[Unset, None, int] = UNSET,
    pagination_as_of_time: Union[Unset, None, datetime.datetime] = UNSET,
    pagination_sort_order: Union[Unset, None, CockroachCloudListAllowlistEntriesPaginationSortOrder] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/clusters/{cluster_id}/networking/allowlist".format(client.base_url, cluster_id=cluster_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["pagination.page"] = pagination_page

    params["pagination.limit"] = pagination_limit

    json_pagination_as_of_time: Union[Unset, None, str] = UNSET
    if not isinstance(pagination_as_of_time, Unset):
        json_pagination_as_of_time = pagination_as_of_time.isoformat() if pagination_as_of_time else None

    params["pagination.as_of_time"] = json_pagination_as_of_time

    json_pagination_sort_order: Union[Unset, None, str] = UNSET
    if not isinstance(pagination_sort_order, Unset):
        json_pagination_sort_order = pagination_sort_order.value if pagination_sort_order else None

    params["pagination.sort_order"] = json_pagination_sort_order

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, ListAllowlistEntriesResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAllowlistEntriesResponse.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, ListAllowlistEntriesResponse]]:
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
    pagination_page: Union[Unset, None, str] = UNSET,
    pagination_limit: Union[Unset, None, int] = UNSET,
    pagination_as_of_time: Union[Unset, None, datetime.datetime] = UNSET,
    pagination_sort_order: Union[Unset, None, CockroachCloudListAllowlistEntriesPaginationSortOrder] = UNSET,
) -> Response[Union[Any, ListAllowlistEntriesResponse]]:
    """Get the IP allowlist and propagation status for a cluster

     Sort order: CIDR address

    Args:
        cluster_id (str):
        pagination_page (Union[Unset, None, str]):
        pagination_limit (Union[Unset, None, int]):
        pagination_as_of_time (Union[Unset, None, datetime.datetime]):
        pagination_sort_order (Union[Unset, None,
            CockroachCloudListAllowlistEntriesPaginationSortOrder]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAllowlistEntriesResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        client=client,
        pagination_page=pagination_page,
        pagination_limit=pagination_limit,
        pagination_as_of_time=pagination_as_of_time,
        pagination_sort_order=pagination_sort_order,
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
    pagination_page: Union[Unset, None, str] = UNSET,
    pagination_limit: Union[Unset, None, int] = UNSET,
    pagination_as_of_time: Union[Unset, None, datetime.datetime] = UNSET,
    pagination_sort_order: Union[Unset, None, CockroachCloudListAllowlistEntriesPaginationSortOrder] = UNSET,
) -> Optional[Union[Any, ListAllowlistEntriesResponse]]:
    """Get the IP allowlist and propagation status for a cluster

     Sort order: CIDR address

    Args:
        cluster_id (str):
        pagination_page (Union[Unset, None, str]):
        pagination_limit (Union[Unset, None, int]):
        pagination_as_of_time (Union[Unset, None, datetime.datetime]):
        pagination_sort_order (Union[Unset, None,
            CockroachCloudListAllowlistEntriesPaginationSortOrder]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAllowlistEntriesResponse]
    """

    return sync_detailed(
        cluster_id=cluster_id,
        client=client,
        pagination_page=pagination_page,
        pagination_limit=pagination_limit,
        pagination_as_of_time=pagination_as_of_time,
        pagination_sort_order=pagination_sort_order,
    ).parsed


async def asyncio_detailed(
    cluster_id: str,
    *,
    client: Client,
    pagination_page: Union[Unset, None, str] = UNSET,
    pagination_limit: Union[Unset, None, int] = UNSET,
    pagination_as_of_time: Union[Unset, None, datetime.datetime] = UNSET,
    pagination_sort_order: Union[Unset, None, CockroachCloudListAllowlistEntriesPaginationSortOrder] = UNSET,
) -> Response[Union[Any, ListAllowlistEntriesResponse]]:
    """Get the IP allowlist and propagation status for a cluster

     Sort order: CIDR address

    Args:
        cluster_id (str):
        pagination_page (Union[Unset, None, str]):
        pagination_limit (Union[Unset, None, int]):
        pagination_as_of_time (Union[Unset, None, datetime.datetime]):
        pagination_sort_order (Union[Unset, None,
            CockroachCloudListAllowlistEntriesPaginationSortOrder]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ListAllowlistEntriesResponse]]
    """

    kwargs = _get_kwargs(
        cluster_id=cluster_id,
        client=client,
        pagination_page=pagination_page,
        pagination_limit=pagination_limit,
        pagination_as_of_time=pagination_as_of_time,
        pagination_sort_order=pagination_sort_order,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cluster_id: str,
    *,
    client: Client,
    pagination_page: Union[Unset, None, str] = UNSET,
    pagination_limit: Union[Unset, None, int] = UNSET,
    pagination_as_of_time: Union[Unset, None, datetime.datetime] = UNSET,
    pagination_sort_order: Union[Unset, None, CockroachCloudListAllowlistEntriesPaginationSortOrder] = UNSET,
) -> Optional[Union[Any, ListAllowlistEntriesResponse]]:
    """Get the IP allowlist and propagation status for a cluster

     Sort order: CIDR address

    Args:
        cluster_id (str):
        pagination_page (Union[Unset, None, str]):
        pagination_limit (Union[Unset, None, int]):
        pagination_as_of_time (Union[Unset, None, datetime.datetime]):
        pagination_sort_order (Union[Unset, None,
            CockroachCloudListAllowlistEntriesPaginationSortOrder]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ListAllowlistEntriesResponse]
    """

    return (
        await asyncio_detailed(
            cluster_id=cluster_id,
            client=client,
            pagination_page=pagination_page,
            pagination_limit=pagination_limit,
            pagination_as_of_time=pagination_as_of_time,
            pagination_sort_order=pagination_sort_order,
        )
    ).parsed
