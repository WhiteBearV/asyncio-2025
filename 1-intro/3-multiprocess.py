import time
from multiprocessing import Process
from datetime import datetime

def make_burger(student_id):

    start = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] เริ่มทำเบอร์เกอร์ให้นักเรียนคนที่ {student_id} เริ่มทำที่เวลา {datetime.now().strftime('%H:%M:%S')}")
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 1. ทอดเบอร์เกอร์...")
    time.sleep(5)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 2. ทอดไก่...")
    time.sleep(5)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 3. ใส่ผักและชีส...")
    time.sleep(5)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 4. ห่อเบอร์เกอร์...")
    time.sleep(5)
    end = time.time()


    print(f"[{datetime.now().strftime('%H:%M:%S')}] เสร็จแล้ว! เบอร์เกอร์ของนักเรียนคนที่ {student_id}และเวลาที่เสร็จคือ {end - start:.6f}")

def main():
    start = time.time()
    
    processes = []
    for i in range(1, 6):
        p = Process(target=make_burger, args=(i,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    end = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] รวมเวลาทั้งหมด: {end - start:.2f} วินาที")

if __name__ == "__main__":
    main()
