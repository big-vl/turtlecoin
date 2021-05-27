import telethon
import logging
import time
import asyncio
import json
import lib
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.types import MessageMediaPhoto
from module import Language
from wares import Wares
from buttons import Buttons
from misc import Misc
from user import User
from os import environ


class Subbot(TelegramClient, Wares, Buttons, Misc):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = Language()
        self.add_event_handler(self.on_update, events.NewMessage)
        self.add_event_handler(self.on_callback, events.CallbackQuery)
        self.user_list = {}
        self.donate = "`TRTLv3Xfx2YCXfPKcfuFDpefDF5UP1RR964JJJrPfHBYh3x6Z8v3XkuLAoZRBzFzBG2F1UqxRSc71Td89dyNV2eVfPdsd2jdMR8`"

    async def on_callback(self, event):
        print("event", event)
        print("event dir", dir(event))
        user_obj = await self.get_user_obj(event)
        data = event.data.decode("utf-8")
        print("user_obj", user_obj)
        if len(data) < 64:
            data = json.loads(data)
        if user_obj.wallet.open_wallet() and user_obj.auth:
            if user_obj.auth:
                if "pin" in data:
                    await self.delete_messages(event.chat_id, event.query.msg_id)
            if "page_transactions" in data:
                if isinstance(data["page_transactions"], int):
                    page = data["page_transactions"]
                    event, message_, buttons, pinned = await self.transactions(
                        event, user_obj, page=page
                    )
                    message_ = await self.update_message_(
                        chat_id=event.chat_id,
                        msg_id=event.query.msg_id,
                        message_=message_,
                        user_obj=user_obj,
                        buttons=buttons,
                    )
            elif "wallet" in data:
                if data["wallet"] == "rescan":
                    if user_obj.wallet.rescan:
                        rescan = True
                    else:
                        rescan = await user_obj.wallet.rescan_wallet()
                    if rescan:
                        event, message_, buttons, pinned = await self.sync_status(
                            event, user_obj
                        )
                        message_ = await self.update_message_(
                            chat_id=event.chat_id,
                            msg_id=event.query.msg_id,
                            message_=message_,
                            user_obj=user_obj,
                            buttons=buttons,
                        )
            elif "my_wallet" in data:
                if data["my_wallet"] == "create":
                    create = await user_obj.wallet.create_wallet_sub()
                    if create:
                        event, message_, buttons, pinned = await self.my_wallets(
                            event, user_obj
                        )
                        await event.edit(message_, buttons=buttons)
                elif data["my_wallet"] == "import":
                    message_ = self.language.message("{donate}", user_obj) + self.donate
                    import_ = await self.send_message(
                        event.chat_id,
                        message=message_,
                    )
                elif data["my_wallet"] == "import_view":
                    message_ = self.language.message("{donate}", user_obj) + self.donate
                    import_ = await self.send_message(
                        event.chat_id,
                        message=message_,
                    )
            elif "send_coin" in data:
                if not data["send_coin"]:
                    user_obj.send_coin = {}
                    del user_obj.send_coin_msg
                    await self.delete_messages(event.chat_id, event.query.msg_id)
            elif await self.send_hash(data, user_obj):
                format_msg_success = (
                    "**%s**\n\n**%s:**\n`%s`\n\n**%s: %s**\n**%s: %s**\n**%s: %s**"
                )
                format_msg_error = "**%s**"
                send_hash = await user_obj.wallet.send_hash(
                    hash_=user_obj.send_coin["hash"]
                )
                print("send_hash", send_hash)
                success_transfer = self.language.message("{success_transfer}", user_obj)
                amount_text = self.language.message("{amount}", user_obj)
                fee_text = self.language.message("{fee}", user_obj)
                total_text = self.language.message("{total}", user_obj)
                send_to_text = self.language.message("{send_to}", user_obj)
                total = int(user_obj.send_coin["fee"]) + int(
                    user_obj.send_coin["amount"]
                )
                message_ = format_msg_success % (
                    success_transfer,
                    send_to_text,
                    user_obj.send_coin["address"],
                    amount_text,
                    user_obj.send_coin["amount"],
                    fee_text,
                    user_obj.send_coin["fee"],
                    total_text,
                    total,
                )
                await event.edit(message_)
            elif "get_mnemonic_keys" in data:
                if data["get_mnemonic_keys"]:
                    if await user_obj.wallet.wallet_exists_async():
                        format_msg_mnemonic = (
                            "**%s:**\n`%s`\n**%s:**\n`%s`\n**%s:**\n`%s`\n\n%s"
                        )
                        (
                            mnemonic,
                            private,
                            view,
                        ) = await user_obj.wallet.get_mnemonic_keys()
                        mnemonic_phrase_text = self.language.message(
                            "{mnemonic_phrase_text}", user_obj
                        )
                        private_key_text = self.language.message(
                            "{private_key_text}", user_obj
                        )
                        view_key_text = self.language.message(
                            "{view_key_text}", user_obj
                        )
                        mnemonic_attention = self.language.message(
                            "{mnemonic_attention}", user_obj
                        )
                        message_ = format_msg_mnemonic % (
                            mnemonic_phrase_text,
                            mnemonic,
                            private_key_text,
                            private,
                            view_key_text,
                            view,
                            mnemonic_attention,
                        )
                        await event.edit(message_)
                        if await self.counter_message(
                            event.chat_id,
                            event.query.msg_id,
                            message_,
                            user_obj=user_obj,
                            sec=30,
                            show_eye=True,
                        ):
                            await self.delete_messages(
                                event.chat_id, event.query.msg_id
                            )
                    else:
                        message_ = self.language.message(
                            "{wallet_file_exists_false}", user_obj
                        )
                        await event.edit(message_)
        elif not user_obj.auth:
            pin = user_obj.security_pincode(data)
            print("pincode:", pin)
            if pin is None:
                message_ = "{message}\n{lenpin}".format(
                    message=self.language.message("{wallet_open_security}", user_obj),
                    lenpin=user_obj.pincode_len(),
                )
                await event.edit(message_, buttons=self.buttons_pincode_panel(user_obj))
            elif "success" in pin.keys():
                if await self.run_wallet(event.chat_id, event.query.msg_id, user_obj):
                    message_ = self.language.message("{wallet_open_true}", user_obj)
                    await event.edit(message_)
                    if user_obj.command:
                        command = await user_obj.command(event, user_obj)
                        msg = await self.send_message_(*command)
                        if user_obj.command == self.send_coin:
                            user_obj.send_coin_msg = msg
                        elif user_obj.command == self.get_balance:
                            user_obj.update_msg = msg
            elif "button" in pin.keys():
                if "bN" in pin.values():
                    event, message_, buttons = await self.security_pincode_menu(
                        event, user_obj
                    )
                    await event.edit(message_, buttons=buttons)
            elif "error" in pin.keys():
                event, message_, buttons = await self.security_pincode_menu(
                    event, user_obj
                )
                if "no_pincode" in pin.values():
                    await event.edit(message_, buttons=buttons)
                elif "pincode_retry" in pin.values():
                    format_msg = "**%s: %s**"
                    error_pincode_retry = self.language.message(
                        "{error_pincode_retry}", user_obj
                    )
                    message_ = format_msg % (
                        error_pincode_retry,
                        user_obj.block_wallet_str(),
                    )
                    await event.edit(message_, buttons=buttons)
                elif "pincode" in pin.values():
                    await event.edit(message_, buttons=buttons)

    async def connect(self):
        await super().connect()
        self.me = await self.get_me()
        print("Connect bot...", self.me)

    async def send_hash(self, data, user_obj):
        if "hash" in user_obj.send_coin:
            if user_obj.send_coin["hash"]:
                return True
        return False

    async def run_wallet(self, chat_id, msg_id, user_obj=None, import_=[]):
        if user_obj:
            message_ = self.language.message("{pre_init_wallet}", user_obj)
            await self.edit_message(
                chat_id,
                msg_id,
                message_,
            )
            daemon = await user_obj.wallet.daemon_start()
            print("daemon", daemon)
            if daemon:
                if import_:
                    wallet = await user_obj.wallet.import_seed(import_)
                elif await user_obj.wallet.wallet_exists_async():
                    wallet = await user_obj.wallet.start_open_wallet()
                else:
                    wallet = await user_obj.wallet.create_wallet()
                message_ = self.language.message("{init_wallet}", user_obj)
                await self.edit_message(
                    chat_id,
                    msg_id,
                    message_,
                )
                if wallet:
                    message_ = self.language.message(
                        "{init_wallet_node_config}", user_obj
                    )
                    await self.edit_message(
                        chat_id,
                        msg_id,
                        message_,
                    )
                    node = await user_obj.wallet.set_node()
                    if node:
                        message_ = self.language.message("{init_wallet_node}", user_obj)
                        await self.edit_message(
                            chat_id,
                            msg_id,
                            message_,
                        )
                    return True
            else:
                if "error" in user_obj.wallet:
                    error = user_obj.wallet.error
                    print(error)
                    message_ = self.language.message("{wallet_error}", user_obj)
                    message_ = message.format(error=error)
                    await self.edit_message(
                        chat_id,
                        msg_id,
                        message_,
                    )
                else:
                    message_ = self.language.message("{unknow_wallet_error}", user_obj)
                    await self.edit_message(
                        chat_id,
                        msg_id,
                        message_,
                    )
        else:
            message_ = self.language.message("{user_obj_wallet_error}", user_obj)
            await self.edit_message(
                chat_id,
                msg_id,
                message_,
            )
        return False

    async def get_user_obj(self, event):
        if hasattr(event, "message"):
            user_id = str(event.message.peer_id.user_id)
        else:
            user_id = str(event.sender_id)
        if user_id not in self.user_list.keys():
            user_obj = User(user_id=user_id)
            self.user_list[user_id] = user_obj
        else:
            user_obj = self.user_list[user_id]
        return user_obj

    async def on_update(self, event):
        for user_ in self.user_list.values():
            user_.deactive()
        message = event.message.message
        print("event", dir(event))
        print("message", event.message)
        print("event to dict", event.to_dict())
        print("client", event.client)
        print("chat_id", event.chat_id)
        user_obj = await self.get_user_obj(event)
        check_button = await self.language.check_button(event.message.message, user_obj)
        check_flag = await self.language.check_flag(message)
        flags_list = self.language.flags_list
        if message in flags_list:
            if check_flag:
                format_msg_change_language = "**%s:** %s\n**%s**"
                self.language.choiceLanguage(message, user_obj)
                select_language = self.language.message("{select_language}", user_obj)
                send_flag_text = self.language.message("{send_flag_text}", user_obj)
                message_ = format_msg_change_language % (
                    select_language,
                    message,
                    send_flag_text,
                )
                await self.send_message(
                    event.chat_id, message=message_, buttons=self.buttons_menu(user_obj)
                )
            else:
                format_msg_flag_detected = "**%s**\n\n**%s:**\n`%s`"
                flag_detected = self.language.message("{flag_detected}", user_obj)
                example_text = self.language.message("{example_text}", user_obj)
                flag_detected_example = self.language.language_translate["us"][
                    "{flag_detected_example}"
                ]
                message_ = format_msg_flag_detected % (
                    flag_detected,
                    example_text,
                    flag_detected_example,
                )
                await self.send_message(
                    event.chat_id, message=message_, buttons=self.buttons_menu(user_obj)
                )
        elif len(message.split()) == 25:
            mnemonic_list = message.split()
            if not await user_obj.wallet.wallet_exists_async():
                wallet_import_process = self.language.message(
                    "{wallet_import_process}", user_obj
                )
                import_wallet = await self.send_message(
                    event.chat_id,
                    message=wallet_import_process,
                )
                chat_id = event.chat_id
                msg_id = import_wallet.id
                check_mnemonic_list = [lib.check_mnemonic(m) for m in mnemonic_list]
                if all(check_mnemonic_list):
                    await self.delete_messages(event.chat_id, event.message)
                    if (
                        await self.run_wallet(
                            chat_id, msg_id, user_obj, import_=mnemonic_list
                        )
                        is True
                    ):
                        format_import_wallet_msg = "**%s**"
                        wallet_import_success = self.language.message(
                            "{wallet_import_success}", user_obj
                        )
                        message_ = format_import_wallet_msg % (wallet_import_success)
                        if await self.counter_message(
                            event.chat_id,
                            import_wallet.id,
                            message_,
                            user_obj=user_obj,
                            sec=4,
                            show_eye=False,
                        ):
                            await self.delete_messages(event.chat_id, import_wallet)
                            my_wallets = await self.my_wallets(
                                event,
                                user_obj,
                                buttons=self.buttons_menu(user_obj),
                                view_buttons=False,
                            )
                            await self.send_message_(*my_wallets)
                    else:
                        format_import_wallet_msg = "**%s**:\n__%s__"
                        wallet_import_error = self.language.message(
                            "{wallet_import_error}", user_obj
                        )
                        message_ = format_import_wallet_msg % (
                            wallet_import_error,
                            user_obj.wallet.get_error(),
                        )
                        await self.edit_message(
                            import_wallet,
                            message_,
                        )
                else:
                    format_import_wallet_msg = "**%s:**\n**%s**"
                    wallet_import_error = self.language.message(
                        "{wallet_import_wrong_one_word}", user_obj
                    )
                    error_mnemonic_word = [
                        mnemonic_list[i]
                        for i in range(0, len(check_mnemonic_list))
                        if not check_mnemonic_list[i]
                    ]
                    error_mnemonic_word = " ".join(error_mnemonic_word)
                    message_ = format_import_wallet_msg % (
                        wallet_import_error,
                        error_mnemonic_word,
                    )
                    await self.edit_message(
                        import_wallet,
                        message_,
                    )
        elif not await user_obj.wallet.wallet_exists_async() and lib.check_mnemonic(
            message
        ):
            format_check_mnemonic = "**%s**"
            send_wrong_one_word = self.language.message(
                "{wallet_import_send_wrong_one_word}", user_obj
            )
            message_ = format_check_mnemonic % (send_wrong_one_word)
            await self.send_message(
                event.chat_id, message=message_, buttons=self.buttons_menu(user_obj)
            )
        elif len(message.split("#")) == 2 and len(message) < 10:
            message = message.split("#")
            format_flag_add_thank = "**%s**"
            f = open("flag.txt", "a+")
            f.write('"%s": "%s",\n' % (message[1], message[0].strip()))
            f.close()
            flag_add_thank = self.language.message("{flag_add_thank}", user_obj)
            message_ = format_flag_add_thank % (flag_add_thank)
            await self.send_message(
                event.chat_id, message=message_, buttons=self.buttons_menu(user_obj)
            )
        elif event.message.media is not None:
            if isinstance(event.message.media, MessageMediaPhoto):
                file_ = await self.download_media(event.message, file=bytes)
                detected_qrcode_list = user_obj.read_qr(file_)
                security = await self.security_pincode_menu(event, user_obj)
                print(
                    "detected_qrcode_list",
                    bool(detected_qrcode_list),
                    detected_qrcode_list,
                )
                if detected_qrcode_list:
                    if detected_qrcode_list[0].data.decode("utf-8").startswith("TRTL"):
                        user_obj.send_coin = {}
                        if event.message.message.isdigit():
                            user_obj.send_coin = {
                                **user_obj.send_coin,
                                "amount": event.message.message,
                            }
                        user_obj.send_coin = {
                            **user_obj.send_coin,
                            "address": detected_qrcode_list[0].data.decode("utf-8"),
                        }
                        if security is True:
                            send_coin = await self.send_coin(event, user_obj)
                            user_obj.send_coin_msg = await self.send_message_(
                                *send_coin
                            )
                        else:
                            await self.send_message_(*security)
                            user_obj.command = self.send_coin
                    else:
                        no_detected_qr_trtl = self.language.message(
                            "{no_detected_qr_trtl}", user_obj
                        )
                        await self.send_message(
                            event.chat_id,
                            message=no_detected_qr_trtl,
                        )
                else:
                    no_detected_qr = self.language.message("{no_detected_qr}", user_obj)
                    await self.send_message(
                        event.chat_id,
                        message=no_detected_qr,
                    )
            else:
                no_detected_photo = self.language.message(
                    "{no_detected_photo}", user_obj
                )
                await self.send_message(
                    event.chat_id,
                    message=no_detected_photo,
                )
        elif event.message.message.isdigit():
            await self.delete_messages(event.chat_id, event.message)
            if "address" in user_obj.send_coin.keys():
                if hasattr(user_obj, "send_coin_msg"):
                    user_obj.send_coin = {
                        **user_obj.send_coin,
                        "amount": event.message.message,
                    }
                    event, message_, buttons, pinned = await self.send_coin(
                        event, user_obj
                    )
                    msg_id = user_obj.send_coin_msg.id
                    if str(msg_id) in user_obj.counter_message:
                        user_obj.counter_message_break.add(str(msg_id))
                        await asyncio.sleep(1)
                        user_obj.counter_message_break.remove(str(msg_id))
                    event, message_, buttons, pinned = send_coin = await self.send_coin(
                        event, user_obj
                    )
                    message_ = await self.update_message_(
                        chat_id=event.chat_id,
                        msg_id=msg_id,
                        message_=message_,
                        user_obj=user_obj,
                        buttons=buttons,
                    )
                    if await self.counter_message(
                        chat_id=event.chat_id,
                        msg_id=msg_id,
                        message_=message_,
                        user_obj=user_obj,
                        buttons=buttons,
                        sec=300,
                        show_eye=True,
                    ):
                        user_obj.send_coin = None
                        await self.delete_messages(
                            event.chat_id, user_obj.send_coin_msg
                        )
                else:
                    print("hassatr not send_coin_msg")
        elif event.message.message.startswith("TRTL"):
            security = await self.security_pincode_menu(event, user_obj)
            user_obj.send_coin = {"address": event.message.message}
            if security is True:
                send_coin = await self.send_coin(event, user_obj)
                user_obj.send_coin_msg = await self.send_message_(*send_coin)
            else:
                await self.send_message_(*security)
                user_obj.command = self.send_coin
        elif any(check_button):
            option_button, check_button_text = check_button
            if option_button in ["{hide_lang}", "{show_lang}"]:
                if user_obj.hide_lang:
                    user_obj.hide_lang = False
                else:
                    user_obj.hide_lang = True
                message_option = "{choice}".format(
                    choice=check_button_text
                )
                hide_show_lang = await self.send_message(
                    event.chat_id,
                    message=message_option.format(choice=message),
                    buttons=self.buttons_menu(user_obj),
                )
            elif option_button == "{all_balance}":
                security = await self.security_pincode_menu(event, user_obj)
                if security is True:
                    if user_obj.command == self.get_balance:
                        if hasattr(user_obj, "update_msg"):
                            (
                                event,
                                message_,
                                buttons,
                                pinned,
                            ) = all_balance = await self.get_balance(event, user_obj)
                            if await self.update_message_(
                                event.chat_id,
                                user_obj.update_msg.id,
                                message_,
                                user_obj=user_obj,
                            ):
                                await self.delete_messages(event.chat_id, event.message)
                    else:
                        user_obj.command = self.get_balance
                        all_balance = await self.get_balance(event, user_obj)
                        balance_msg = await self.send_message_(*all_balance)
                        user_obj.update_msg = balance_msg
                else:
                    await self.send_message_(*security)
                    user_obj.command = self.get_balance
            elif option_button == "{sync_status}":
                security = await self.security_pincode_menu(event, user_obj)
                if security is True:
                    sync_status = await self.sync_status(event, user_obj)
                    await self.send_message_(*sync_status)
                    if user_obj.command == self.sync_status:
                        pass
                    else:
                        user_obj.command = self.sync_status
                else:
                    await self.send_message_(*security)
                    user_obj.command = self.sync_status
            elif option_button == "{my_wallets}":
                security = await self.security_pincode_menu(event, user_obj)
                if security is True:
                    my_wallets = await self.my_wallets(event, user_obj)
                    await self.send_message_(*my_wallets)
                    if user_obj.command == self.my_wallets:
                        pass
                    else:
                        user_obj.command = self.my_wallets
                else:
                    await self.send_message_(*security)
                    user_obj.command = self.my_wallets
            elif option_button == "{all_transactions}":
                security = await self.security_pincode_menu(event, user_obj)
                if security is True:
                    transactions = await self.transactions(event, user_obj)
                    await self.send_message_(*transactions)
                    if user_obj.command == self.transactions:
                        pass
                    else:
                        user_obj.command = self.transactions
                else:
                    await self.send_message_(*security)
                    user_obj.command = self.transactions
            elif option_button == "{get_mnemonic_keys}":
                security = await self.security_pincode_menu(event, user_obj)
                if security is True:
                    get_mnemonic_keys = await self.get_mnemonic_keys(event, user_obj)
                    await self.send_message_(*get_mnemonic_keys)
                    if user_obj.command == self.get_mnemonic_keys:
                        pass
                    else:
                        user_obj.command = self.get_mnemonic_keys
                else:
                    await self.send_message_(*security)
                    user_obj.command = self.get_mnemonic_keys
            elif option_button == "{send_turtlecoin}":
                message_ = self.language.message("{send_turtlecoin_text}", user_obj)
                await self.send_message(
                    event.chat_id,
                    message=message_,
                )
            elif option_button == "{import_wallet}":
                if not await user_obj.wallet.wallet_exists_async():
                    message_ = self.language.message("{import_wallet_text}", user_obj)
                    init_wallet = await self.send_message(
                        event.chat_id, message=message_
                    )
            elif option_button == "{create_wallet}":
                if not await user_obj.wallet.wallet_exists_async():
                    message_ = self.language.message("{create_new_user}", user_obj)
                    init_wallet = await self.send_message(
                        event.chat_id, message=message_
                    )
                    if await self.run_wallet(event.chat_id, init_wallet.id, user_obj):
                        message_ = self.language.message(
                            "{create_wallet_success}", user_obj
                        )
                        await self.edit_message(
                            init_wallet,
                            message_,
                        )
                        if await self.counter_message(
                            event.chat_id,
                            init_wallet.id,
                            message_,
                            user_obj=user_obj,
                            sec=4,
                            show_eye=False,
                        ):
                            await self.delete_messages(event.chat_id, init_wallet)
                            my_wallets = await self.my_wallets(
                                event,
                                user_obj,
                                buttons=self.buttons_menu(user_obj),
                                view_buttons=False,
                            )
                            await self.send_message_(*my_wallets)
                        else:
                            error = await self.language.translate(
                                create_["error"], user_obj
                            )
                            message_ = self.language.message(
                                "{wallet_error}", user_obj
                            ).format(error=error, **image)
                            await self.edit_message(
                                init_wallet,
                                message_,
                            )
                else:
                    message_ = self.language.message("{create_wallet_exists}", user_obj)
                    create_wallet_exists = await self.send_message(
                        event.chat_id,
                        message=message_,
                        buttons=self.buttons_menu(user_obj),
                    )
        elif event.message.message == "/start":
            welcome = self.language.message("{welcome_bot}", user_obj)
            await self.send_message(
                event.chat_id,
                message=welcome,
                buttons=self.buttons_menu(user_obj),
                file="images/turtlecoin_wallet.png",
            )
            user_obj.command = None
        print("active user:", self.user_list)


bot = Subbot(
    environ.get("TG_SESSION"), environ.get("TG_API_ID"), environ.get("TG_API_HASH")
).start(bot_token=environ.get("TG_TOKEN"))
bot.run_until_disconnected()
