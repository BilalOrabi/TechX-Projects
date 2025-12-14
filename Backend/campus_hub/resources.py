class Resource:
    def __init__(self, rid: str, rtype: str):
        self.id = rid
        self.type = rtype
        self.available = True

    def allocate_to(self, student):
        if not self.available:
            raise RuntimeError("Resource unavailable")
        self.available = False

    def needs_resource(self):
        return self.available

    def __repr__(self):
        status = "available" if self.available else "allocated"
        return f"Resource(id={self.id}, type={self.type}, status={status})"


class ResourceCatalog:
    def __init__(self):
        self.items = []

    def add(self, resource):
        self.items.append(resource)

    def allocate(self, consumer):
        for r in self.items:
            if r.available and consumer.needs_resource():
                return r
        return None

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)
