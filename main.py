import re
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzlWULv-JbOHbHpiiOFnb39Hw_8uRZusR5-Rm1GapuCjRq_I1NSZ3eMfxCPlPXkA3ollQ/exec"

index_html = """
<!DOCTYPE html>
<html lang="mn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edelweiss Yoga Center – Бүртгэл</title>
</head>
<body>
    <h2>Edelweiss Yoga Center – Бүртгэл</h2>
    <form method="post" action="/register">
        <label>Багш</label><br>
        <select name="teacher">
            <option>Өлзийжаргал</option>
            <option>Өлзийдэлгэр</option>
            <option>Өлзийбаяр</option>
            <option>Тунгалаг</option>
        </select><br><br>

        <label>Өдөр</label><br>
        <input name="schedule"><br><br>

        <label>Цаг</label><br>
        <input name="time"><br><br>

        <label>Нэр</label><br>
        <input name="client"><br><br>

        <label>Утас</label><br>
        <input name="phone"><br><br>

        <label>Төлбөр</label><br>
        <input name="price" type="number"><br><br>

        <button type="submit">Бүртгэх</button>
    </form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return index_html


@app.post("/register", response_class=HTMLResponse)
def register(
    teacher: str = Form(...),
    schedule: str = Form(...),
    time: str = Form(...),
    client: str = Form(...),
    phone: str = Form(...),
    price: int = Form(...)
):
    if not re.fullmatch(r"\d{8}$", phone):
        return "❌ Утас буруу <a href='/'>Буцах</a>"

    payload = {
        "teacher": teacher,
        "schedule": schedule,
        "time": time,
        "client": client,
        "phone": phone,
        "price": price
    }

    requests.post(SCRIPT_URL, json=payload, timeout=10)

    return "✅ Амжилттай бүртгэгдлээ <a href='/'>Буцах</a>"
