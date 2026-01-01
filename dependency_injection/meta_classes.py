"""
基于元类的依赖注入架构
"""
from typing import Dict, Any, Optional, Type
import inspect


# 全局容器引用
_global_container = None

def set_global_container(container):
    """设置全局容器"""
    global _global_container
    _global_container = container

def get_global_container():
    """获取全局容器"""
    return _global_container


class ServiceMeta(type):
    """服务元类"""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 如果没有预先设置服务名称，则基于类名生成
        if not hasattr(cls, '_service_name'):
            cls._service_name = name[0].lower() + name[1:] if name else name
        
        # 提取依赖信息
        if hasattr(cls, '__annotations__'):
            cls._dependencies = {}
            for attr_name, attr_type in cls.__annotations__.items():
                if not attr_name.startswith('_'):
                    cls._dependencies[attr_name] = attr_type
        
        return cls
    
    def __call__(cls, *args, **kwargs):
        # 创建实例
        instance = super().__call__(*args, **kwargs)
        
        # 获取全局容器
        container = get_global_container()
        if container:
            # 注册服务实例（使用类级别服务名）
            container.register(cls._service_name, instance)
            print(f"Registered service {cls._service_name}")
        
        return instance


class ControllerMeta(type):
    """控制器元类"""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 提取依赖信息
        if hasattr(cls, '__annotations__'):
            cls._dependencies = {}
            for attr_name, attr_type in cls.__annotations__.items():
                if not attr_name.startswith('_'):
                    cls._dependencies[attr_name] = attr_type
        
        return cls
    
    def __call__(cls, *args, **kwargs):
        # 创建实例
        instance = super().__call__(*args, **kwargs)
        
        # 获取全局容器
        container = get_global_container()
        if container:
            # 注入依赖
            container.inject_dependencies(instance)
            
            # 调用初始化方法（如果有）
            if hasattr(instance, 'initialize'):
                instance.initialize()
        
        return instance


class AutoWireMeta(type):
    """自动装配元类"""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 提取依赖信息
        if hasattr(cls, '__annotations__'):
            cls._dependencies = {}
            for attr_name, attr_type in cls.__annotations__.items():
                if not attr_name.startswith('_'):
                    cls._dependencies[attr_name] = attr_type
        
        return cls
    
    def __call__(cls, *args, **kwargs):
        # 创建实例
        instance = super().__call__(*args, **kwargs)
        
        # 获取全局容器
        container = get_global_container()
        if container:
            # 注入依赖
            container.inject_dependencies(instance)
            
            # 调用初始化方法（如果有）
            if hasattr(instance, 'initialize'):
                instance.initialize()
        
        return instance