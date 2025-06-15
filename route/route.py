from fastapi import APIRouter
from schema.shemas import list_serial, product_serializer
from config.database import todos_collection, product_collection
from models.todos import Todo
from models.products import Product
router = APIRouter()

# Get call

@router.get("/")
async def get_todos():
    todos = list_serial(todos_collection.find())
    return todos


@router.post("/api/todo")
async def add_todo(todo: Todo):
    res =  todos_collection.insert_one(dict(todo))
    print(res)



@router.post("/api/add-products")
async def add_products(product: Product):
    res = product_collection.insert_one(dict(product))
    print(res)