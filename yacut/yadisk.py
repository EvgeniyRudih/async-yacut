import asyncio
import os

import aiohttp


YADISK_API_URL = 'https://cloud-api.yandex.net'
YADISK_UPLOAD_PATH = '/yacut/{}'
YADISK_HEADERS = {
    'Authorization': f'OAuth {os.getenv("DISK_TOKEN")}',
}
YADISK_UPLOAD_PARAMS = {'overwrite': 'true'}


async def upload_file(session, file_name, file_data):
    async with session.get(
        f'{YADISK_API_URL}/v1/disk/resources/upload',
        headers=YADISK_HEADERS,
        params={
            **YADISK_UPLOAD_PARAMS,
            'path': YADISK_UPLOAD_PATH.format(file_name),
        },
    ) as response:
        upload_url = (await response.json())['href']

    async with session.put(upload_url, data=file_data):
        pass

    async with session.get(
        f'{YADISK_API_URL}/v1/disk/resources/download',
        headers=YADISK_HEADERS,
        params={'path': YADISK_UPLOAD_PATH.format(file_name)},
    ) as response:
        return (await response.json())['href']


async def upload_all(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(
                upload_file(session, file.filename, file.read())
                for file in files
            )
        )


def upload_files_to_disk(files):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(upload_all(files))
    finally:
        loop.close()
