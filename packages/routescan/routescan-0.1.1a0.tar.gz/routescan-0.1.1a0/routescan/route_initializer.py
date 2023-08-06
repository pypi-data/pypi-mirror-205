from routescan.module_scanner import ModuleScanner
from routescan.route_registrar import RouteRegistrar


class RouteInitializer:
    def __init__(self, app):
        self.app = app
        pass

    def register(self, file_path, base_module_name):
        # 根据路径扫描并加载module
        scanner = ModuleScanner()
        scanner.scan(file_path, base_module_name)

        # 将各module中的ApiRouter加入app
        self.do_register()
        pass

    def do_register(self):
        # 将各module中的ApiRouter加入app
        for item in RouteRegistrar.get_api_routers():
            self.app.include_router(item)

        # 将各module中Func方式注册路由加入app
        for item in RouteRegistrar.get_func_routers():
            self.app.add_api_route(item.path, item.endpoint, methods=item.methods, name=item.name)

        # 将各module中类方式注册路由加入app
        for item in RouteRegistrar.get_class_view_routers():
            self.app.add_route(item.path, item.route, methods=item.methods, name=item.name)
        pass
