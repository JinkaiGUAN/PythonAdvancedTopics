import os
import importlib
import inspect

# Track processed modules to prevent duplicate scanning
_processed_modules = set()

def scanServices(container, package_or_module):
    if isinstance(package_or_module, str):
        package = importlib.import_module(package_or_module)
    else:
        package = package_or_module

    # Skip if this module/package has already been processed
    if package.__name__ in _processed_modules:
        return
    _processed_modules.add(package.__name__)

    instances = []
    controllers = []

    modules_to_scan = []
    if hasattr(package, '__path__'):  # It's a package
        for moduleName in os.listdir(os.path.dirname(package.__file__)):
            if moduleName.endswith('.py') and moduleName != '__init__.py':
                try:
                    module = importlib.import_module(f'{package.__name__}.{moduleName[:-3]}')
                    modules_to_scan.append(module)
                except ImportError:
                    # Skip modules that can't be imported
                    continue
    else:  # It's a module
        modules_to_scan.append(package)

    # First pass: discover and instantiate all services and controllers
    for module in modules_to_scan:
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if hasattr(cls, 'serviceName'):
                instance = cls()
                serviceName = getattr(cls, 'serviceName')
                container.register(serviceName, instance)
                instances.append(instance)
            elif hasattr(cls, 'is_controller'):
                instance = cls()
                instances.append(instance)
                controllers.append(instance)

    # Second pass: inject dependencies for all instances
    for instance in instances:
        container.injectDependencies(instance)

    # Third pass: run post-init for controllers
    for controller_instance in controllers:
        if hasattr(controller_instance, '__post_init__'):
            controller_instance.__post_init__()