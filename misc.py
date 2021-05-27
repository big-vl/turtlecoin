import asyncio
from datetime import datetime


class Misc:
    async def send_message_(
        self, event, message_, buttons=None, pinned=False, file_=None
    ):
        msg = await self.send_message(
            event.chat_id, message=message_, buttons=buttons, file=file_
        )
        if pinned:
            await self.pin_message(event.chat_id, msg, notify=False)
        return msg

    async def update_message_(
        self,
        chat_id=None,
        msg_id=None,
        message_=None,
        user_obj=None,
        buttons=None,
    ):
        format_msg_update = "\n__%s %s__"
        last_update = self.language.message("{last_update}", user_obj)
        message = format_msg_update % (last_update, datetime.now())
        message = "{message_} {message}".format(message_=message_, message=message)
        await self.edit_message(chat_id, msg_id, message, buttons=buttons)
        return message

    async def counter_message(
        self,
        chat_id=None,
        msg_id=None,
        message_=None,
        user_obj=None,
        buttons=None,
        sec=4,
        show_eye=False,
        anti_flood=50,
    ):
        message_hide = str()
        eye = str()
        image_count = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
        ]
        user_obj.counter_message.add(str(msg_id))
        if user_obj:
            message_hide = self.language.message("{message_hide}", user_obj)
            message_hide = "__{m}__".format(m=message_hide)
        if show_eye:
            eye = "👁"
        for count in reversed(range(0, sec)):
            sec_img = "".join([image_count[int(x)] for x in str(count)])
            message_count = "{message} \n\n{eye}{count} {message_hide}".format(
                message=message_, eye=eye, count=sec_img, message_hide=message_hide
            )
            if anti_flood > count:
                await self.edit_message(chat_id, msg_id, message_count, buttons=buttons)
            if str(msg_id) in user_obj.counter_message_break:
                message_count = "{message}".format(
                    message=message_,
                )
                await self.edit_message(chat_id, msg_id, message_count, buttons=buttons)
                user_obj.counter_message.remove(str(msg_id))
                return False
            await asyncio.sleep(1)
        user_obj.counter_message.remove(str(msg_id))  # = False
        return True
