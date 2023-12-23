import math
import os
import time
import json
from main.plugins.helpers import TimeFormatter, humanbytes

# ------
FINISHED_PROGRESS_STR = "█"
UN_FINISHED_PROGRESS_STR = "░"
DOWNLOAD_LOCATION = "/app"


async def progress_for_pyrogram(
    current,
    total,
    bot,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        status = f"{DOWNLOAD_LOCATION}/status.json"
        if os.path.exists(status):
            with open(status, 'r+') as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        filled_blocks = "█" * math.floor(percentage / 10)
        empty_blocks = "░" * (10 - math.floor(percentage / 10))

        progress = f"**[{filled_blocks}{empty_blocks}]**\n"

        stats = (
            f"├ 𝙎𝙞𝙯𝙚: {humanbytes(current)} / {humanbytes(total)}\n"
            f"├ 𝙎𝙥𝙚𝙚𝙙: {humanbytes(speed)}/s\n"
            f"├ 𝙀𝙏𝘼: {estimated_total_time if estimated_total_time != '' else '0 s'}\n"
            "╰─⌈ 𝘽𝙤𝙩 𝙢𝙖𝙙𝙚 𝙗𝙮 TIGER ⌋──╯"
        )

        text = f"{ud_type}\n{progress}{stats}"
        try:
            if message.text != text or message.caption != text:
                if not message.photo:
                    await message.edit_text(text=text)
                else:
                    await message.edit_caption(caption=text)
        except Exception:
            pass
