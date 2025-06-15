from pymongo import MongoClient

client = MongoClient("mongodb+srv://PratikChavan:pratik4321@cluster0.axzgan9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.todos
todos_collection = db["todos"]
product_collection = db["products"]

