import logging
import threading
import time

def thread_function(name, delay):
    logging.info("Thread %s: starting (delay=%s)", name, delay)
    time.sleep(delay)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    start_time = time.perf_counter()

    threads = []

    # เริ่มสร้างและรัน threads พร้อมเวลาหน่วงที่ต่างกัน
    for i in range(3):
        delay = (i + 1) * 1.5  # 1.5s, 3s, 4.5s
        logging.info("Main    : create and start thread %d with delay %.1f", i, delay)
        x = threading.Thread(target=thread_function, args=(i, delay))
        threads.append(x)
        x.start()

    for i, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d", i)
        thread.join()
        logging.info("Main    : thread %d done", i)

    end_time = time.perf_counter()
    logging.info("Main    : all done in %.2f seconds", end_time - start_time)
