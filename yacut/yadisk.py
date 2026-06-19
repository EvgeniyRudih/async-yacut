import asyncio

import aiohttp

from yacut import app
from yacut.constants import (
    YADISK_AUTH_HEADER,
    YADISK_DOWNLOAD_URL,
    YADISK_UPLOAD_PATH,
    YADISK_UPLOAD_URL,
)


def get_headers():
    return {'Authorization':
            YADISK_AUTH_HEADER.format(app.config['DISK_TOKEN'])}


async def upload_file(session, file_name, file_data):
    file_path = YADISK_UPLOAD_PATH.format(file_name)
    headers = get_headers()

    async with session.get(
        f'{app.config["YADISK_API_URL"]}{YADISK_UPLOAD_URL}',
        headers=headers,
        params={'path': file_path, 'overwrite': 'true'},
    ) as resp:
        upload_href = (await resp.json())['href']

    async with session.put(upload_href, data=file_data):
        pass

    async with session.get(
        f'{app.config["YADISK_API_URL"]}{YADISK_DOWNLOAD_URL}',
        headers=headers,
        params={'path': file_path},
    ) as resp:
        return file_name, (await resp.json())['href']


async def upload_all(files):
    async with aiohttp.ClientSession() as session:
        tasks = [
            upload_file(session, file.filename, file.read())
            for file in files
        ]
        return await asyncio.gather(*tasks)


def upload_files_to_disk(files):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(upload_all(files))
    finally:
        loop.close()
