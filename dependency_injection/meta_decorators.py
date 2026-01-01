"""
基于元类的装饰器实现
"""
from dependency_injection.meta_classes import ServiceMeta, ControllerMeta, get_global_container


def service(name: str = None):
    """
    服务装饰器 - 使用元类实现
    
    Args:
        name: 可选的服务名称，如果不提供则自动从类名生成
    """
    def decorator(cls):
        # 设置服务名称
        service_name = name or cls.__name__[0].lower() + cls.__name__[1:]
        
        # 创建新类，继承原始类并使用ServiceMeta元类
        class ServiceWithMeta(cls, metaclass=ServiceMeta):
            def __init__(self, *args, **kwargs):
                # 先调用原始类的构造函数
                cls.__init__(self, *args, **kwargs)
                self._is_service = True
        
        # 设置类级别的服务名称，避免多个服务发生同名覆盖
        ServiceWithMeta._service_name = service_name
        
        # 复制类型注解
        if hasattr(cls, '__annotations__'):
            ServiceWithMeta.__annotations__ = cls.__annotations__.copy()
        
        # 注册服务类到容器
        container = get_global_container()
        if container:
            container.register_service(service_name, ServiceWithMeta)
        
        return ServiceWithMeta
    
    return decorator


def controller(cls):
    """
    控制器装饰器 - 使用元类实现
    """
    # 设置控制器名称
    controller_name = cls.__name__[0].lower() + cls.__name__[1:]
    
    # 创建新类，继承原始类并使用ControllerMeta元类
    class ControllerWithMeta(cls, metaclass=ControllerMeta):
        def __init__(self, *args, **kwargs):
            # 先调用原始类的构造函数
            cls.__init__(self, *args, **kwargs)
            self._is_controller = True
    
    # 复制类型注解
    if hasattr(cls, '__annotations__'):
        ControllerWithMeta.__annotations__ = cls.__annotations__.copy()
    
    # 注册控制器类到容器
    container = get_global_container()
    if container:
        container.register_controller(controller_name, ControllerWithMeta)
    
    return ControllerWithMeta


# 简化的装饰器，直接使用元类
def simple_service(cls):
    """简化版服务装饰器"""
    service_name = cls.__name__[0].lower() + cls.__name__[1:]
    new_cls = type(cls.__name__, (cls,), {'__metaclass__': ServiceMeta, '_is_service': True})
    
    # 设置类级别的服务名称
    setattr(new_cls, '_service_name', service_name)
    
    # 注册服务类到容器
    container = get_global_container()
    if container:
        container.register_service(service_name, new_cls)
    
    return new_cls


def simple_controller(cls):
    """简化版控制器装饰器"""
    controller_name = cls.__name__[0].lower() + cls.__name__[1:]
    new_cls = type(cls.__name__, (cls,), {'__metaclass__': ControllerMeta, '_is_controller': True})
    
    # 注册控制器类到容器
    container = get_global_container()
    if container:
        container.register_controller(controller_name, new_cls)
    
    return new_cls