from typing import Callable, Any, Coroutine, Optional, List


class FuncRouteInfo:
    """
    函数式路由注册的扩展接口，更多参数待逐步添加
    """
    def __init__(
            self,
            path: str,
            endpoint: Callable,
            methods: Optional[List[str]] = ["GET"],
            name: Optional[str] = None):
        self.path = path
        self.endpoint = endpoint
        self.methods = methods
        self.name = name
        # self.response_class = response_class


class ClassViewRouteInfo:
    """
    类视图式路由注册的扩展接口，仅支持get、post、put、head等标准方法注册，同时参数必须位request对象，返回值用Response对象包裹
    """
    def __init__(
            self,
            path: str,
            route: Callable,
            methods: Optional[List[str]] = None,
            name: Optional[str] = None,
            include_in_schema: bool = True):
        self.path = path
        self.route = route
        self.methods = methods
        self.name = name
        self.include_in_schema = include_in_schema

