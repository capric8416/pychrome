import time
import threading


stop_flag = False


def print_a():
    while not stop_flag:
        print('a')
        time.sleep(1)

    print("stop print_a")


th = threading.Thread(target=print_a)

th.start()
th.join(2)

stop_flag = True

print("restart")

th.start()
th.join(4)