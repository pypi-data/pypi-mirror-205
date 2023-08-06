from typing import Any, List, Optional, Dict, Type
from dockerode_api_proxy_client.settings.env import get_environment_enum
from dockerode_api_proxy_client.dto.image import ImageInfo
from dockerode_api_proxy_client.dto.container import ContainerInfo, ContainerInspectInfo
from dockerode_api_proxy_client.utils.get_authentication_header import (
    get_authentication_header,
    extend_headers,
)
from dockerode_api_proxy_client.utils.formatting import camel_case_keys, define_dict
from caesari_clients.base.generic_rest_client import GenericRestClient


class ApiProxyClient(GenericRestClient):
    def __init__(self, host: str, request_timeout: int = 10, *args, **kwargs) -> None:
        super(ApiProxyClient, self).__init__(host, request_timeout, *args, **kwargs)

    def _transform_response(
        self,
        Dataclass: Type[ContainerInspectInfo] | Type[ImageInfo] | Type[ContainerInfo],
        data: Dict[str, Any] | List[Any] | str,
    ):
        if isinstance(data, dict):
            if data == {}:
                return data
            return Dataclass(**data)
        if isinstance(data, list):
            if data == []:
                return data
            return list(map(lambda entry: Dataclass(**entry), data))
        return data

    async def get_all_images(self, *args, **kwargs) -> List[ImageInfo]:
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)
        response = await self._get("v1/image", *args, **kwargs)
        data = response["data"]
        result: List[ImageInfo] = self._transform_response(ImageInfo, data)
        return result

    async def pull_image_on_remote(
        self, image: str, *args, **kwargs
    ) -> List[ImageInfo]:
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        defined_params = {image: image}
        pull_params = camel_case_keys(define_dict(defined_params))
        response = await self._post(
            "v1/image/pull",
            json=pull_params,
            *args,
            **kwargs,
        )
        data = response["data"]
        result: List[ImageInfo] = self._transform_response(ImageInfo, data)
        return result

    async def get_all_containers(self, *args, **kwargs) -> List[ContainerInfo]:
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._get("v1/container", *args, **kwargs)
        data = response["data"]
        result: List[ContainerInfo] = self._transform_response(ContainerInfo, data)
        return result

    async def get_container_by_id(self, id: str, *args, **kwargs):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._get(f"v1/container/{id}", *args, **kwargs)
        data = response["data"]
        return data

    async def inspect_container_by_id(
        self, id: str, *args, **kwargs
    ) -> ContainerInspectInfo:
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._get(f"v1/container/{id}/inspect", *args, **kwargs)
        data = response["data"]
        result: ContainerInspectInfo = self._transform_response(
            ContainerInspectInfo, data
        )
        return result

    async def create(
        self,
        image: str,
        env: List[str],
        name: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        exposed_ports: Optional[Dict[str, Dict[str, None]]] = None,
        keep_alive: Optional[bool] = None,
        *args,
        **kwargs,
    ):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        defined_params = {
            "image": image,
            "env": env,
            "name": name,
            "labels": labels,
            "exposed_ports": exposed_ports,
            "keep_alive": keep_alive,
        }
        create_params = camel_case_keys(define_dict(defined_params))
        response = await self._post(
            "v1/container/create",
            json=create_params,
            *args,
            **kwargs,
        )
        data = response["data"]
        return data

    async def rename(
        self,
        id: str,
        name: str,
        *args,
        **kwargs,
    ):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        defined_params = {
            "name": name,
        }
        create_params = camel_case_keys(define_dict(defined_params))
        response = await self._post(
            f"v1/container/{id}/rename",
            json=create_params,
            *args,
            **kwargs,
        )
        data = response["data"]
        return data

    async def start(self, id: str, *args, **kwargs):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._post(f"v1/container/{id}/start", *args, **kwargs)
        data = response["data"]
        return data

    async def pause(self, id: str, *args, **kwargs):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._post(f"v1/container/{id}/pause", *args, **kwargs)
        data = response["data"]
        return data

    async def restart(self, id: str, *args, **kwargs):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._post(f"v1/container/{id}/restart", *args, **kwargs)
        data = response["data"]
        return data

    async def stop(self, id: str, *args, **kwargs):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._post(f"v1/container/{id}/stop", *args, **kwargs)
        data = response["data"]
        return data

    async def remove(self, id: str, *args, **kwargs):
        headers = kwargs.get("headers", {})
        jwt_secret = get_environment_enum().JWT_SECRET
        authenticated_headers = get_authentication_header(jwt_secret)
        kwargs["headers"] = extend_headers(headers, authenticated_headers)

        response = await self._delete(f"v1/container/{id}", *args, **kwargs)
        data = response["data"]
        return data
