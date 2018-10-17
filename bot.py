from balebot.updater import Updater
import asyncio
from balebot.filters import PhotoFilter
from balebot.handlers import MessageHandler
from balebot.models.messages import TextMessage
from balebot.utils.logger import Logger

updater = Updater(token="57c74e5c2cfee9288eb579dcaf289c8191a9edd3", loop=asyncio.get_event_loop())

dispatcher = updater.dispatcher

logger = Logger.get_logger()


def success(response, user_data):
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    userId = user_peer.peer_id
    logger.info("message sent successfully.", extra={"user_id": userId, "tag": "info"})


def failure(response, user_data):
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    userId = user_peer.peer_id
    try_times = int(user_data["try_times"])
    message = user_data["message"]
    if try_times < 2:
        try_times += 1
        logger.error("message send failed", {"user_id": userId, "tag": "error"})
        kwargs = {"message": message, "user_peer": user_peer, "try_times": try_times}
        dispatcher.bot.send_message(message, user_peer, success_callback=success, failure_callback=failure,
                                    kwargs=kwargs)
    else:
        logger.error("time out", extra={"tag": "error"})


def start_bot(bot, update):
    user_peer = update.get_effective_user()
    message = TextMessage("سلام به بات آموزشی خوش اومدید ... لطفا عکس  رو بفرستید ...")
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(PhotoFilter(), get_photo)])


def get_photo(bot, update):
    user_peer = update.get_effective_user()
    photo = update.get_effective_message()



updater.run()
