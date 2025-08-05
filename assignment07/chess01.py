import time
from datetime import timedelta

# กำหนดความเร็วในการเล่น (เช่น 1000 หมายถึง 1 วินาที = 1/1000 วินาที)
speed = 1000
# เวลาที่ Judit ใช้ในการเดินหมากแต่ละตา (5 วินาที หารด้วย speed)
Judit_time = 5 / speed
# เวลาที่คู่แข่งใช้ในการเดินหมากแต่ละตา (55 วินาที หารด้วย speed)
Opponent_time = 55 / speed
# จำนวนคู่แข่ง หรือจำนวนเกมที่เล่น
Opponent = 24
# จำนวนคู่ของการเดินหมาก (Judit และคู่แข่งเดินหมากคนละ 1 ครั้งต่อคู่)
move_pairs = 30

# (5(Judit_time)+55(Opponent_time))*30(move_pairs) = 1800 second
# หมายเหตุ: สูตรนี้ใช้คำนวณเวลารวมในการเล่นบนกระดานเดียว

def game(x):
    # ฟังก์ชันนี้จำลองการเล่นบนกระดานที่ x
    board_start_time = time.perf_counter()  # เวลาที่เริ่มเล่นกระดานนี้
    calculated_board_start_time = 0         # ตัวแปรเก็บเวลาที่คำนวณเอง
    for i in range(move_pairs): 
        # Judit เดินหมาก ใช้เวลา Judit_time
        time.sleep(Judit_time)
        calculated_board_start_time = calculated_board_start_time + Judit_time
        print(f"BOARD-{x+1} {i+1} Judit made a nove with {int(Judit_time*speed)} secs.")
        # คู่แข่งเดินหมาก ใช้เวลา Opponent_time
        time.sleep(Opponent_time)
        print(f"BOARD-{x+1} {i+1} Opponent sade sove wit {int(Opponent_time*speed)} secs.")
        calculated_board_start_time = calculated_board_start_time + Opponent_time
    # แสดงผลเวลาที่ใช้จริงและเวลาที่คำนวณได้
    print(f"B0ARD- {x+1} ->>>>>>>>>>>>> Finished Bove in {(time.perf_counter() - board_start_time)*speed:.1f} secs")
    print(f"BOARD-{x+1} ->>>>>>>>>>>>>> Finished move in {calculated_board_start_time *speed:.1f} secs(calculated) \n")
    # คืนค่าเวลาที่ใช้จริงและเวลาที่คำนวณได้
    return [(time.perf_counter() - board_start_time), calculated_board_start_time]


if __name__ == "__main__":
    # แสดงจำนวนกระดานและจำนวนคู่ของการเดินหมาก
    print("Number of boards: , {Opponent} game")
    print("Nomber of move pairs: , {move_pairs} pairs")
    start_time = time.perf_counter()  # เวลาที่เริ่มต้นทั้งหมด

    board_times = 0
    calculated_board_times = 0
    # วนลูปเล่นบนแต่ละกระดาน
    for board in range(Opponent):
        board_times += game(board)[0]              # สะสมเวลาที่ใช้จริง
        calculated_board_times += game(board)[1]   # สะสมเวลาที่คำนวณได้

    # แสดงผลเวลารวมที่ใช้จริงและเวลาที่คำนวณได้ทั้งหมด
    print(f"Board exhibition finished for {Opponent} opponents in {timedelta(seconds=round(board_times*speed))} hr.")
    print(f"Board exhibition finished for {Opponent} opponents in {timedelta(seconds=round(calculated_board_times*speed))} hr. (calculated)")
    print(f"Finished in {round(time.perf_counter() - start_time)} secs.")

