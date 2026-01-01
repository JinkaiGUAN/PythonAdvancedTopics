def to_camel_case(name):
    return name[0].lower() + name[1:]

def service(name=None):
    def decorator(cls):
        service_name = name if name else to_camel_case(cls.__name__)
        cls.serviceName = service_name
        return cls
    return decorator

def controller():
    def decorator(cls):
        cls.is_controller = True
        return cls
    return decorator