import os
import asyncio
import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.events import NewMessage
import logging
from animesdb import DBHelper, tables

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s]%(name)s:%(message)s', level=logging.WARNING)

API_ID: int = int(os.getenv("API_ID"))
API_HASH: str = os.getenv("API_HASH")
STRING_SESSION: str = os.environ.get("STRING_SESSION", None)
db = DBHelper(os.getenv("DATABASE_URL"))

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

if STRING_SESSION is None:
    print("Your string session is:\n" + StringSession.save(client.session))


channels = []
destination = []
reg_exp = ''
not_exist = f'There is no such type in the db\n\nposible:\n{", ".join(tables)}'
error = 'An error has occurred and the items could not be added.'


async def act_list(tipo: str):
    result = db.get_items(tipo)
    print(result)
    lista = [x.att for x in result]
    if tipo == tables[0]:
        animes = lista
        global reg_exp
        if animes:
            reg_exp = '(?i).*(' + "|".join([x.replace(" ", "[\W_]") for x in animes]) + ').*'
        else:
            reg_exp = ''
    elif tipo == tables[1]:
        global channels
        channels = lista
    else:
        global destination
        destination = lista

    return result


def filter_type(message: NewMessage):
    if message.message.chat_id in channels and (re.search(reg_exp, message.raw_text) or re.search(reg_exp, message.file.name)):
        return True


@client.on(NewMessage(func=filter_type))
async def forward_files(event):
    print(event.message)
    for dest in destination:
        await bot.send_message(dest, event.message)


@client.on(NewMessage(pattern='\/add (.+)((\n.+)+)', chats="me"))
async def add_elements(event):
    tipo = event.pattern_match.group(1).strip()

    if tipo not in tables:
        await event.respond(not_exist)
        return
    lista = event.pattern_match.group(2).split('\n')[1:]
    list_valida = []
    if tipo == 'channel_from' or tipo == 'channel_to':
        for id in lista:
            try:
                await client.get_entity(int(id))
                list_valida.append(int(id))
            except Exception as e:
                await event.respond(f'{id} is not a valid entity.')
                print(e)
    else:
        list_valida = lista
    if list_valida:
        if db.add_items(tipo, list_valida):
            await event.respond(f'Elements successfully added to {tipo}.')
            await act_list(tipo)
        else:
            await event.respond(error)
    else:
        await event.respond('no element has been added.')



@client.on(NewMessage(pattern='\/delete (.+)\n((\s*\d)+)', chats="me"))
async def delete_elements(event):
    tipo = event.pattern_match.group(1).strip()
    lista = event.pattern_match.group(2).split()

    if tipo not in tables:
        await event.respond(not_exist)
        return
    if db.del_items(tipo, lista):
        await event.respond(f'Items successfully deleted from  {tipo}.')
        await act_list(tipo)
    else:
        await event.respond(error)


@client.on(NewMessage(pattern='\/list (.+)', chats="me"))
async def get_elements(event):
    tipo = event.pattern_match.group(1)

    if tipo not in tables:
        await event.respond(not_exist)
        return
    lista = await act_list(tipo=tipo)

    if lista:
        final = f'**List of {tipo}**\n'
        for element in lista:
            final += f'\nid: {element.id} telegram_id: {element.att}'
            if tipo == 'channel_from' or tipo == 'channel_to':
                final += f" name: {(await client.get_entity(element.att)).title}"
        await event.respond(final)
    else:
        await event.respond(f'No items in {tipo}.')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(act_list(tipo='anime'))
    loop.create_task(act_list(tipo='channel_from'))
    loop.create_task(act_list(tipo='channel_to'))
    loop.run_forever()


