# Wildlife Backend

Backend for the project "Image Based Classification of Wildlife Animals".
Built with Flask + MongoDB.

## Folder structure

```
wildlife-backend/
├── run.py              # start the server -> python run.py
├── requirements.txt
├── .env.example        # copy to .env and add values
└── app/
    ├── __init__.py     # create_app() - builds the flask app
    ├── config.py       # settings from environment variables
    ├── db.py           # mongodb connection
    ├── models/         # database schema
    │   ├── user.py
    │   └── prediction.py
    └── routes/
        ├── health.py       # GET /health
        ├── auth.py         # /api/auth/*  (stubs for now)
        └── predictions.py  # /api/predictions/*  (stubs for now)
```

## Database design

**users**

| field | type | notes |
|-------|------|-------|
| _id | ObjectId | auto |
| name | string | |
| email | string | unique, used to login |
| password | string | stored as hash |
| role | string | user / admin |
| created_at | datetime | |

**predictions**

| field | type | notes |
|-------|------|-------|
| _id | ObjectId | auto |
| user_id | ObjectId | links to users._id |
| image_path | string | uploaded image location |
| detections | array | list of {class_name, confidence, bbox} |
| animal_count | int | total animals detected |
| created_at | datetime | |

Animal class names are not hardcoded. The dataset has 74 classes and we just
store whatever class the trained YOLOv8 model returns.

## How to run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Then open http://localhost:5000/health to check the server is running.
