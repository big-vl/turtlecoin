import math
from telethon import Button


class Wares:
    async def get_balance(self, event, user_obj, buttons=None, pinned=False):
        balance = await user_obj.wallet.get_balances()
        total_balance, main_wallet, main_wallet_balance, other_wallets_balance = balance
        get_balance_total = self.language.message("{get_balance_total}", user_obj)
        get_balance_confirmed = self.language.message(
            "{get_balance_confirmed}", user_obj
        )
        get_balance_unconfirmed = self.language.message(
            "{get_balance_unconfirmed}", user_obj
        )
        wallet_address = self.language.message("{wallet_address}", user_obj)
        your_main_wallet = self.language.message("{your_main_wallet}", user_obj)
        total_balance_ = self.language.message("{all_balance}", user_obj)
        format_msg_total = "**%s**\n**%s %s**\n**%s %s**\n\n"
        format_msg_main_wallet = "**%s #1:**\n`%s`\n**%s %s**\n**%s %s**\n\n"
        format_msg_sub_wallet = "**%s #%s:**\n`%s`\n**%s %s**\n**%s %s**\n\n"
        message_ = format_msg_total % (
            get_balance_total,
            get_balance_confirmed,
            total_balance["unlocked"],
            get_balance_unconfirmed,
            total_balance["locked"],
        )
        message_ += format_msg_main_wallet % (
            your_main_wallet,
            main_wallet,
            get_balance_confirmed,
            main_wallet_balance["unlocked"],
            get_balance_unconfirmed,
            main_wallet_balance["locked"],
        )

        message_tmp = str()
        if other_wallets_balance:
            for w in other_wallets_balance:
                message_tmp += format_msg_sub_wallet % (
                    wallet_address,
                    other_wallets_balance.index(w) + 2,
                    w["address"],
                    get_balance_confirmed,
                    w["unlocked"],
                    get_balance_unconfirmed,
                    w["locked"],
                )

        message_ = "{message_}{message_tmp}".format(
            message_=message_, message_tmp=message_tmp
        )
        return (event, message_, buttons, pinned)

    async def security_pincode_menu(self, event, user_obj):
        if await user_obj.wallet.daemon_start():
            if user_obj.auth:
                return True
            else:
                message_ = (
                    self.language.message("{wallet_open_security}", user_obj) + "\n"
                )
                buttons = self.buttons_pincode_panel(user_obj)
                return (event, message_, buttons)

    async def send_hash_message(self, event, user_obj, buttons=None, pinned=True):
        format_msg = "%s\n\n%s"
        success_transfer = self.language.message("{success_transfer}", user_obj)
        message_ = format_msg % ()
        return (event, message_, buttons, pinned)

    async def sync_status(self, event, user_obj, buttons=None, pinned=False):
        format_msg_sync = "**%s:**\n\n%s: **%s** \n%s: **%s** \n%s: **%s**\n\n%s"
        get_status = await user_obj.wallet.get_status()
        sync_status = self.language.message("{sync_status}", user_obj)
        wallet_block_count = self.language.message("{wallet_block_count}", user_obj)
        local_daemon_block_count = self.language.message(
            "{local_daemon_block_count}", user_obj
        )
        network_block_count = self.language.message("{network_block_count}", user_obj)
        synchronized_on = self.language.message("{synchronized_on}", user_obj)
        synchronized_error = self.language.message("{synchronized_error}", user_obj)
        print("get_status", get_status, user_obj)
        if get_status["localDaemonBlockCount"] != 0:
            percent = (
                100
                * float(get_status["walletBlockCount"])
                / float(get_status["localDaemonBlockCount"])
            )
            if percent == 100.0:
                load = "🟩"
                if user_obj.wallet.rescan:
                    user_obj.wallet.rescan = False
            else:
                load = "🟥"
                user_obj.wallet.rescan = True
            percent = "%.5s%%" % (percent)
            percent = "**{load}{synchronized_on} {percent}**".format(
                load=load, synchronized_on=synchronized_on, percent=percent
            )
        else:
            percent = synchronized_error
        message = format_msg_sync % (
            sync_status,
            wallet_block_count,
            get_status["walletBlockCount"],
            local_daemon_block_count,
            get_status["localDaemonBlockCount"],
            network_block_count,
            get_status["networkBlockCount"],
            percent,
        )
        if user_obj.wallet.rescan:
            module_wallet_rescan, text_wallet_rescan = self.language.button(
                "{wallet_rescan_update}", user_obj
            )
        else:
            module_wallet_rescan, text_wallet_rescan = self.language.button(
                "{wallet_rescan}", user_obj
            )
        buttons = [
            [
                Button.inline(text_wallet_rescan, b'{"wallet": "rescan"}'),
            ],
        ]
        return (event, message, buttons, pinned)

    async def my_wallets(
        self, event, user_obj, buttons=None, pinned=True, view_buttons=True
    ):
        """My wallets menu telegram click"""
        format_msg_my_wallets = "**%s №1:**\n`%s`\n\n\n"
        your_main_wallet = self.language.message("{your_main_wallet}", user_obj)
        wallet_address_sub = self.language.message("{wallet_address}", user_obj)
        main_wallet = await user_obj.wallet.get_wallet()
        message_ = format_msg_my_wallets % (your_main_wallet, main_wallet)
        module_create_wallet_sub, create_wallet_sub = self.language.button(
            "{create_wallet_sub}", user_obj
        )
        module_import_wallet_sub, import_wallet_sub = self.language.button(
            "{import_wallet_sub}", user_obj
        )
        module_import_wallet_view_sub, import_wallet_view_sub = self.language.button(
            "{import_wallet_view_sub}", user_obj
        )
        if view_buttons:
            buttons = [
                [
                    Button.inline(create_wallet_sub, b'{"my_wallet": "create"}'),
                    Button.inline(import_wallet_sub, b'{"my_wallet": "import"}'),
                    Button.inline(
                        import_wallet_view_sub, b'{"my_wallet": "import_view"}'
                    ),
                ],
            ]
        file_ = user_obj.create_qr(main_wallet)
        file_ = user_obj.watermark(file_, main_wallet)
        file_ = await self.upload_file(file_, file_name="images/wallet.png")
        return (event, message_, buttons, pinned, file_)

    async def my_wallets_sub(self, event, user_obj, buttons=None, pinned=False):
        format_msg_my_wallets_sub = "**%s №%s:**\n`%s`\n\n"
        note_ = self.language.message("{note}", user_obj)
        num_defferent = self.language.message("{_numbered_defferent}", user_obj)
        wallets_sub = await user_obj.wallet.get_wallet()
        if wallets_sub:
            for wallet in wallets_sub:
                message_ += format_msg_my_wallets_sub % (
                    wallet_address_sub,
                    wallets_sub.index(wallet) + 2,
                    wallet,
                )
            message_ = "{message_}\n\n__{note} {num_defferent}__".format(
                message_=message_, note=note_, num_defferent=num_defferent
            )
        return (event, message_, buttons, pinned, file_)

    async def get_mnemonic_keys(self, event, user_obj, pinned=False):
        message_ = self.language.message("{pre_get_mnemonic_keys}", user_obj)
        module_get_mnemonic_keys, get_mnemonic_keys = self.language.button(
            "{get_mnemonic_keys}", user_obj
        )
        buttons = [
            [
                Button.inline(
                    "{get_mnemonic_keys}".format(get_mnemonic_keys=get_mnemonic_keys),
                    b'{"get_mnemonic_keys": true}',
                ),
            ]
        ]
        return (event, message_, buttons, pinned)

    async def send_coin(self, event, user_obj, buttons=None, pinned=False):
        address_send = await user_obj.wallet.validate_wallet(
            user_obj.send_coin["address"]
        )
        send_coin_text = self.language.message("{send_coin_text}", user_obj)
        yes = self.language.message("{yes}", user_obj)
        no = self.language.message("{no}", user_obj)
        if address_send:
            if (
                "address" in user_obj.send_coin.keys()
                and "amount" not in user_obj.send_coin.keys()
            ):
                if hasattr(user_obj, "send_coin_msg"):
                    print("delete old message")
                    if "hash" in user_obj.send_coin:
                        payment = tuple(user_obj.send_coin["hash"])
                        await user_obj.wallet.transaction_prepare(payment=payment)
                    await self.delete_messages(event.chat_id, user_obj.send_coin_msg)
                    del user_obj.send_coin_msg
                format_send_coin_msg = "**%s**\n`%s`\n\n**%s**"
                send_coin_amount_text = self.language.message(
                    "{send_coin_amount_text}", user_obj
                )
                message_ = format_send_coin_msg % (
                    send_coin_text,
                    user_obj.send_coin["address"],
                    send_coin_amount_text,
                )
                return (event, message_, buttons, pinned)
            elif "amount" in user_obj.send_coin.keys():
                amount_text = self.language.message("{amount}", user_obj)
                if address_send["isIntegrated"]:
                    payment = (
                        address_send["actualAddress"],
                        int(user_obj.send_coin["amount"]),
                        address_send["paymentID"],
                    )
                    actual_address = self.language.message("{actual_address}", user_obj)
                    payment_id = self.language.message("{payment_id}", user_obj)
                    format_send_coin_msg = (
                        "**%s**\n`%s`\n\n**%s**:\n`%s`\n\n**%s**:\n`%s`\n\n**%s: %s**"
                    )
                    message_ = format_send_coin_msg % (
                        send_coin_text,
                        user_obj.send_coin["address"],
                        actual_address,
                        address_send["actualAddress"],
                        payment_id,
                        address_send["paymentID"],
                        amount_text,
                        user_obj.send_coin["amount"],
                    )
                else:
                    payment = (
                        user_obj.send_coin["address"],
                        int(user_obj.send_coin["amount"]),
                    )
                    format_send_coin_msg = "**%s**\n`%s`\n\n**%s: %s**"
                    message_ = format_send_coin_msg % (
                        send_coin_text,
                        user_obj.send_coin["address"],
                        amount_text,
                        user_obj.send_coin["amount"],
                    )
                wallet_transaction_prepare = await user_obj.wallet.transaction_prepare(
                    payment=payment
                )
                if wallet_transaction_prepare:
                    fee_text = self.language.message("{fee}", user_obj)
                    total_text = self.language.message("{total}", user_obj)
                    format_send_coin = "%s\n**%s: %s**\n**%s: %s**\n\n"
                    fee = str(wallet_transaction_prepare["fee"])[:-2]
                    hash_ = wallet_transaction_prepare["transactionHash"]
                    user_obj.send_coin = {
                        **user_obj.send_coin,
                        "fee": fee,
                        "hash": hash_,
                    }
                    send_hash = "%s" % (hash_)
                    buttons = [
                        [
                            Button.inline(
                                "{yes}".format(yes=yes),
                                bytes(send_hash, encoding="utf8"),
                            ),
                            Button.inline(
                                "{no}".format(no=no), b'{"send_coin": false}'
                            ),
                        ]
                    ]
                    total = int(fee) + int(user_obj.send_coin["amount"])
                    message_ = format_send_coin % (
                        message_,
                        fee_text,
                        fee,
                        total_text,
                        total,
                    )
                else:
                    error = self.language.message("{error_unknown}", user_obj)
                    message_ += "\n\n{error}\n".format(error=error)
                return (event, message_, buttons, pinned)
        else:
            format_send_coin_msg_error = "**%s**"
            validate_wallet_error = self.language.message(
                "{validate_wallet_error}", user_obj
            )
            message_ = format_send_coin_msg_error % (validate_wallet_error)
            return (event, message_, buttons, pinned)

    async def transactions(self, event, user_obj, buttons=None, pinned=False, page=0):
        transactions = await user_obj.wallet.transactions()
        if transactions:
            page_image = [
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
            incoming = self.language.message("{incoming}", user_obj)
            outcoming = self.language.message("{outcoming}", user_obj)
            transaction_text = self.language.message("{transaction_text}", user_obj)
            timestamp_text = self.language.message("{timestamp_text}", user_obj)
            amount_text = self.language.message("{amount}", user_obj)
            blockheight_text = self.language.message("{blockheight_text}", user_obj)
            hash_text = self.language.message("{hash_}", user_obj)
            wallet_address_text = self.language.message("{wallet_address}", user_obj)
            fee_text = self.language.message("{fee}", user_obj)
            payment_id_text = self.language.message("{payment_id}", user_obj)
            unlocktime_text = self.language.message("{unlocktime_text}", user_obj)
            is_coinbase_transaction_text = self.language.message(
                "{is_coinbase_transaction}", user_obj
            )
            transactions_translate = dict(
                incoming=incoming,
                outcoming=outcoming,
                transaction_text=transaction_text,
                timestamp_text=timestamp_text,
                amount_text=amount_text,
                blockheight_text=blockheight_text,
                hash_text=hash_text,
                wallet_address_text=wallet_address_text,
                fee_text=fee_text,
                payment_id_text=payment_id_text,
                unlocktime_text=unlocktime_text,
                is_coinbase_transaction_text=is_coinbase_transaction_text,
            )
            transactions_obj = []
            page_count = [0]
            count = 0
            z_list = zip(reversed(transactions), range(0, len(transactions)))
            for transaction, t in z_list:
                transaction_object = Transaction(transaction, transactions_translate)
                transactions_obj.append(transaction_object)
                count += transaction_object.get_len()
                if count >= 4096:
                    page_count.append(t)
                    count = 0
            if page_count[-1] == page_count[page]:
                transactions_page = transactions_obj[page_count[page] :]
            else:
                transactions_page = transactions_obj[
                    page_count[page] : page_count[page + 1]
                ]
            transactions_msg = "".join(x.to_string() for x in transactions_page)
            buttons = [[]]
            l = 0
            for i in range(0, len(page_count)):
                num_img = "".join([page_image[int(x)] for x in str(i + 1)])
                buttons[l].append(
                    Button.inline(
                        num_img,
                        bytes('{"page_transactions": %s}' % (i), encoding="utf8"),
                    )
                )
                if len(buttons[l]) == 5:
                    l += 1
                    buttons.append([])
            message_ = transactions_msg
        else:
            format_msg = "**%s**"
            empty_transactions = self.language.message("{empty_transactions}", user_obj)
            message_ = format_msg % (empty_transactions)
        return (event, message_, buttons, pinned)


class Transfer:
    def __init__(self, transfer, translate):
        self.__dict__ = {**transfer, **translate}

    @property
    def type_transaction(self):
        if int(self.amount) > 0:
            type_transaction = self.incoming
        else:
            type_transaction = self.outcoming
        return type_transaction

    def to_string(self):
        corn = "├ "
        corn_l = "└ "
        format_msg_transfers = "    {corn}**{wallet_address_text}:** `{address}`\n"
        format_msg_transfers += "    {corn_l}**{amount_text}: {amount}**\n"
        transfers_msg = format_msg_transfers.format(
            corn=corn, corn_l=corn_l, **self.__dict__
        )
        return transfers_msg

    def __str__(self):
        return self.to_string()


class Transaction:
    def __init__(self, transactions, translate):
        self.__dict__ = {**transactions, **translate}
        self.transfer_all = self.transfer(translate)

    def get_len(self):
        return len(self.to_string())

    def transfer(self, translate):
        # print(type(self.transfers))
        transfers = str()
        for transfer in self.transfers:
            # print(transfer)
            transfer = Transfer(transfer, translate)
            transfers += transfer.to_string()
            self.type_transaction = transfer.type_transaction
        return transfers

    def to_string(self):
        format_msg_transaction = "**{transaction_text}: {type_transaction}\n"
        format_msg_transaction += "{blockheight_text}: {blockHeight}\n"
        format_msg_transaction += "├ {timestamp_text}: {timestamp}**\n"
        format_msg_transaction += "{payment_id}"
        format_msg_transaction += "{unlocktime}"
        format_msg_transaction += "├ **{fee_text}: {fee}**\n"
        format_msg_transaction += "├ **{hash_text}:** `{hash}`\n"
        format_msg_transaction += "{transfer_all}"
        format_msg_transaction += "{is_coinbase_transaction}"
        format_msg_transaction += "{delemiter}\n"
        delemiter = "➖" * 20
        transactions_msg = format_msg_transaction.format(
            payment_id=self.payment_id,
            unlocktime=self.unlocktime,
            is_coinbase_transaction=self.is_coinbase_transaction,
            delemiter=delemiter,
            **self.__dict__
        )
        print(transactions_msg)
        return transactions_msg

    @property
    def payment_id(self):
        format_msg_payment_id = "├ **{payment_id_text}:**\n`{paymentID}`\n"
        if self.paymentID:
            payment_id = format_msg_payment_id.format(
                payment_id=payment_id_text,
                # transaction["paymentID"]
            )
        else:
            payment_id = str()
        return payment_id

    @property
    def is_coinbase_transaction(self):
        if self.isCoinbaseTransaction:
            is_coinbase = "__%s__\n" % (self.is_coinbase_transaction_text)
        else:
            is_coinbase = str()
        return is_coinbase

    @property
    def unlocktime(self):
        format_msg_unlocktime = "├ **{unlocktime_text}:** `{unlocktime}`\n"
        if self.unlockTime != 0:
            unlocktime = format_msg_unlocktime.format(
                unlocktime_text=unlocktime_text,
                unlocktime=self.timestamp + timedelta(seconds=self.unlockTime),
            )
        else:
            unlocktime = str()
        return unlocktime

    def __str__(self):
        return self.to_string()
