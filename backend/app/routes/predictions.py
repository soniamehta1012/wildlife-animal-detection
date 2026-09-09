from flask import Blueprint, jsonify

# prediction routes - stubs for now.
# upload + running the yolo model comes in Core APIs and Model Integration.
# for now just reserving the endpoints.

predictions_bp = Blueprint("predictions", __name__)


@predictions_bp.post("/")
def upload_and_predict():
    # will take an image, run the model and save + return detections
    return jsonify({"message": "predict not implemented yet"}), 501


@predictions_bp.get("/")
def history():
    # will return the logged in user's past predictions
    return jsonify({"message": "history not implemented yet"}), 501
