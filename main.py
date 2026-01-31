import re
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzlWULv-JbOHbHpiiOFnb39Hw_8uRZusR5-Rm1GapuCjRq_I1NSZ3eMfxCPlPXkA3ollQ/exec"


# =========================
# INDEX PAGE
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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    margin: 0;
    padding: 0;
}
.container {
    max-width: 420px;
    margin: 40px auto;
    background: #ffffff;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
h1 {
    text-align: center;
    color: #2e7d32;
    margin-bottom: 24px;
    font-size: 22px;
}
label {
    display: block;
    margin-top: 14px;
    font-weight: 600;
    color: #333;
    font-size: 14px;
}
select, input {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    border-radius: 10px;
    border: 1px solid #ccc;
    font-size: 16px;
}
button {
    margin-top: 24px;
    width: 100%;
    padding: 14px;
    background: #43a047;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 12px;
}
.note {
    text-align: center;
    margin-top: 12px;
    font-size: 12px;
    color: #777;
}
</style>
</head>

<body>
<div class="container">
<h1>Edelweiss Yoga Center – Бүртгэл</h1>

<form method="post" action="/register">

<label>Багш</label>
<select name="teacher" required>
<option value="">Сонгох</option>
<option>Өлзийжаргал</option>
<option>Өлзийдэлгэр</option>
<option>Өлзийбаяр</option>
<option>Тунгалаг</option>
</select>

<label>Өдөр</label>
<select name="schedule" required>
<option value="">Сонгох</option>
<option>Даваа, Лхагва, Баасан</option>
<option>Мягмар, Пүрэв, Бямба</option>
</select>

<label>Цаг</label>
<select name="time" required>
<option value="">Сонгох</option>
<option>6:00</option>
<option>7:00</option>
<option>9:00</option>
<option>12:00</option>
<option>17:30</option>
<option>18:00</option>
<option>19:00</option>
</select>

<label>Үйлчлүүлэгчийн нэр</label>
<input type="text" name="client" required>

<label>Утас (8 оронтой)</label>
<input type="tel" name="phone" pattern="[0-9]{8}" required>

<label>Төлбөр (₮)</label>
<input type="number" name="price" required>

<button type="submit">Бүртгэх</button>
</form>

<div class="note">📱 Гар утсанд тохирсон загвар</div>
</div>
</body>
</html>
"""


# =========================
# REGISTER ENDPOINT
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
    # 1️⃣ Утас шалгах
    if not re.fullmatch(r"\d{8}", phone):
        return "❌ Утасны дугаар буруу <a href='/'>Буцах</a>"

    # 2️⃣ Өдөр–цагийн зөвшөөрөгдсөн логик
    VALID_TIMES = {
        "Даваа, Лхагва, Баасан": ["6:00", "7:00", "9:00", "12:00", "18:00", "19:00"],
        "Мягмар, Пүрэв, Бямба": ["8:00", "9:30", "17:30", "19:00"]
    }

    if time not in VALID_TIMES.get(schedule, []):
        return "❌ Сонгосон өдөрт тохирохгүй цаг байна <a href='/'>Буцах</a>"

    # 3️⃣ Google Sheets рүү илгээх payload
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
