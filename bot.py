import asyncio
import datetime

import aioschedule
import pytz
from pyrogram import Client
from pyrogram.errors import FloodWait

from config import (API_HASH, API_ID, BOT_ADMIN_IDS, BOT_LIST,
                    CHANNEL_OR_GROUP_ID, CHECK_DELAY, MESSAGE_ID,
                    SESSION_STRING, TIME_ZONE)

app = Client(
    'BOT',
    API_ID,
    API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

async def bot_check(bot_username):
    """Checks if bot is online or not

    Args:
        bot_username (str): bot username to check

    Returns:
        str: bot status
    """
    try:
        checker_status = await app.send_message(bot_username, "/start")
        first_message_id = checker_status.id
        await asyncio.sleep(5)
        async for message in app.get_chat_history(bot_username, limit=1):
            second_message_id = message.id
        if first_message_id == second_message_id:
            status = f"\n\n🤖 **BOT** : @{bot_username}\n🔴 STATUS : **OFF** ❌"
            for bot_admin_id in BOT_ADMIN_IDS:
                if bot_admin_id.isnumeric():
                    bot_admin_id = int(bot_admin_id)
                try:
                    await app.send_message(bot_admin_id, f"🚨 **Notification** 🚨\n\n» @{bot_username} is **DEAD** ❌")
                except Exception as e:
                    print(e)
        else:
            status = f"\n\n🤖 **BOT** : @{bot_username}\n🟢 STATUS : **ON** ✅"
        await app.read_chat_history(bot_username)
        return status
    except FloodWait as e:
        await asyncio.sleep(e.x)


async def status_checker():
    message = f"**🔗 Wᴇʟᴄᴏᴍᴇ Tᴏ Iɴꜰʟᴇx Bᴏᴛ'ꜱ Sᴛᴀᴛᴜꜱ Cʜᴀɴɴᴇʟ .**\n\n**🔗 Tʜɪꜱ Iꜱ Lɪᴠᴇ Sᴛᴀᴛᴜꜱ Oꜰ Aʟʟ Iɴꜰʟᴇx Bᴏᴛꜱ. Tʜɪꜱ Mᴇꜱꜱᴀɢᴇ Kᴇᴇᴘꜱ Oɴ Uᴘᴅᴀᴛɪɴɢ Iɴ Eᴠᴇʀʏ 60 Mɪɴꜱ Wɪᴛʜ Lɪᴠᴇ Sᴛᴀᴛᴜꜱ Oꜰ Aʟʟ Iɴꜰʟᴇx Bᴏᴛꜱ Wʜᴇᴛʜᴇʀ Tʜᴇʏ Aʀᴇ ON / OFF .**\n\n"
    for bot in BOT_LIST:
        message += await bot_check(bot)
    time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
    last_update = time.strftime("%d %b %Y at %I:%M %p")
    message += f"\n\n🛂 Last Check: {last_update} ({TIME_ZONE})\n\n🟡 **Iᴛ Wɪʟʟ Bᴇ Uᴘᴅᴀᴛᴇᴅ Eᴠᴇʀʏ {CHECK_DELAY} Sᴇᴄᴏɴᴅꜱ ({int(CHECK_DELAY/60)} Mɪɴᴜᴛᴇꜱ)**"
    await app.edit_message_text(int(CHANNEL_OR_GROUP_ID), MESSAGE_ID, message)
    print(f"Last Check: {last_update}")
                        
async def main():
    await app.start()
    info = await app.get_me()
    print(f'[INFO] @{info.username} STARTED!')
    await status_checker()
    aioschedule.every(CHECK_DELAY).seconds.do(status_checker)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)
        
asyncio.get_event_loop().run_until_complete(main())
