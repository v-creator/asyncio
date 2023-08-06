import asyncio

from model import Base, Session, SwapiPeople, engine
from pprint import pprint


async def make_db_table():
    """Функция делает миграцию в БД и создает таблицы"""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_db_table():
    """Функция делает миграцию в БД и удаляет таблицы"""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


async def get_people(client, people_id):
    """Функция получает данные от swapi"""

    async with client.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()
        return json_data


async def get_info(client, url):
    """Функция получает дополнительные данные по персонажу от swapi"""

    async with client.get(f'{url}') as response:
        json_data = await response.json()
        return json_data


async def paste_to_db(people_jsons):
    """Функция записывает данные в БД"""

    async with Session() as session:
        orm_objects = [SwapiPeople(json=item) for item in people_jsons]
        session.add_all(orm_objects)
        await session.commit()


async def load_attribute(client, url_list):
    """Функция получает дополнительные данные по персонажу от swapi"""
    attribute_list_cor = [get_info(client, url) for url in url_list]
    get_attribute = await asyncio.gather(*attribute_list_cor)
    return get_attribute


async def additional_load_info(client, people_list):
    for people in people_list:
        for id, value in people.items():
            if id == 'films':
                films_value = await load_attribute(client, value)
                result_films_attr = [row['title'] for row in films_value]
            elif type(value) == list:
                attr_value = await load_attribute(client, value)
                result_attr = [row['name'] for row in attr_value]
                print(1)
        people['films'] = result_films_attr
        pprint(people['films'])
            

    # for attr in ['films', 'species', 'starships', 'vehicles']:
    #     print(attr)
    #     attribute_info = await additional_load_info(client, attr, people_list)

    #             # pprint(attribute_info)
    #         # elif type(value) == list:
    #         #     attribute_info = await additional_load_info(client, id, people_list)
    #         #     pprint(attribute_info)



    # for num in range(len(people_list)):
    #     people_list[num][attribute] = result_attribute[num]

    # pprint.pprint(people_list)

    # if key == 'homeworld':
    #     homeworld_list = await get_info(client, value)
    #     value = get_value['name']
    # # print(type(value))
    # if key == 'films':
    #     get_value = await get_info_list(client, value)
    #     value = [row['title'] for row in get_value]
    # elif key == 'species':
    #     get_value = await get_info_list(client, value)
    #     value = [row['name'] for row in get_value]
    # elif key == 'starships':
    #     get_value = await get_info_list(client, value)
    #     value = [row['name'] for row in get_value]
    # elif key == 'vehicles':
    #     get_value = await get_info_list(client, value)
    #     value = [row['name'] for row in get_value]
    print(people_list)
