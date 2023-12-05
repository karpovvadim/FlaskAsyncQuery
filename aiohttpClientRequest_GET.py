import asyncio
import aiohttp

url: str = "http://localhost:5000/add_to_work_2"  # URL - адрес, получающий данные
list_data = [
    {"name": "One", "time": 8},
    {"name": "Two", "time": 3},
    {"name": "Three", "time": 5},
    {"name": "Four", "time": 19},
    {"name": "Five", "time": 15},
    {"name": "Six", "time": 11},
    {"name": "Seven", "time": 9},
    {"name": "Eight", "time": 13},
    {"name": "Nine", "time": 7},
    {"name": "Ten", "time": 4},
]


async def get_page(session, data):
    resp = await session.get(url, params=data)
    print("Status:", resp.status)
    print("Content-type:", resp.headers['content-type'])
    html = await resp.text()
    print("Body:", html, "...\n")
    return html


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for data in list_data:
            task = asyncio.create_task(get_page(session, data))
            tasks.append(task)

        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
