import asyncio
import json
import datetime
from collections import deque

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

deque_queries = deque()
max_workers = 3
current_workers = {}


async def work_func(t):
    await asyncio.sleep(t)


@app.route('/get_statistics', methods=['GET'])
async def get_statistics():
    return json.dumps({
        "in_work": current_workers,
        "in_queue": dict(deque_queries)
    })


@app.route('/add_to_work_2', methods=['GET', 'POST'])
async def add_to_work():
    if request.method == "POST":
        request_data = request.get_data()
        request_data = json.loads(request_data)
        name_workers = request_data["name"]
        query_time = request_data["time"]
        time_work = int(query_time)
    else:
        name_workers = request.args.get('name')
        query_time = request.args.get('time')
        time_work = int(query_time)

    deque_queries.append((name_workers, time_work))

    while True:
        dq_left = deque_queries.popleft()
        deque_queries.insert(0, dq_left)
        if len(current_workers) < max_workers and dq_left[0] == name_workers:
            current_workers[name_workers] = time_work
            deque_queries.popleft()
            print(datetime.datetime.now(), name_workers, time_work)

            await work_func(time_work)

            del current_workers[name_workers]

            break
        await asyncio.sleep(1)

    if request.method == 'POST':
        response = {name_workers: time_work}
    else:
        response = f"name = {name_workers}, time = {time_work}"
    return response


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
