import asyncio
import aiohttp

url: str = "http://localhost:5000/add_to_work_2"  # URL - адрес, получающий данные
list_data = [
    {"name": "one", "time": 6},
    {"name": "two", "time": 2},
    {"name": "three", "time": 5},
    {"name": "four", "time": 4},
    {"name": "five", "time": 7},
    {"name": "six", "time": 11},
    {"name": "seven", "time": 15},
    {"name": "eight", "time": 13},
    {"name": "nine", "time": 5},
    {"name": "ten", "time": 3},
]
tasks = []


async def get_page(request, data):
    response = await request.post(url, json=data)
    print("Status:", response.status)
    print("Content-type:", response.headers['content-type'])
    html = await response.json()
    print("Body:", html, "...\n")
    return html


async def main():
    async with aiohttp.ClientSession() as request:
        for data in list_data:
            task = asyncio.create_task(get_page(request, data))
            tasks.append(task)
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
