from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.cockroach_cloud_remove_user_from_role_resource_type import CockroachCloudRemoveUserFromRoleResourceType
from ...models.cockroach_cloud_remove_user_from_role_role_name import CockroachCloudRemoveUserFromRoleRoleName
from ...models.get_all_roles_for_user_response_contains_a_representation_of_all_roles_a_given_user_has import (
    GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas,
)
from ...types import Response


def _get_kwargs(
    user_id: str,
    resource_type: CockroachCloudRemoveUserFromRoleResourceType,
    resource_id: str,
    role_name: CockroachCloudRemoveUserFromRoleRoleName,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/v1/roles/{user_id}/{resource_type}/{resource_id}/{role_name}".format(
        client.base_url, user_id=user_id, resource_type=resource_type, resource_id=resource_id, role_name=role_name
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas.from_dict(
            response.json()
        )

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    resource_type: CockroachCloudRemoveUserFromRoleResourceType,
    resource_id: str,
    role_name: CockroachCloudRemoveUserFromRoleRoleName,
    *,
    client: Client,
) -> Response[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]:
    """Removes the user from the given role

    Args:
        user_id (str):
        resource_type (CockroachCloudRemoveUserFromRoleResourceType):
        resource_id (str):
        role_name (CockroachCloudRemoveUserFromRoleRoleName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        role_name=role_name,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    resource_type: CockroachCloudRemoveUserFromRoleResourceType,
    resource_id: str,
    role_name: CockroachCloudRemoveUserFromRoleRoleName,
    *,
    client: Client,
) -> Optional[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]:
    """Removes the user from the given role

    Args:
        user_id (str):
        resource_type (CockroachCloudRemoveUserFromRoleResourceType):
        resource_id (str):
        role_name (CockroachCloudRemoveUserFromRoleRoleName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]
    """

    return sync_detailed(
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        role_name=role_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    resource_type: CockroachCloudRemoveUserFromRoleResourceType,
    resource_id: str,
    role_name: CockroachCloudRemoveUserFromRoleRoleName,
    *,
    client: Client,
) -> Response[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]:
    """Removes the user from the given role

    Args:
        user_id (str):
        resource_type (CockroachCloudRemoveUserFromRoleResourceType):
        resource_id (str):
        role_name (CockroachCloudRemoveUserFromRoleRoleName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        role_name=role_name,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    resource_type: CockroachCloudRemoveUserFromRoleResourceType,
    resource_id: str,
    role_name: CockroachCloudRemoveUserFromRoleRoleName,
    *,
    client: Client,
) -> Optional[Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]]:
    """Removes the user from the given role

    Args:
        user_id (str):
        resource_type (CockroachCloudRemoveUserFromRoleResourceType):
        resource_id (str):
        role_name (CockroachCloudRemoveUserFromRoleRoleName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetAllRolesForUserResponseContainsARepresentationOfAllRolesAGivenUserHas]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            role_name=role_name,
            client=client,
        )
    ).parsed
