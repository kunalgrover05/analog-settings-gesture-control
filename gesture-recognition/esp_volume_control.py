# Code responsible for sending API requests to the ESP server. 
# Implemented as a consumer system implemented using a single thread. Consumes
# any new entries added to the queue and processes them. 
import queue
import threading

# Queue for HTTP requests
http_queue = queue.Queue()

def http_queue_worker():
    print("Starting worker")
    while True:
        try:
            item = None
            if http_queue.empty():
                continue

            print("Non empty queue found")

            # Simple implementation of a queue of size 1, clean up all the elements and
            # process the last element in the queue.
            while not http_queue.empty():
                print("Emptying queue", item)
                item = http_queue.get()
                http_queue.task_done()
            
            print("Processing last item", item)
            timeDiff = time.time() - item['time']
            if item and timeDiff <= ACTION_TIMEOUT:
                print(f'Working on {item}, timeDiff {timeDiff}')
                last_response = requests.post(ENDPOINT_HOST + '/volume?delta=' + str(item['value']), timeout=API_REQUEST_TIMEOUT)
                print(last_response)
                print(f'Finished {item}')
            else:
                print(f'Skipped stale data {item}, timeDiff {timeDiff}')
        except Exception as e:
            print("Failed", e)

# HTTPRequests worker thread
threading.Thread(target=http_queue_worker, daemon=True).start()