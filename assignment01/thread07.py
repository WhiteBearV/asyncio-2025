import concurrent.futures
import logging
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
    return f"Result from thread {name}"

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks and collect futures
        futures = [executor.submit(thread_function, i) for i in range(3)]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            logging.info("Main: got result: %s", result)

    finish = time.perf_counter()
    logging.info("Main: all done in %.2f seconds", finish - start)
