import re
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Google Apps Script Web App URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzlWULv-JbOHbHpiiOFnb39Hw_8uRZusR5-Rm1GapuCjRq_I1NSZ3eMfxCPlPXkA3ollQ/exec"


# =========================
# INDEX PAGE (FORM)
# =========================
@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html lang="mn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edelweiss Yoga Center – Бүртгэл</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            padding: 20px;
        }
        .card {
            max-width: 420px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            font-weight: bold;
            display: block;
            margin-top: 12px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        button {
            background: #2e7d32;
            color: white;
            font-size: 16px;
            border: none;
            margin-top: 20px;
        }
        button:hover {
            background: #256628;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Edelweiss Yoga Center – Бүртгэл</h2>

        <form method="post" action="/register">

            <label>Багш</label>
            <select name="teacher" required>
                <option value="Өлзийжаргал">Өлзийжаргал</option>
                <option value="Өлзийдэлгэр">Өлзийдэлгэр</option>
                <option value="Өлзийбаяр">Өлзийбаяр</option>
                <option value="Тунгалаг">Тунгалаг</option>
            </select>

            <label>Өдрийн сонголт</label>
            <select name="schedule" required>
                <option value="Даваа, Лхагва, Баасан">Даваа, Лхагва, Баасан</option>
                <option value="Мягмар, Пүрэв, Бямба">Мягмар, Пүрэв, Бямба</option>
            </select>

            <label>Цаг</label>
            <select name="time" required>
                <option value="6am">6am</option>
                <option value="7am">7am</option>
                <option value="9am">9am</option>
                <option value="12pm">12pm</option>
                <option value="6pm">6pm</option>
                <option value="7pm">7pm</option>
            </select>

            <label>Үйлчлүүлэгчийн овог нэр</label>
            <input type="text" name="client" required>

            <label>Утасны дугаар (8 оронтой)</label>
            <input type="text" name="phone" maxlength="8" required>

            <label>Төлбөр (₮)</label>
            <input type="number" name="price" required>

            <button type="submit">Бүртгэх</button>
        </form>
    </div>
</body>
</html>
"""


# =========================
# REGISTER → GOOGLE SHEETS
# =========================
@app.post("/register", response_class=HTMLResponse)
def register(
    teacher: str = Form(...),
    schedule: str = Form(...),
    time: str = Form(...),
    client: str = Form(...),
    phone: str = Form(...),
    price: int = Form(...)
):
    # phone validation (8 digits)
    if not re.fullmatch(r"\d{8}$", phone):
        return "<h3>❌ Утасны дугаар буруу</h3><a href='/'>Буцах</a>"

    payload = {
        "teacher": teacher,
        "schedule": schedule,
        "time": time,
        "client": client,
        "phone": phone,
        "price": price
    }

    try:
        r = requests.post(SCRIPT_URL, json=payload, timeout=10)
        print("Apps Script response:", r.text)
    except Exception as e:
        print("Apps Script error:", e)
        return "<h3>❌ Серверийн алдаа</h3><a href='/'>Буцах</a>"

    return "<h2>✅ Амжилттай бүртгэгдлээ</h2><a href='/'>Буцах</a>"
