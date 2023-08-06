import random
from time import sleep
from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.http_error import HttpError
from ...models.http_validation_error import HTTPValidationError
from ...models.list_response_endpoint_out import ListResponseEndpointOut
from ...models.ordering import Ordering
from ...types import UNSET, Unset


def _get_kwargs(
    app_id: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/app/{app_id}/endpoint/".format(client.base_url, app_id=app_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["iterator"] = iterator

    json_order: Union[Unset, None, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value if order else None

    params["order"] = json_order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> ListResponseEndpointOut:
    if response.status_code == 401:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == 403:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == 404:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == 409:
        raise HttpError(response.json(), response.status_code)
    if response.status_code == 422:
        raise HTTPValidationError(response.json(), response.status_code)
    if response.status_code == 429:
        raise HttpError(response.json(), response.status_code)
    response_200 = ListResponseEndpointOut.from_dict(response.json())

    return response_200


sleep_time = 0.05
num_retries = 3


def sync_detailed(
    app_id: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseEndpointOut:
    """List Endpoints

     List the application's endpoints.

    Args:
        app_id (str):  Example: unique-app-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):  Example: ep_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseEndpointOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        client=client,
        limit=limit,
        iterator=iterator,
        order=order,
    )

    kwargs["headers"] = {"svix-req-id": f"{random.getrandbits(32)}", **kwargs["headers"]}

    retry_count = 0
    for retry in range(num_retries):
        response = httpx.request(
            verify=client.verify_ssl,
            **kwargs,
        )
        if response.status_code >= 500 and retry < num_retries:
            retry_count += 1
            kwargs["headers"]["svix-retry-count"] = str(retry_count)
            sleep(sleep_time)
            sleep_time * 2
        else:
            break

    return _parse_response(response=response)


def sync(
    app_id: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseEndpointOut:
    """List Endpoints

     List the application's endpoints.

    Args:
        app_id (str):  Example: unique-app-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):  Example: ep_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseEndpointOut
    """

    return sync_detailed(
        app_id=app_id,
        client=client,
        limit=limit,
        iterator=iterator,
        order=order,
    )


async def asyncio_detailed(
    app_id: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseEndpointOut:
    """List Endpoints

     List the application's endpoints.

    Args:
        app_id (str):  Example: unique-app-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):  Example: ep_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseEndpointOut
    """

    kwargs = _get_kwargs(
        app_id=app_id,
        client=client,
        limit=limit,
        iterator=iterator,
        order=order,
    )

    kwargs["headers"] = {"svix-req-id": f"{random.getrandbits(32)}", **kwargs["headers"]}

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        retry_count = 0
        for retry in range(num_retries):
            response = await _client.request(**kwargs)
            if response.status_code >= 500 and retry < num_retries:
                retry_count += 1
                kwargs["headers"]["svix-retry-count"] = str(retry_count)
                sleep(sleep_time)
                sleep_time * 2
            else:
                break

    return _parse_response(response=response)


async def asyncio(
    app_id: str,
    *,
    client: Client,
    limit: Union[Unset, None, int] = UNSET,
    iterator: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, Ordering] = UNSET,
) -> ListResponseEndpointOut:
    """List Endpoints

     List the application's endpoints.

    Args:
        app_id (str):  Example: unique-app-identifier.
        limit (Union[Unset, None, int]):
        iterator (Union[Unset, None, str]):  Example: ep_1srOrx2ZWZBpBUvZwXKQmoEYga2.
        order (Union[Unset, None, Ordering]): Defines the ordering in a listing of results.

    Returns:
        ListResponseEndpointOut
    """

    return await asyncio_detailed(
        app_id=app_id,
        client=client,
        limit=limit,
        iterator=iterator,
        order=order,
    )
