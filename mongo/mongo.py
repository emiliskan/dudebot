from mongo import db

def add_values(collection, values):
    collection = db[collection]
    collection.insert_many(values)


def add_value(collection, value):
    collection = db[collection]
    collection.insert_one(value)


def update_value(collection, query_elements, new_values):
    collection = db[collection]
    collection.update_one(query_elements, {'$set': new_values})


def get_values(collection, elements={}):
    collection = db[collection]

    results = collection.find(elements)
    return [r for r in results]


def clear_values(collection):
    collection = db[collection]
    collection.delete_many({})
    return True
