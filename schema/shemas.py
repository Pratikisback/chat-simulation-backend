def individual_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "status": todo["status"]
    }



def single_product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": str(product["name"]),
        "price": int(product["price"]),
        "status": str(product["status"])
    }


def product_serializer(products) -> list:
    return [single_product_serializer(product) for product in products]


def list_serial(todos) -> list:
    return [individual_serializer(todo) for todo in todos]