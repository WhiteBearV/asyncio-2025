from flask import Flask, render_template, request

# สร้างอินสแตนซ์แอปพลิเคชัน Flask
app = Flask(__name__)

# กำหนดเส้นทางหน้าแรก (URL ราก "/")
@app.route("/")
def home():
    # แสดงผลเทมเพลต HTML และส่งค่า name เริ่มต้นเป็น "World"
    return render_template("index.html", name="World")

# กำหนดเส้นทาง /hello ซึ่งรับคำขอ GET จากฟอร์ม
@app.route("/hello", methods=["GET"])
def hello():
    # รับพารามิเตอร์ 'name' จาก query string ของ URL (เช่น ?name=Alice)
    # ถ้าไม่มีการส่งชื่อมา จะใช้ค่าเริ่มต้นเป็น "World"
    name = request.args.get("name", "World")
    # แสดงผลเทมเพลตเดิมโดยส่งชื่อที่ผู้ใช้กรอกมา
    return render_template("index.html", name=name)

# รันแอปถ้าไฟล์นี้ถูกเรียกใช้งานโดยตรง
if __name__ == "__main__":
    # เริ่มเซิร์ฟเวอร์สำหรับพัฒนา บนพอร์ต 50000 พร้อมเปิดโหมด debug
    app.run(debug=True, port=50000)
