
# Edelweiss Yoga Center – Бүртгэл

FastAPI ашигласан иогийн төвийн бүртгэлийн вэб сайт.

## Локал ажиллуулах
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Browser:
http://127.0.0.1:8000

## Render дээр байршуулах
Start command:
```
uvicorn main:app --host 0.0.0.0 --port 10000
```
