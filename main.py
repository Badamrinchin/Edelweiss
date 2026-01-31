import re
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

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
    margin-botto
