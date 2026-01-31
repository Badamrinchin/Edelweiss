
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import openpyxl, os, re
from datetime import datetime
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzlWULv-JbOHbHpiiOFnb39Hw_8uRZusR5-Rm1GapuCjRq_I1NSZ3eMfxCPlPXkA3ollQ/exec"


app = FastAPI()
EXCEL_FILE = "Бүртгэл.xlsx"

if not os.path.exists(EXCEL_FILE):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Registrations"
    ws.append(["Огноо","Багш","Өдөр","Цаг","Үйлчлүүлэгч","Утас","Төлбөр (₮)"])
    wb.save(EXCEL_FILE)

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
body{margin:0;background:#ecfdf5;display:flex;justify-content:center;align-items:center;font-family:Arial}
.card{background:#fff;width:100%;max-width:430px;margin:16px;padding:24px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.12)}
h1{text-align:center;color:#065f46}
label{font-weight:bold;margin-top:12px;display:block}
select,input{width:100%;padding:10px;border-radius:8px;border:1px solid #d1d5db;margin-top:4px}
button{margin-top:20px;width:100%;padding:14px;background:#16a34a;color:white;border:none;border-radius:10px;font-size:16px;font-weight:bold}
</style>
<script>
function updateTimes(){
  const day = document.getElementById("schedule").value;
  const time = document.getElementById("time");
  time.innerHTML = "";
  let options = [];
  if(day === "DLB"){
    options = ["6am","7am","9am","12pm","6pm","7pm"];
  } else if(day === "MPB"){
    options = ["8am","9:30am","5:30pm","7pm"];
  }
  options.forEach(t=>{
    let opt=document.createElement("option");
    opt.value=t; opt.text=t;
    time.appendChild(opt);
  });
}
</script>
</head>
<body>
<div class="card">
<h1>Edelweiss Yoga Center – Бүртгэл</h1>
<form method="post" action="/register">
<label>Багшийн нэр</label>
<select name="teacher" required>
<option>Өлзийжаргал</option>
<option>Өлзийдэлгэр</option>
<option>Өлзийбаяр</option>
<option>Тунгалаг</option>
</select>

<label>Өдрийн сонголт</label>
<select name="schedule" id="schedule" onchange="updateTimes()" required>
<option value="">Сонгоно уу</option>
<option value="DLB">Даваа, Лхагва, Баасан</option>
<option value="MPB">Мягмар, Пүрэв, Бямба</option>
</select>

<label>Цаг</label>
<select name="time" id="time" required></select>

<label>Үйлчлүүлэгчийн овог нэр</label>
<input type="text" name="client" required>

<label>Утас (8 оронтой)</label>
<input type="text" name="phone" pattern="[0-9]{8}" maxlength="8" required>

<label>Төлбөр</label>
<div style="display:flex;align-items:center">
<input type="number" name="price" required><span style="margin-left:6px;font-weight:bold">₮</span>
</div>

<button type="submit">Бүртгэх</button>
</form>
</div>
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
        return "<h3>❌ Утас буруу</h3><a href='/'>Буцах</a>"

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

    return "<h2>✅ Амжилттай бүртгэгдлээ</h2><a href='/'>Буцах</a>"
