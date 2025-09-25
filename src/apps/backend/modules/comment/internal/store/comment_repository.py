from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.comment.internal.store.comment_model import CommentModel
from modules.logger.logger import Logger


class CommentRepository(ApplicationRepository):
    collection_name = CommentModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index([("task_id", 1)], name="task_id_index")
        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["task_id", "account_id", "text", "created_at", "updated_at"],
                    "properties": {
                        "task_id": {"bsonType": "string"},
                        "account_id": {"bsonType": "string"},
                        "text": {"bsonType": "string"},
                        "created_at": {"bsonType": "date"},
                        "updated_at": {"bsonType": "date"},
                    },
                }
            },
            "validationLevel": "strict",
        }
        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(
                    cls.collection_name, validator=add_validation_command["validator"]
                )
            else:
                Logger.error(message=f"OperationFailure occurred for collection comments: {e.details}")
        return True
