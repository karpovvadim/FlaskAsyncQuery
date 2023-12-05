import asyncio
import aiohttp

tasks = []
url: str = "http://localhost:5000/add_to_work"  # URL - адрес, получающий данные
list_data = [
    {"name": "one", "time": 6},
    {"name": "two", "time": 3},
    {"name": "three", "time": 5},
    {"name": "four", "time": 19},
    {"name": "five", "time": 7},
    {"name": "six", "time": 11},
    {"name": "seven", "time": 8},
    {"name": "eight", "time": 13},
    {"name": "nine", "time": 4},
    {"name": "ten", "time": 2},
]


async def get_page(request, data):
    async with request.post(url=url, json=data) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        html = await response.text()
        print("Body:", html, "...")


async def main():
    async with aiohttp.ClientSession() as request:
        for data in list_data:
            task = asyncio.create_task(get_page(request, data))
            tasks.append(task)
        return await asyncio.gather(*tasks)


asyncio.run(main())
