class PlatformProductFormat:
    def __init__(self, id: str, name: str, platform_id: str, description: str,
                 title: str, price: str, pm_restaurant_id: str, options: list, status: bool):
        self.id = id
        self.name = name
        self.platform_id = platform_id
        self.description = description
        self.title = title
        self.price = price
        self.pm_restaurant_id = pm_restaurant_id
        self.options = options
        self.status = status


class PlatformProductOptionFormat:
    def __init__(self, id: str, type: str, name: str, description: str,
                 price: str, title: str):
        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.price = price
        self.title = title

