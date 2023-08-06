import threading
import typing
from fastapi import APIRouter

from routescan.api_router import ApiRouter
from routescan.route_info import FuncRouteInfo, ClassViewRouteInfo


class RouteRegistrar:
    """
    统一路由注册服务类，通过三类6个方法实现路由的集中注册
    """
    _apiRouterList: typing.List[APIRouter] = []
    _funcRouterList: typing.List[FuncRouteInfo] = []
    _classViewRouterList: typing.List[ClassViewRouteInfo] = []
    _rlock = threading.RLock()

    @classmethod
    def add_original_api_router(cls, api_router: APIRouter):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._apiRouterList.append(api_router)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def add_original_api_routers(cls, api_route_list: typing.List[APIRouter]):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._apiRouterList.extend(api_route_list)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def add_api_router(cls, api_router: ApiRouter):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._apiRouterList.append(api_router.get_api_router)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def add_api_routers(cls, api_route_list: typing.List[ApiRouter]):
        # 加锁
        cls._rlock.acquire()
        try:
            for item in api_route_list:
                cls._apiRouterList.append(item.get_api_router())
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def get_api_routers(cls) -> typing.List[APIRouter]:
        return cls._apiRouterList

    @classmethod
    def add_func_router(cls, func_router: FuncRouteInfo):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._funcRouterList.append(func_router)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def add_func_routers(cls, func_route_list: typing.List[FuncRouteInfo]):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._funcRouterList.extend(func_route_list)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def get_func_routers(cls) -> typing.List[FuncRouteInfo]:
        return cls._funcRouterList

    @classmethod
    def add_class_view_router(cls, class_view_router: ClassViewRouteInfo):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._classViewRouterList.append(class_view_router)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def add_class_view_routers(cls, class_view_route_list: typing.List[ClassViewRouteInfo]):
        # 加锁
        cls._rlock.acquire()
        try:
            cls._classViewRouterList.extend(class_view_route_list)
        finally:
            # 修改完成，释放锁
            cls._rlock.release()

    @classmethod
    def get_class_view_routers(cls) -> typing.List[ClassViewRouteInfo]:
        return cls._classViewRouterList
