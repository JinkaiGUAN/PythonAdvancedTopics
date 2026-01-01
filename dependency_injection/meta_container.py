"""
基于元类的依赖注入容器
"""
from typing import Dict, Any, Optional, Type, List
from dependency_injection.meta_classes import AutoWireMeta, ServiceMeta, ControllerMeta, set_global_container


class MetaContainer(metaclass=AutoWireMeta):
    """使用元类的依赖注入容器"""
    
    def __init__(self):
        self._service_instances: Dict[str, Any] = {}
        self._controller_instances: list = []
        self._service_classes: Dict[str, Type] = {}
        self._controller_classes: Dict[str, Type] = {}
        # 设置自己为全局容器
        set_global_container(self)
    
    def register(self, name: str, instance: Any) -> None:
        """注册服务实例"""
        self._service_instances[name] = instance
    
    def register_service(self, name: str, service_class: Type) -> None:
        """注册服务类"""
        self._service_classes[name] = service_class
    
    def register_controller(self, name: str, controller_class: Type) -> None:
        """注册控制器类"""
        self._controller_classes[name] = controller_class
    
    def get(self, name: str) -> Optional[Any]:
        """获取服务实例"""
        return self._service_instances.get(name)
    
    def get_service_instance(self, class_name: str) -> Optional[Any]:
        """根据类名获取服务实例"""
        print(f"Looking for service instance with class name: {class_name}")
        print(f"Available services: {list(self._service_instances.keys())}")
        
        # 首先尝试直接匹配
        if class_name in self._service_instances:
            return self._service_instances[class_name]
        
        # 然后尝试转换为camelCase匹配
        service_name = class_name[0].lower() + class_name[1:] if class_name else class_name
        result = self._service_instances.get(service_name)
        print(f"Found service: {result}")
        return result
    
    def get_all_services(self) -> Dict[str, Any]:
        """获取所有服务实例"""
        return self._service_instances.copy()
    
    def get_all_service_classes(self) -> Dict[str, Type]:
        """获取所有服务类"""
        return self._service_classes.copy()
    
    def get_all_controller_classes(self) -> Dict[str, Type]:
        """获取所有控制器类"""
        return self._controller_classes.copy()
    
    def inject_dependencies(self, instance: Any) -> None:
        """注入依赖到实例"""
        print(f"Injecting dependencies into {type(instance).__name__}")
        if not hasattr(instance, '_dependencies'):
            print("No dependencies found")
            return
        
        print(f"Found dependencies: {instance._dependencies}")
        for attr_name, attr_type in instance._dependencies.items():
            # 获取依赖的服务名称
            service_name = self._get_service_name(attr_type)
            print(f"Looking for service {service_name} for attribute {attr_name}")
            
            # 从容器中获取依赖实例
            dependency_instance = self.get(service_name)
            if dependency_instance:
                setattr(instance, attr_name, dependency_instance)
                print(f"Injected {service_name} into {attr_name}")
            else:
                print(f"Service {service_name} not found")
    
    def _get_service_name(self, cls: Type) -> str:
        """获取类的服务名称"""
        if isinstance(cls, str):
            # 处理字符串类型（前向引用）
            return cls[0].lower() + cls[1:] if cls else cls
        elif hasattr(cls, '_service_name'):
            return cls._service_name
        # 默认转换：PascalCase -> camelCase
        name = cls.__name__
        return name[0].lower() + name[1:] if name else name
    
    def auto_wire_services(self) -> None:
        """自动装配所有注册的服务"""
        print("Auto-wiring services...")
        # 实例化所有服务类
        for service_name, service_class in self._service_classes.items():
            if service_name not in self._service_instances:
                print(f"Creating instance of {service_name}")
                instance = service_class()
                self.register(service_name, instance)
        
        # 注入依赖
        for instance in self._service_instances.values():
            self.inject_dependencies(instance)
    
    def auto_wire_controllers(self) -> None:
        """自动装配所有控制器"""
        print("Auto-wiring controllers...")
        # 实例化所有控制器类
        for controller_name, controller_class in self._controller_classes.items():
            print(f"Creating instance of {controller_name}")
            instance = controller_class()
            self._controller_instances.append(instance)
            
            # 注入依赖
            self.inject_dependencies(instance)
    
    def get_controllers(self) -> list:
        """获取所有控制器实例"""
        return self._controller_instances.copy()
    
    def clear(self) -> None:
        """清空容器中的所有实例和类"""
        self._service_instances.clear()
        self._controller_instances.clear()
        self._service_classes.clear()
        self._controller_classes.clear()


# 创建全局容器实例
meta_container = MetaContainer()