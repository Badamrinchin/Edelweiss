import re
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzlWULv-JbOHbHpiiOFnb39Hw_8uRZusR5-Rm1GapuCjRq_I1NSZ3eMfxCPlPXkA3ollQ/exec"


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
      <head>
        <title>Edelweiss Yoga Center – Бүртгэл</title>
      </head>
      <body>
        <h2>Edelweiss Yoga Center – Бүртгэл</h2>

        <form method="post" action="/register">
          <p>Багш</p>
          <input name="teacher" required>

          <p>Өдөр</p>
          <input name="schedule" required>

          <p>Цаг</p>
          <input name="time" required>

          <p>Үйлчлүүлэгчийн нэр</p>
          <input name="client" required>

          <p>Утас (8 оронтой)</p>
          <input name="phone" required>

          <p>Төлбөр</p>
          <input name="price" type="number" required>

          <br><br>
          <button type="submit">Бүртгэх</button>
        </form>
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
        return "❌ Утасны дугаар буруу <a href='/'>Буцах</a>"

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
