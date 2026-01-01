"""
使用元类架构的示例实现
"""
try:
    # 优先使用包方式导入（推荐通过 -m 运行）
    from dependency_injection.meta_container import meta_container
    from dependency_injection.meta_decorators import service, controller
except ModuleNotFoundError:
    # 当直接运行文件时，父目录不在 sys.path，添加父目录以支持绝对导入
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from dependency_injection.meta_container import meta_container
    from dependency_injection.meta_decorators import service, controller


@service()
class MetaServiceA:
    """使用元类的服务A"""
    
    def __init__(self):
        self.message = "This is a message from MetaServiceA"
        print(f"MetaServiceA initialized with message: {self.message}")
    
    def do_something(self):
        return "MetaServiceA is doing something"
    
    def get_message(self):
        return self.message


@service()
class MetaServiceB:
    """使用元类的服务B，依赖ServiceA"""
    
    # 类型注解会自动被元类识别为依赖
    serviceA: 'MetaServiceA'  # 使用字符串前向引用
    
    def __init__(self):
        print("MetaServiceB initialized")
    
    def do_something_with_a(self, message: str):
        action = self.serviceA.do_something()
        return f"MetaServiceB is doing something with '{action}' and received: '{message}'"


@controller
class MetaTestRunner:
    """使用元类的控制器"""
    
    # 依赖注入
    serviceA: MetaServiceA
    serviceB: MetaServiceB
    
    def __init__(self):
        print("MetaTestRunner controller initialized")
    
    def initialize(self):
        """控制器的初始化逻辑，由元类自动调用"""
        print("\n=== Running Meta Tests ===")
        
        # 测试ServiceA
        message_from_a = self.serviceA.do_something()
        print(f"MetaTestRunner received from ServiceA: '{message_from_a}'")
        
        # 测试ServiceB
        message_from_b = self.serviceB.do_something_with_a("Message from MetaTestRunner")
        print(f"MetaTestRunner received from ServiceB: '{message_from_b}'")
        
        print("=== Meta Tests Finished ===\n")


def run_meta_example():
    """运行元类架构示例"""
    print("\n🚀 Starting Meta-Class Architecture Demo\n")
    
    # 首先实例化所有服务
    meta_container.auto_wire_services()
    
    # 然后实例化所有控制器（此时服务已可用）
    meta_container.auto_wire_controllers()
    
    print("\n✅ Meta-Class Architecture Demo Complete\n")


if __name__ == "__main__":
    run_meta_example()