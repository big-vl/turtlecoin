from telethon import Button


class Buttons:
    def buttons_menu(self, user_obj):
        if user_obj.wallet.wallet_exists():
            module_get_mnemonic_keys, get_mnemonic_keys = self.language.button(
                "{get_mnemonic_keys}", user_obj
            )
            module_send_turtlecoin, send_turtlecoin = self.language.button(
                "{send_turtlecoin}", user_obj
            )
            module_sos, sos = self.language.button("{sos}", user_obj)
            module_all_balance, balance = self.language.button(
                "{all_balance}", user_obj
            )
            module_all_transactions, all_transactions = self.language.button(
                "{all_transactions}", user_obj
            )
            module_my_wallets, my_wallets = self.language.button(
                "{my_wallets}", user_obj
            )
            module_sync_status, sync_status = self.language.button(
                "{sync_status}", user_obj
            )
            buttons = [
                [
                    Button.text(send_turtlecoin, resize=True, single_use=False),
                ],
                [
                    Button.text(all_transactions, resize=True, single_use=False),
                ],
                [
                    Button.text(balance, single_use=False),
                    Button.text(my_wallets, single_use=False),
                ],
                [
                    Button.text(get_mnemonic_keys, resize=True, single_use=False),
                    Button.text(sync_status, resize=True, single_use=False),
                    Button.text(sos, single_use=False),
                ],
            ]
        else:
            module_create_wallet, create_wallet = self.language.button(
                "{create_wallet}", user_obj
            )
            module_import_wallet, import_wallet = self.language.button(
                "{import_wallet}", user_obj
            )
            buttons = [
                [
                    Button.text(create_wallet, resize=True, single_use=False),
                    # ],
                    # [
                    Button.text(import_wallet, resize=True, single_use=False),
                ]
            ]
        if not user_obj.hide_lang:
            image = {
                "flag_ru": "🇷🇺",
                "flag_us": "🇺🇸",
                "flag_ae": "🇦🇪",
                "flag_ua": "🇺🇦",
            }
            module_hide_lang, hide_lang = self.language.button("{hide_lang}", user_obj)
            buttons.append(
                [
                    Button.text(
                        "{flag_ru}".format(**image), resize=True, single_use=False
                    ),
                    Button.text(
                        "{flag_us}".format(**image), resize=True, single_use=False
                    ),
                    Button.text(
                        "{flag_ae}".format(**image), resize=True, single_use=False
                    ),
                    Button.text(
                        "{flag_ua}".format(**image), resize=True, single_use=False
                    ),
                    Button.text(hide_lang, resize=True, single_use=False),
                ]
            )
        else:
            module_show_lang, hide_lang = self.language.button("{show_lang}", user_obj)
            buttons.append(
                [
                    Button.text(hide_lang, resize=True, single_use=False),
                ]
            )
        return buttons

    def buttons_pincode_panel(self, user_obj):
        number = {
            "b1": "1️⃣",
            "b2": "2️⃣",
            "b3": "3️⃣",
            "b4": "4️⃣",
            "b5": "5️⃣",
            "b6": "6️⃣",
            "b7": "7️⃣",
            "b8": "8️⃣",
            "b9": "9️⃣",
            "b0": "0️⃣",
            "bY": "✅",
            "bN": "❎",
        }
        keyboard = [
            [
                Button.inline("{b1}".format(**number), b'{"pin": "b1"}'),
                Button.inline("{b2}".format(**number), b'{"pin":"b2"}'),
                Button.inline("{b3}".format(**number), b'{"pin":"b3"}'),
            ],
            [
                Button.inline("{b4}".format(**number), b'{"pin": "b4"}'),
                Button.inline("{b5}".format(**number), b'{"pin":"b5"}'),
                Button.inline("{b6}".format(**number), b'{"pin":"b6"}'),
            ],
            [
                Button.inline("{b7}".format(**number), b'{"pin": "b7"}'),
                Button.inline("{b8}".format(**number), b'{"pin":"b8"}'),
                Button.inline("{b9}".format(**number), b'{"pin":"b9"}'),
            ],
            [
                Button.inline("{bN}".format(**number), b'{"pin": "bN"}'),
                Button.inline("{b0}".format(**number), b'{"pin":"b0"}'),
                Button.inline("{bY}".format(**number), b'{"pin":"bY"}'),
            ],
        ]
        return keyboard
