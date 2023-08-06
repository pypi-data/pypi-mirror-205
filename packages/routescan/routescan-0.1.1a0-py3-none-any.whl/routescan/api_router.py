from enum import Enum
from typing import Optional, Union, Set, List, Callable, Any
from fastapi.routing import APIRoute, APIWebSocketRoute, APIRouter
from routescan.types import DecoratedCallable


class ApiRouter:
    def __init__(
        self,
        *,
        prefix: str = "",
    ) -> None:
        self.prefix = prefix
        self.api_router = APIRouter(prefix=prefix)

    def get_api_router(self) -> APIRouter:
        return self.api_router

    def route(
        self,
        path: str,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.api_router.add_route(
                path,
                func,
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
            )
            return func

        return decorator

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        status_code: Optional[int] = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        name: Optional[str] = None,
    ) -> None:
        route_class = APIRoute
        route = route_class(
            self.prefix + path,
            endpoint=endpoint,
            status_code=status_code,
            methods=methods,
            name=name,
        )
        self.api_router.routes.append(route)

    def api_route(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_api_route(
                path,
                func,
                status_code=status_code,
                methods=methods,
                name=name,
            )
            return func

        return decorator

    def add_api_websocket_route(
        self, path: str, endpoint: Callable[..., Any], name: Optional[str] = None
    ) -> None:
        route = APIWebSocketRoute(
            self.prefix + path,
            endpoint=endpoint,
            name=name,
        )
        self.api_router.routes.append(route)

    def websocket(
        self, path: str, name: Optional[str] = None
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_api_websocket_route(path, func, name=name)
            return func

        return decorator

    def websocket_route(
        self, path: str, name: Union[str, None] = None
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.add_websocket_route(path, func, name=name)
            return func

        return decorator

    def include_router(
        self,
        router: "APIRouter",
        *,
        prefix: str = "",
    ) -> None:
        self.api_router.include_router(router, prefix=prefix)

    def get(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["GET"],
            name=name,
        )

    def put(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["PUT"],
            name=name,
        )

    def post(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["POST"],
            name=name,
        )

    def delete(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["DELETE"],
            name=name,
        )

    def options(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["OPTIONS"],
            name=name,
        )

    def head(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["HEAD"],
            name=name,
        )

    def patch(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["PATCH"],
            name=name,
        )

    def trace(
        self,
        path: str,
        *,
        status_code: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return self.api_route(
            path=path,
            status_code=status_code,
            methods=["TRACE"],
            name=name,
        )

    def on_event(
        self, event_type: str
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.api_router.add_event_handler(event_type, func)
            return func

        return decorator
