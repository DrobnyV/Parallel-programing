import threading
import time
from queue import Queue

from color import Color
from examples.simulation import Simulation


class Messages(Simulation):
    def run(self):
        def producer(queue):
            for i in range(5):
                queue.put(f"Zpráva {i}")
                print(f"Producent odeslal: Zpráva {i}")
                time.sleep(1)

        def consumer(queue):
            while not queue.empty() or threading.current_thread().is_alive():
                if not queue.empty():
                    msg = queue.get()
                    print(f"Konzument přijal: {msg}")

        queue = Queue()
        producer_thread = threading.Thread(target=producer, args=(queue,))
        consumer_thread = threading.Thread(target=consumer, args=(queue,))
        consumer_thread.do_run = True

        producer_thread.start()
        consumer_thread.start()
        producer_thread.join()
        consumer_thread.do_run = False
        consumer_thread.join()

    def show_code(self):
        print(f"""
        {Color.GREEN}# Simulation of messaging{Color.RESET}
                def producer(queue):
            for i in range(5):
                queue.put("Zpráva" + str(i))
                print("Producent odeslal: Zpráva " + str(i))
                time.sleep(1)

        def consumer(queue):
            while not queue.empty() or threading.current_thread().is_alive():
                if not queue.empty():
                    msg = queue.get()
                    print(f"Konzument přijal: "+ str(msg))

        queue = Queue()
        producer_thread = threading.Thread(target=producer, args=(queue,))
        consumer_thread = threading.Thread(target=consumer, args=(queue,))
        consumer_thread.do_run = True

        producer_thread.start()
        consumer_thread.start()
        producer_thread.join()
        consumer_thread.do_run = False
        consumer_thread.join()
        """)