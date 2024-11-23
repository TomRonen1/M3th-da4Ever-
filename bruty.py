import requests
import random
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()

TIME_SLEEP_FOR_BOT_DETECTION = 5 # seconds
PRINT_LOGS = False
THREAD_TRANSMITS_TOTAL = 10000
THREAD_TRANSMITS_DIVISION = 500
MAX_WORKERS = 10
STATUS_CODE_OK = 200
THREAD_REPEAT_COUNT = 10

def print_logs(content):
    if PRINT_LOGS:
        print(content)  

def sleep_random():
    value = random.randint(1, 10) / 10000
    sleep(value)
    print_logs(f"slept for {value} seconds")
    return value


# Define the URL and headers
url = "Add your url here"
headers = {
    'Host': 'Add Host here',
    'Cookie': ('Add Cookies here'),
    'Sec-Ch-Ua': '',
    'Accept': 'application/json, text/plain, */*',
    'Requestverificationtoken': '',
    'Sec-Ch-Ua-Mobile': '',
    'User-Agent': '',
    'Sec-Ch-Ua-Platform': '',
    'Origin': '',
    'Sec-Fetch-Site': '',
    'Sec-Fetch-Mode': '',
    'Sec-Fetch-Dest': '',
    'Referer': '',
    'Accept-Encoding': '',
    'Accept-Language': '',
    'Content-Length': '0'
}

def transmit_packet():
    response = session.patch(url, headers=headers)
    print_logs(f"Status Code: {response.status_code}")
    print_logs(f"Response Body: {response.text}")
    if response.status_code != STATUS_CODE_OK:
        raise Exception(f"status code is not OK. failed.\n\tstatus received is:{response.status_code}")


def transmit_thread_callback():
    # Number of times to send the packet
    start_time = time()
    sleep_time_total = 0

    for i in range(THREAD_TRANSMITS_TOTAL):
        transmit_packet()
        sleep_time_total += sleep_random()
        if i > (THREAD_TRANSMITS_DIVISION - 1) and i % THREAD_TRANSMITS_DIVISION == 0:
            end_time = time()
            time_taken = end_time - start_time 
            print(f"Time taken for last {THREAD_TRANSMITS_DIVISION} iterations was: {time_taken:.4f} seconds")
            print(f"From this period, {sleep_time_total} seconds of them slept")
            print(f"Thread finished iteration, sleeping for {TIME_SLEEP_FOR_BOT_DETECTION} seconds...")
            sleep(TIME_SLEEP_FOR_BOT_DETECTION)
            print("Woken up\n\n")
            start_time = time()
            sleep_time_total = 0

    print("Done sending packets")


def main(): 
    print("Starting...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor: 
        futures = [executor.submit(transmit_thread_callback) for _ in range(THREAD_REPEAT_COUNT)]
        for future in futures:
            future.result()
    print("Finished")


if __name__ == "__main__":
    sleep_time_total = 0
    main()