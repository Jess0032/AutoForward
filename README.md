# AutoForward

Auto forward messages from chats to others with your **Telegram** user account

## Supported Types

 - **anime** (specify keyword to regex)
 - **channel_to** (ID)
 - **channel_from** (ID)

## Commands >> Used from saved messages


```
/add - add items to the list of the given type
/list - view items of the list of the given type
/delete - delete items from the list of the given type
```


    /add [type]
    element
    element
    ...

    /list [type]

    /delete [type]
    id id id ...

## Examples of use 

    /add anime
    One Piece
    Kaguya

    /add channel_from
    -10012345678

    /add channel_to
    -10087654321

    /delete
    1 2

    /list channel_from


## Environment Variables

    API_ID - Get this value from https://my.telegram.org/apps
    API_HASH - Get this value from https://my.telegram.org/apps
    STRING_SESSION - ⬇️
    DATABASE_URL - 


## Script to get your telegram Session in telethon and pyrogram.

<a href="https://repl.it/@KeselekPermen/UserButt#main.py"><img src="https://img.shields.io/badge/run-string__session.py-blue?style=for-the-badge&logo=repl.it" alt="generate_string" /></a>

This code is part of [UserButt](https://github.com/KeselekPermen69/UserButt) by [Mr.Miss](https://github.com/KeselekPermen69).

Copyleft © [Mr.Miss](https://github.com/KeselekPermen69),  All wrongs reserved.


## Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Jess0032/AutoForward)
