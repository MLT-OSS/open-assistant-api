import logging

from app.libs.bson.objectid import ObjectId

if __name__ == "__main__":
    random_original = ObjectId()

    index = 0
    while index < 10:
        logging.info(ObjectId())
        index = index + 1
