import asyncio
import argparse
from random import randint
from typing import Any
from better_proxy import Proxy

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions, get_tg_client
from bot.utils.accounts import Accounts



art_work = """

                888                             888  
                888                             888                         
                888                             888                         
 .d8888b 8888b. 888888.d8888b     ____      .d88888 .d88b.  .d88b. .d8888b                          
d88P"       "88b888   88K        /  _ \    d88" 888d88""88bd88P"88b88K
888     .d888888888   "Y8888b.   >  _ </\  888  888888  888888  888"Y8888b.      
Y88b.   888  888Y88b.      X88  /  <_\ \/  Y88b 888Y88..88PY88b 888     X88 
 "Y8888P"Y888888 "Y888 88888P'  \_____\ \   "Y88888 "Y88P"  "Y88888 88888P'
                                       \/                       888
                                                           Y8b d88P 
                                                            "Y88P"
                                                                      by Surinity                                    
"""

version = "      accounts.json edition"

start_text = """                                             
Select an action:

    1. Run bot
    2. Create session
    
"""


def get_proxy(raw_proxy: str) -> Proxy:
    return Proxy.from_str(proxy=raw_proxy).as_url if raw_proxy else None


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")
    action = parser.parse_args().action

    if not action:
        print('\033[1m' + '\033[92m' + art_work + '\033[0m')
        print('\033[1m' + '\033[93m' + version + '\033[0m')
        print(start_text)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
            elif action not in ["1", "2"]:
                logger.warning("Action must be 1 or 2")
            else:
                action = int(action)
                break

    if action == 2:
        await register_sessions()
    elif action == 1:
        accounts = await Accounts().get_accounts()
        await run_tasks(accounts=accounts)


async def run_tasks(accounts: [Any, Any, list]):
    tasks = []
    for account in accounts:
        session_name, user_agent, raw_proxy = account.values()
        tg_client = await get_tg_client(session_name=session_name, proxy=raw_proxy)
        proxy = get_proxy(raw_proxy=raw_proxy)
        tasks.append(asyncio.create_task(run_tapper(tg_client=tg_client, user_agent=user_agent, proxy=proxy)))
        await asyncio.sleep(delay=randint(settings.START_DELAY[0], settings.START_DELAY[1]))

    await asyncio.gather(*tasks)
