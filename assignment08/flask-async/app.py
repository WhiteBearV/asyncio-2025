from flask import Flask, render_template, request
import asyncio  # ใช้สำหรับงานแบบอะซิงโครนัส เช่น การหน่วงเวลา หรือ I/O แบบอะซิงโครนัส

# สร้างแอปพลิเคชัน Flask
app = Flask(__name__)

# กำหนด route หลัก ("/") เป็นฟังก์ชันแบบอะซิงโครนัส
@app.route("/")
async def index():
    # แสดงผลเทมเพลต HTML โดยใช้ค่าเริ่มต้นของ name เป็น "World"
    # หมายเหตุ: render_template เป็นฟังก์ชันซิงโครนัส ไม่ควรใช้ await
    return render_template("index.html", name="World")

# กำหนด route /hello เพื่อรับคำขอ GET แบบอะซิงโครนัส
@app.route("/hello")
async def hello():
    # ดึงค่าจาก query string ของ URL (?name=YourName)
    # ถ้าไม่มี name ให้ใช้ค่าเริ่มต้นเป็น "World"
    name = request.args.get("name", "World")
    
    # จำลองงาน I/O แบบอะซิงโครนัส (เช่น รอข้อมูลจากฐานข้อมูลหรือ API)
    await asyncio.sleep(1)  # จำลองงาน async
    # ส่งคืนเทมเพลตพร้อมกับชื่อที่รับมา
    return render_template("index.html", name=name)

# รันแอปเมื่อสคริปต์นี้ถูกเรียกใช้งานโดยตรง
if __name__ == "__main__":
    # เริ่มเซิร์ฟเวอร์ Flask ในโหมด debug ที่พอร์ต 50000
    app.run(debug=True, port=50000)
