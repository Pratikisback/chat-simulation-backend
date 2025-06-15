from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str=Field(..., min_length=3, max_length=24)
    price: int
    status: str