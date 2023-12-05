import asyncio
import datetime
import json

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, request

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

work_flag = False
list_query_time = []
max_workers = 3
count_workers = max_workers


async def work_func(time):
    await asyncio.sleep(time)


@app.route('/add_to_work', methods=['GET', 'POST'])
async def add_to_work():
    global work_flag, count_workers

    if request.method == "POST":
        request_data = request.get_data()
        request_data = json.loads(request_data)
        name_worker = request_data["name"]
        query_time = request_data["time"]
        time_work = int(query_time)
    else:
        name_worker = request.args.get('name')
        query_time = request.args.get('time')
        time_work = int(query_time)

    list_query_time.append(time_work)

    while True:
        if not work_flag and list_query_time[0] == time_work:
            if count_workers > 0:
                count_workers -= 1
                time_work = list_query_time.pop(0)
            if count_workers == 0:
                work_flag = True
            print(datetime.datetime.now(), name_worker, time_work)
            await work_func(time_work)

            if count_workers < max_workers:
                count_workers += 1
            if count_workers == max_workers:
                work_flag = False
            break

        await asyncio.sleep(1)

    return f"name = {name_worker}, time = {time_work}"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
