from time import sleep
import requests
import random

import src.speech_to_text.task_queue as task_queue

if __name__ == "__main__":
    # p = {'x':random.randrange(1,10000000)}
    # r = requests.get('http://localhost:5000/test', params = p)
    # print(r.json())
    # gto = r.json()['goto']
    # print(gto)
    # r2 = requests.get(f"http://localhost:5000/test/result/{gto}")
    # print(r2.json())

    res = task_queue.process.delay(5)
    print(res)
    print(res.ready())
    print(res.status)
    print(res.backend)

    sleep(4)

    print(res)
    print(res.ready())
    print(res.status)
    print(res.backend)