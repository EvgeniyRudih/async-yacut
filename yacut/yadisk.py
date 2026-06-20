import asyncio

import aiohttp


YADISK_UPLOAD_URL = '/v1/disk/resources/upload'
YADISK_DOWNLOAD_URL = '/v1/disk/resources/download'
YADISK_UPLOAD_PATH = '/yacut/{}'
YADISK_AUTH_HEADER = 'OAuth {}'
AUTHORIZATION_HEADER = 'Authorization'
UPLOAD_PARAMS = {'overwrite': 'true'}


async def upload_file(session, file_name, file_data, headers, api_url):
    file_path = YADISK_UPLOAD_PATH.format(file_name)

    async with session.get(
        f'{api_url}{YADISK_UPLOAD_URL}',
        headers=headers,
        params={**UPLOAD_PARAMS, 'path': file_path},
    ) as response:
        upload_url = (await response.json())['href']

    async with session.put(upload_url, data=file_data):
        pass

    async with session.get(
        f'{api_url}{YADISK_DOWNLOAD_URL}',
        headers=headers,
        params={'path': file_path},
    ) as response:
        return (await response.json())['href']


async def upload_all(files, headers, api_url):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(
                upload_file(
                    session,
                    file.filename,
                    file.read(),
                    headers,
                    api_url,
                )
                for file in files
            )
        )


def upload_files_to_disk(files, disk_token, api_url):
    headers = {
        AUTHORIZATION_HEADER: YADISK_AUTH_HEADER.format(disk_token),
    }
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(upload_all(files, headers, api_url))
    finally:
        loop.close()
