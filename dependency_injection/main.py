from dependency_injection.container import IocContainer
from dependency_injection.scanner import scanServices
from dependency_injection.decorators import service

@service()
class ServiceA:
    def __init__(self):
        self.message = "This is a message from ServiceA"

    def do_something(self):
        return "ServiceA is doing something"

    def get_message(self):
        return self.message

@service()
class ServiceB:
    serviceA: ServiceA

    def do_something_with_a(self, message):
        action = self.serviceA.do_something()
        return f"ServiceB is doing something with '{action}' and received the message: '{message}'"

if __name__ == "__main__":
    container = IocContainer()
    scanServices(container, 'dependency_injection')

    # Inject dependencies
    for serviceInstance in container.getAllServices().values():
        container.injectDependencies(serviceInstance)

    serviceB_instance = container.get('serviceB')
    print(serviceB_instance.do_something_with_a("A message for B"))