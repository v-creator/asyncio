import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from data_service import (additional_load_info, drop_db_table, get_people,
                          make_db_table, paste_to_db)
from model import Base, engine
from pprint import pprint


async def main():
    await drop_db_table()
    await make_db_table()

    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as client:
        for id_chunk in chunked(range(1, 8), 3):
            people_cors = [get_people(client, people_id)
                           for people_id in id_chunk]
            gether_people = await asyncio.gather(*people_cors)

            add_attribute = await additional_load_info(client, gether_people)
            # pprint(gether_people)


            # for attribute in ['homeworld', ]
            # res = await additional_load_info(client, 'homeworld', result)

            # paste_to_db_cor = paste_to_db(result)
            # paste_to_db_task = asyncio.create_task(paste_to_db_cor)
            # tasks.append(paste_to_db_task)

    tasks = asyncio.all_tasks() - {asyncio.current_task(), }
    for task in tasks:
        await task


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
