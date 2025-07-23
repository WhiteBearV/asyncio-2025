import time
import requests as requests
from flask import Flask, render_template

# นำเข้า blueprint จากโฟลเดอร์ sync และ async route
from sync_routes.routes import sync_bp
from async_routes.routes import async_bp

# สร้างแอป Flask
app = Flask(__name__)

# ลงทะเบียน blueprint สำหรับ sync และ async โดยใช้ URL prefix ที่ต่างกัน
app.register_blueprint(sync_bp, url_prefix="/sync")
app.register_blueprint(async_bp, url_prefix="/async")

# กำหนดค่าคงที่โดยใช้ config dictionary ของ Flask
app.config["NUMBER_OF_POKEMON"] = 1000  # ใช้ควบคุมจำนวน XKCD ที่จะดึงข้อมูล

# กำหนด route หลัก
@app.route('/')
def index():
    start_time = time.perf_counter()  # เริ่มจับเวลา
    end_time = time.perf_counter()    # จับเวลาสิ้นสุด (ทันทีเพราะไม่มี logic)

    # render template base.html พร้อมข้อมูลเวลาและรายการว่าง
    return render_template('base.html'
                           , title="Flask App Flask"
                           , heading="Pokemon Flask"
                           , xkcds=[]   # ตัวแทนสำหรับ XKCD หรือรายการอื่น
                           , end_time=end_time, start_time=start_time)

# รันแอปพลิเคชัน
if __name__ == '__main__':
    app.run(debug=True, port=50000)