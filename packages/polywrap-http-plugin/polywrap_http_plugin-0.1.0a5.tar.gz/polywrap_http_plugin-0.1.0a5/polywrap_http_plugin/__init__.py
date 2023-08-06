"""This package contains the HTTP plugin."""
import base64
from typing import Optional, cast

from httpx import AsyncClient
from httpx import Response as HttpxResponse
from polywrap_core import InvokerClient, UriPackageOrWrapper
from polywrap_msgpack import GenericMap
from polywrap_plugin import PluginPackage

from .wrap import ArgsGet, ArgsPost, Module, Response, ResponseType, manifest


def _is_response_binary(args: ArgsGet) -> bool:
    if args.get("request") is None:
        return False
    if not args["request"]:
        return False
    if not args["request"].get("responseType"):
        return False
    if args["request"]["responseType"] == 1:
        return True
    if args["request"]["responseType"] == "BINARY":
        return True
    return args["request"]["responseType"] == ResponseType.BINARY


class HttpPlugin(Module[None]):
    """HTTP plugin."""

    def __init__(self):
        """Initialize the HTTP plugin."""
        super().__init__(None)
        self.client = AsyncClient()

    async def get(
        self, args: ArgsGet, client: InvokerClient[UriPackageOrWrapper], env: None
    ) -> Optional[Response]:
        """Make a GET request to the given URL."""
        res: HttpxResponse
        if args.get("request") is None:
            res = await self.client.get(args["url"])
        elif args["request"] is not None:
            res = await self.client.get(
                args["url"],
                params=args["request"].get("urlParams"),
                headers=args["request"].get("headers"),
                timeout=cast(float, args["request"].get("timeout")),
            )
        else:
            res = await self.client.get(args["url"])

        if _is_response_binary(args):
            return Response(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return Response(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )

    async def post(
        self, args: ArgsPost, client: InvokerClient[UriPackageOrWrapper], env: None
    ) -> Optional[Response]:
        """Make a POST request to the given URL."""
        res: HttpxResponse
        if args.get("request") is None:
            res = await self.client.post(args["url"])
        elif args["request"] is not None:
            content = (
                args["request"]["body"].encode()
                if args["request"]["body"] is not None
                else None
            )
            res = await self.client.post(
                args["url"],
                content=content,
                params=args["request"].get("urlParams"),
                headers=args["request"].get("headers"),
                timeout=cast(float, args["request"].get("timeout")),
            )
        else:
            res = await self.client.post(args["url"])

        if _is_response_binary(args):
            return Response(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return Response(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )


def http_plugin():
    """Factory function for the HTTP plugin."""
    return PluginPackage(module=HttpPlugin(), manifest=manifest)
