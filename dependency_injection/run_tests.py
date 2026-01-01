from dependency_injection.container import IocContainer
from dependency_injection.scanner import scanServices

if __name__ == "__main__":
    container = IocContainer()
    scanServices(container, 'dependency_injection')