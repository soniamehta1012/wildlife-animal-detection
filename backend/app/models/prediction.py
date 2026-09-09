from datetime import datetime

from app.db import get_db

# predictions collection.
# every time a user uploads an image and the model runs, we save one document
# here with the detected animals.
#
# shape:
# {
#   "_id": ObjectId,
#   "user_id": ObjectId,       -> which user uploaded (links to users._id)
#   "image_path": str,         -> where the uploaded image is saved
#   "detections": [            -> one item per animal found
#       {
#          "class_name": str,   -> animal name from the model (74 classes)
#          "confidence": float, -> 0 to 1
#          "bbox": [x1, y1, x2, y2]
#       },
#       ...
#   ],
#   "animal_count": int,
#   "created_at": datetime
# }
#
# note: we do NOT hardcode animal names here. whatever class the trained
# yolo model returns is what we store, so it works for all 74 classes.


def predictions():
    return get_db()["predictions"]


def create_indexes():
    # index on user_id + created_at so showing a user's history (newest first)
    # is fast
    predictions().create_index([("user_id", 1), ("created_at", -1)])


def make_prediction(user_id, image_path, detections):
    return {
        "user_id": user_id,
        "image_path": image_path,
        "detections": detections,
        "animal_count": len(detections),
        "created_at": datetime.utcnow(),
    }
