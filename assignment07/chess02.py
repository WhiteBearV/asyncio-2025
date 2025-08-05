import time  # ใช้สำหรับจับเวลา
from datetime import timedelta  # ใช้แปลงวินาทีเป็นรูปแบบเวลา
import asyncio  # ใช้สำหรับเขียนโปรแกรมแบบ asynchronous

speed = 1000 # ความเร็วในการจำลอง (ค่าที่ใช้คูณเวลาเพื่อให้เห็นผลเร็วขึ้น)
Judit_time = 5/speed # เวลาที่ Judit ใช้ในการเดินแต่ละตา (หน่วยวินาที)
Opponent_time = 55/speed # เวลาที่ฝ่ายตรงข้ามใช้ในการเดินแต่ละตา (หน่วยวินาที)
opponents = 24 # จำนวนฝ่ายตรงข้าม (จำนวนกระดานที่เล่นพร้อมกัน)
move_pairs = 30 # จำนวนคู่ของการเดิน (Judit + Opponent = 1 คู่)

# ฟังก์ชันนี้จำลองการเล่นเกมบนแต่ละกระดานแบบ asynchronous
async def game(x):
    # บันทึกเวลาเริ่มต้นของกระดานนี้
    board_start_time = time.perf_counter()
    for i in range(move_pairs):
        # จำลองการคิดเดินของ Judit โดยใช้ time.sleep (ซึ่งจะ block event loop)
        # หมายเหตุ: ในโค้ดนี้ใช้ time.sleep ซึ่งไม่เหมาะกับ async function เพราะจะหยุด event loop ทั้งหมด
        # ถ้าต้องการให้ทำงานแบบ async จริงๆ ควรใช้ await asyncio.sleep แทน
        time.sleep(Judit_time)
        print(f"BOARD-{x+1} {i+1} Judit made a move with {int(Judit_time*speed)} secs.")
        # ฝ่ายตรงข้ามเดิน โดยใช้ await asyncio.sleep เพื่อไม่ block event loop
        await asyncio.sleep(Opponent_time)
        print(f"BOARD-{x+1} {1+1} Opponent made move with {int (Opponent_time*speed)} secs.")
    # แสดงผลรวมเวลาที่ใช้ในการเล่นกระดานนี้
    print(f"BOARD-{x+1} >>>>>>>>>>>>>>>>> Finished move in {(time.perf_counter() - board_start_time)*speed:.1f} secs.\n")
    return {
        'calculated_board_time': (time.perf_counter() - board_start_time)*speed
    }

# ฟังก์ชัน main สำหรับสร้าง task ของแต่ละกระดานและรันพร้อมกันแบบ async
async def main():
    tasks = []
    for i in range(opponents):
        tasks += [game(i)]  # สร้าง task สำหรับแต่ละกระดาน
    await asyncio.gather(*tasks)  # รันทุก task พร้อมกัน
    print(f"Board exhibition finished for {opponents} opponents in {timedelta(seconds=speed*round(time.perf_counter() - start_time))} hr.")

if __name__ == "__main__":
    print(f"Number of games: {opponents} games.")
    print(f"Number of move: {move_pairs} pairs.")
    start_time = time.perf_counter()  # บันทึกเวลาเริ่มต้น
    asyncio.run(main())  # รัน main แบบ async
    print(f"Finished in {round(time.perf_counter() - start_time)} secs.")
