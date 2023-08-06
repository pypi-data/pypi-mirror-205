import inspect
import os
# import importlib


class ModuleScanner:
    
    def import_object(self, name):
        """Imports an object by name.
        import_object('x') is equivalent to 'import x'.
        import_object('x.y.z') is equivalent to 'from x.y import z'.
        """
        if not isinstance(name, str):
            name = name.encode('utf-8')
        if name.count('.') == 0:
            return __import__(name, None, None)

        parts = name.split('.')
        obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
        try:
            return getattr(obj, parts[-1])
        except AttributeError:
            raise ImportError("No module named %s" % parts[-1])

    def get_attrs_of_module(self, module_name='temp'):
        """
        获取模块中的类
        :param module_name:
        :return:
        """
        module = __import__(module_name)  # 动态引入模块(temp.py文件)
        # 用inspect.getmembers获取模块中的类
        classes = [clsname for (clsname, fullname) in inspect.getmembers(module, inspect.isclass)]

        dic_cls_methods = {}
        for clsname in classes:
            # 用python内置的getattr()方法获取模块的类，inspect.isfunction()方法过滤出该类的方法
            methods = [method_name for (method_name, method) in
                       inspect.getmembers(getattr(module, clsname), inspect.isfunction)]
            dic_cls_methods[clsname] = methods
        print(dic_cls_methods)

    def scan(self, route_file_path, resources_name):
        """
        Automatic import of modules and map routing
        根据接口文件夹自动导入模块和映射路由
        :param route_file_path: Api interface folder path API接口文件地址
        :param resources_name: Api folder module name, default `resources`
                               API接口文件模块名称，默认为 resources
        :return route_list:
            Returns an array containing tuples, the tuple content is
            `(Route endpoint, Request Class)`. The first parameter is the routing
            path, the second parameter is the request class object for this route.
            返回一个数组，里面是多个元组，元组的内容是第一个参数是路由地址，
            第二个参数是此路由的请求类对象
        """
        route_list = []

        def get_route_tuple(file_name, parent_path, load_package=False):
            """
            通过字符串导入类，并将路由和类以元组的方式添加到数组中
            :param file_name: API file name  文件名
            :param parent_path: file 路径（以.分割）
            :param load_package: 加载的package为true，加载module为false
            """
            nonlocal route_list

            # module = importlib.import_module('{}.{}'.format(
            #    resource_module_name, route_endpoint))
            if load_package:
                module = self.import_object(parent_path)
            else:
                route_endpoint = file_name.split(".py")[0]
                module = self.import_object('{}.{}'.format(parent_path, route_endpoint))

            # route_class = underline_to_hump(route_endpoint)
            # real_route_endpoint = r'/{}{}'.format(route_pre, route_endpoint)
            # route_list.append((real_route_endpoint, getattr(module, route_class)))

        def check_file_right(file_name):
            """
            过滤文件夹中不合法的文件，仅当文件为正常*.py文件时返回True
            :param file_name: 文件名
            :return:
            """
            if file_name.startswith("_"):
                return False
            if not file_name.endswith(".py"):
                return False
            if file_name.startswith("."):
                return False
            return True

        def recursive_find_route(route_path, sub_resource=""):
            """
            递归查找目标路径下的文件
            :param route_path: 全路径，以/分隔
            :param sub_resource: 全路径，以.分隔
            :return:
            """
            nonlocal resources_name
            if not os.path.exists(route_path):
                return
            # 如果文件夹存在，判断是否为package。如为package，首先import它，以加载__init__.py.
            if os.path.exists("{}/__init__.py".format(route_path)):
                file_name = os.path.basename(route_path)
                get_route_tuple(file_name, sub_resource, True)

            file_list = os.listdir(route_path)

            for file_item in file_list:
                if file_item.startswith("_"):
                    continue
                if file_item.startswith("."):
                    continue
                if os.path.isdir(route_path + "/{}".format(file_item)):
                    recursive_find_route(route_path + "/{}".format(file_item),
                                         sub_resource + ".{}".format(file_item))
                    continue
                if not check_file_right(file_item):
                    continue
                get_route_tuple(file_item, sub_resource)

        recursive_find_route(route_file_path, resources_name)

        return route_list
