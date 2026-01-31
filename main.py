import re
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Google Apps Script Web App URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzlWULv-JbOHbHpiiOFnb39Hw_8uRZusR5-Rm1GapuCjRq_I1NSZ3eMfxCPlPXkA3ollQ/exec"


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
    margin: 32px auto;
    background: #fff;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}
h1 {
    text-align: center;
    color: #2e7d32;
    font-size: 22px;
    margin-bottom: 24px;
}
label {
    margin-top: 14px;
    display: block;
    font-weight: 600;
    font-size: 14px;
}
select, input {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    border-radius: 12px;
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
    border-radius: 14px;
}
button:hover {
    background: #388e3c;
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
<select name="schedule" id="schedule" required>
    <option value="">Сонгох</option>
    <option value="mwf">Даваа, Лхагва, Баасан</option>
    <option value="tts">Мягмар, Пүрэв, Бямба</option>
</select>

<label>Цаг</label>
<select name="time" id="time" required>
    <option value="">Сонгох</option>
</select>

<label>Үйлчлүүлэгчийн нэр</label>
<input type="text" name="client" required placeholder="Нэрээ оруулна уу">

<label>Утас (8 оронтой)</label>
<input type="tel" name="phone" pattern="[0-9]{8}" required placeholder="99112233">

<label>Төлбөр (₮)</label>
<input type="number" name="price" required placeholder="Мөнгөн дүн">

<button type="submit">Бүртгэх</button>
</form>
</div>

<script>
const schedule = document.getElementById("schedule");
const time = document.getElementById("time");

const TIMES = {
  mwf: ["6:00","7:00","9:00","12:00","18:00","19:00"],
  tts: ["8:00","9:30","17:30","19:00"]
};

schedule.addEventListener("change", () => {
  time.innerHTML = '<option value="">Сонгох</option>';
  if (!TIMES[schedule.value]) return;
  TIMES[schedule.value].forEach(t => {
    const o = document.createElement("option");
    o.value = t;
    o.textContent = t;
    time.appendChild(o);
  });
});
</script>

</body>
</html>
"""


@app.post("/register", response_class=HTMLResponse)
def register(
    teacher: str = Form(...),
    schedule: str = Form(...),
    time: str = Form(...),
    client: str = Form(...),
    phone: str = Form(...),
    price: int = Form(...)
):
    if not re.fullmatch(r"\d{8}", phone):
        return """
        <div style="text-align:center;margin-top:60px;font-size:18px">
        ❌ Утасны дугаар буруу<br><br>
        <a href="/">Буцах</a>
        </div>
        """
if schedule == "mwf":
    schedule_text = "Даваа, Лхагва, Баасан"
elif schedule == "tts":
    schedule_text = "Мягмар, Пүрэв, Бямба"
else:
    schedule_text = schedule

    payload = {
        "teacher": teacher,
        "schedule": schedule_text,
        "time": time,
        "client": client,
        "phone": phone,
        "price": price
    }

    requests.post(SCRIPT_URL, json=payload, timeout=10)

    return """
    <div style="
        max-width:420px;
        margin:80px auto;
        padding:30px;
        text-align:center;
        font-family:sans-serif;
        background:#e8f5e9;
        border-radius:18px;
        box-shadow:0 10px 30px rgba(0,0,0,0.12)">
        <h2 style="color:#2e7d32">✅ Амжилттай бүртгэгдлээ</h2>
        <a href="/" style="
            display:inline-block;
            margin-top:20px;
            padding:12px 24px;
            background:#43a047;
            color:white;
            text-decoration:none;
            border-radius:12px">
            Буцах
        </a>
    </div>
    """
