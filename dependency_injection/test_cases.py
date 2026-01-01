from dependency_injection.container import IocContainer
from dependency_injection.scanner import scanServices
from dependency_injection.decorators import controller
from dependency_injection.main import ServiceA, ServiceB

@controller()
class TestRunner:
    serviceA: ServiceA
    serviceB: ServiceB

    def __init__(self):
        pass

    def __post_init__(self):
        print("--- Running Tests ---")
        message_from_a = self.serviceA.do_something()
        print(f"TestRunner received from ServiceA: '{message_from_a}'")

        message_from_b = self.serviceB.do_something_with_a("This is a message from ServiceA")
        print(f"TestRunner received from ServiceB: '{message_from_b}'")
        print("--- Tests Finished ---")

# Setup container and scan for services
container = IocContainer()
scanServices(container, 'dependency_injection')

# Manually inject dependencies for all services
for service_instance in container.getAllServices().values():
    container.injectDependencies(service_instance)

# Get the TestRunner instance and run tests
test_runner = container.get('testRunner')
if test_runner:
    test_runner.run_tests()