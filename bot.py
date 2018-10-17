from balebot.updater import Updater
import asyncio
from balebot.filters import PhotoFilter
from balebot.handlers import MessageHandler
from balebot.models.messages import TextMessage, PhotoMessage
from balebot.utils.logger import Logger
from combine_pictures import combine

updater = Updater(token="57c74e5c2cfee9288eb579dcaf289c8191a9edd3", loop=asyncio.get_event_loop())

dispatcher = updater.dispatcher

logger = Logger.get_logger()


def final_download_success(result, user_data):
    print("d success : ", result)
    stream = user_data.get("byte_stream", None)
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    with open("hello.jpg", "wb") as file:
        file.write(stream)
        file.close()

    logger.info("photo saved ...")
    combine("hello.jpg")
    dispatcher.bot.send_photo(user_peer, "result.jpg", "تقدیممممم با عشققق ....:)))", "result.jpg")


def success(response, user_data):
    user_data = user_data['kwargs']
    user_peer = user_data["user_peer"]
    print(user_peer.get_json_object()["id"])
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


@dispatcher.command_handler(["/start"])
def start_bot(bot, update):
    user_peer = update.get_effective_user()
    message = TextMessage("سلام به بات آموزشی خوش اومدید ... لطفا عکس  رو بفرستید ...")
    kwargs = {"message": message, "user_peer": user_peer, "try_times": 1}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(PhotoFilter(), get_photo)])


def get_photo(bot, update):
    user_peer = update.get_effective_user()
    photo = update.get_effective_message()
    kwargs = {"user_peer": user_peer}
    bot.download_file(photo.file_id, user_peer.get_json_object()["id"], "photo",
                      success_callback=final_download_success,
                      failure_callback=failure, kwargs=kwargs)


updater.run()
