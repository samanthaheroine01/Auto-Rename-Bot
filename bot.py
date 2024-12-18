import logging
import logging.config
import warnings
from pyrogram import Client, idle
from pyrogram import version
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from pytz import timezone
from datetime import datetime
import asyncio
from plugins.web_support import web_server  # Ensure this file exists
import pyromod

logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):
    def __init__(self):  # Corrected initialization method
        super().__init__(
            name="AshutoshGoswami24",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        app = web.AppRunner(await web_server())  # Ensure this returns a valid app
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

        for id in Config.ADMIN:
            try:
                await self.send_message(
                    id, f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️"
                )
            except Exception as e:
                logging.error(f"Failed to send message to {id}: {e}")

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime("%d %B, %Y")
                time = curr.strftime("%I:%M:%S %p")
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!\n\n📅 Dᴀᴛᴇ : {date}\n⏰ Tɪᴍᴇ : {time}\n🌐 Tɪᴍᴇᴢᴏɴᴇ : Asia/Kolkata\n🤖 Vᴇʀsɪᴏɴ : v{version.__version__} (Layer {layer})</b>",
                )
            except Exception as e:
                logging.error(f"Failed to send log message: {e}")
                    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")


bot_instance = Bot()


def main():
    async def start_services():
        if Config.STRING_SESSION:
            await asyncio.gather(
                bot_instance.start(),  # Start the bot instance
            )
        else:
            await asyncio.gather(bot_instance.start())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    loop.run_forever()


if __name__ == "__main__":  # Fixed main function check
    warnings.filterwarnings("ignore", message="There is no current event loop")
    main()
