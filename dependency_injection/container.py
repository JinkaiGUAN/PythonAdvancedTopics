import inspect

def to_camel_case(name):
    return name[0].lower() + name[1:]

class IocContainer:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services.get(name)

    def __getitem__(self, name):
        return self.get(name)

    def getAllServices(self):
        return self._services

    def injectDependencies(self, instance):
        if hasattr(instance.__class__, '__annotations__'):
            for name, type_hint in instance.__class__.__annotations__.items():
                service_name = to_camel_case(type_hint.__name__)
                dependency = self.get(service_name)
                if dependency:
                    setattr(instance, name, dependency)