import asyncio

import aiohttp

from yacut import app, db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id

YADISK_API = 'https://cloud-api.yandex.net'


async def upload_file(session, file_name, file_data):
    token = app.config['DISK_TOKEN']
    headers = {'Authorization': f'OAuth {token}'}

    # 1. Получаем ссылку для загрузки
    async with session.get(
        f'{YADISK_API}/v1/disk/resources/upload',
        headers=headers,
        params={'path': f'/yacut/{file_name}', 'overwrite': 'true'}
    ) as resp:
        data = await resp.json()
        upload_href = data['href']

    # 2. Загружаем файл
    async with session.put(upload_href, data=file_data) as resp:
        pass

    # 3. Получаем ссылку для скачивания
    async with session.get(
        f'{YADISK_API}/v1/disk/resources/download',
        headers=headers,
        params={'path': f'/yacut/{file_name}'}
    ) as resp:
        data = await resp.json()
        download_href = data['href']

    return file_name, download_href


async def upload_all(files):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for f in files:
            file_data = f.read()
            tasks.append(upload_file(session, f.filename, file_data))
        results = await asyncio.gather(*tasks)
    return results


def upload_files_to_disk(files):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        raw_results = loop.run_until_complete(upload_all(files))
    finally:
        loop.close()

    results = []
    for file_name, download_url in raw_results:
        short_id = get_unique_short_id()
        url_map = URLMap(original=download_url, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        from flask import url_for
        short_link = url_for('redirect_view',
                             short_id=short_id, _external=True)
        results.append({'name': file_name, 'short_link': short_link})
    return results
