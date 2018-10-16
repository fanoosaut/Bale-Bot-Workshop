from balebot.updater import Updater
import asyncio


updater = Updater(token="57c74e5c2cfee9288eb579dcaf289c8191a9edd3", loop=asyncio.get_event_loop())

dispatcher = updater.dispatcher

updater.run()