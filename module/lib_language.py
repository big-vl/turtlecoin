import asyncio
import sqlite3
from googletrans import Translator
from abc import ABC, abstractmethod, abstractproperty


class AbstractDB(ABC):
    @abstractmethod
    def setup_db(self):
        pass

    @abstractmethod
    def insert(self, type_, text, translate, user_obj):
        pass

    @abstractmethod
    def select(self, text):
        pass

    @abstractmethod
    def select_message(self, text, language):
        pass

    @abstractmethod
    def select_button(self, text, language):
        pass


class LiteDB(AbstractDB):
    def __init__(self):
        self.db = sqlite3.connect("ui.db")
        self.setup_db()

    def setup_db(self):
        print("Setup db...")
        cur = self.db.cursor()
        cur.execute(
            """create table if not exists ui_button_translate
        (module text, translate text, lang text);"""
        )
        cur.execute(
            """create table if not exists ui_message_translate
        (message text, translate text, lang text);"""
        )
        self.db.commit()
        cur.close()

    def select(self, text):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM ui_button_translate WHERE translate=?", (text,))
        rows = cur.fetchone()
        return rows

    def select_message(self, text, language):
        cur = self.db.cursor()
        cur.execute(
            "SELECT * FROM ui_message_translate WHERE message=? AND lang=?",
            (text, language),
        )
        rows = cur.fetchone()
        return rows

    def select_button(self, text, language):
        cur = self.db.cursor()
        cur.execute(
            "SELECT * FROM ui_button_translate WHERE module=? AND lang=?",
            (text, language),
        )
        rows = cur.fetchone()
        return rows

    def insert(self, type_, text, translate, user_obj):
        """conditions when adding to the base and adding to the base"""
        if type_ == "button":
            sql = "INSERT INTO ui_button_translate(module, translate, lang) VALUES (?, ?, ?)"
        elif type_ == "message":
            sql = "INSERT INTO ui_message_translate(message, translate, lang) VALUES (?, ?, ?)"
        if sql:
            if "translate" in translate.keys() and translate["translate"] is True:
                if user_obj.admin or user_obj.moderate:
                    cur = self.db.cursor()
                    cur.execute(sql, (text, translate["text"], user_obj.language))
                    self.db.commit()
                else:
                    print(
                        "Notify: Translate not insert user no moderate or admin:",
                        translate,
                    )
        else:
            print("System error sql")


class Language:
    def __init__(self, *args, **kwargs):
        print("Inicialization module language...")
        self.db = LiteDB()
        self.flags_list = [
            "🏳️",
            "🏴",
            "🏴‍☠️",
            "🏁",
            "🚩",
            "🏳️‍🌈",
            "🇺🇳",
            "🇦🇫",
            "🇦🇽",
            "🇦🇱",
            "🇩🇿",
            "🇦🇸",
            "🇦🇩",
            "🇦🇴",
            "🇦🇮",
            "🇦🇶",
            "🇦🇬",
            "🇦🇷",
            "🇦🇲",
            "🇦🇼",
            "🇦🇺",
            "🇦🇹",
            "🇦🇿",
            "🇧🇸",
            "🇧🇭",
            "🇧🇩",
            "🇧🇧",
            "🇧🇾",
            "🇧🇪",
            "🇧🇿",
            "🇧🇯",
            "🇧🇲",
            "🇧🇹",
            "🇧🇴",
            "🇧🇦",
            "🇧🇼",
            "🇧🇷",
            "🇮🇴",
            "🇻🇬",
            "🇧🇳",
            "🇧🇬",
            "🇧🇫",
            "🇧🇮",
            "🇰🇭",
            "🇨🇲",
            "🇨🇦",
            "🇮🇨",
            "🇨🇻",
            "🇧🇶",
            "🇰🇾",
            "🇨🇫",
            "🇹🇩",
            "🇨🇱",
            "🇨🇳",
            "🇨🇽",
            "🇨🇨",
            "🇨🇴",
            "🇰🇲",
            "🇨🇬",
            "🇨🇩",
            "🇨🇰",
            "🇨🇷",
            "🇨🇮",
            "🇭🇷",
            "🇨🇺",
            "🇨🇼",
            "🇨🇾",
            "🇨🇿",
            "🇩🇰",
            "🇩🇯",
            "🇩🇲",
            "🇩🇴",
            "🇪🇨",
            "🇪🇬",
            "🇸🇻",
            "🇬🇶",
            "🇪🇷",
            "🇪🇪",
            "🇸🇿",
            "🇪🇹",
            "🇪🇺",
            "🇫🇰",
            "🇫🇴",
            "🇫🇯",
            "🇫🇮",
            "🇫🇷",
            "🇬🇫",
            "🇵🇫",
            "🇹🇫",
            "🇬🇦",
            "🇬🇲",
            "🇬🇪",
            "🇩🇪",
            "🇬🇭",
            "🇬🇮",
            "🇬🇷",
            "🇬🇱",
            "🇬🇩",
            "🇬🇵",
            "🇬🇺",
            "🇬🇹",
            "🇬🇬",
            "🇬🇳",
            "🇬🇼",
            "🇬🇾",
            "🇭🇹",
            "🇭🇳",
            "🇭🇰",
            "🇭🇺",
            "🇮🇸",
            "🇮🇳",
            "🇮🇩",
            "🇮🇷",
            "🇮🇶",
            "🇮🇪",
            "🇮🇲",
            "🇮🇱",
            "🇮🇹",
            "🇯🇲",
            "🇯🇵",
            "🎌",
            "🇯🇪",
            "🇯🇴",
            "🇰🇿",
            "🇰🇪",
            "🇰🇮",
            "🇽🇰",
            "🇰🇼",
            "🇰🇬",
            "🇱🇦",
            "🇱🇻",
            "🇱🇧",
            "🇱🇸",
            "🇱🇷",
            "🇱🇾",
            "🇱🇮",
            "🇱🇹",
            "🇱🇺",
            "🇲🇴",
            "🇲🇬",
            "🇲🇼",
            "🇲🇾",
            "🇲🇻",
            "🇲🇱",
            "🇲🇹",
            "🇲🇭",
            "🇲🇶",
            "🇲🇷",
            "🇲🇺",
            "🇾🇹",
            "🇲🇽",
            "🇫🇲",
            "🇲🇩",
            "🇲🇨",
            "🇲🇳",
            "🇲🇪",
            "🇲🇸",
            "🇲🇦",
            "🇲🇿",
            "🇲🇲",
            "🇳🇦",
            "🇳🇷",
            "🇳🇵",
            "🇳🇱",
            "🇳🇨",
            "🇳🇿",
            "🇳🇮",
            "🇳🇪",
            "🇳🇬",
            "🇳🇺",
            "🇳🇫",
            "🇰🇵",
            "🇲🇰",
            "🇲🇵",
            "🇳🇴",
            "🇴🇲",
            "🇵🇰",
            "🇵🇼",
            "🇵🇸",
            "🇵🇦",
            "🇵🇬",
            "🇵🇾",
            "🇵🇪",
            "🇵🇭",
            "🇵🇳",
            "🇵🇱",
            "🇵🇹",
            "🇵🇷",
            "🇶🇦",
            "🇷🇪",
            "🇷🇴",
            "🇷🇺",
            "🇷🇼",
            "🇼🇸",
            "🇸🇲",
            "🇸🇹",
            "🇸🇦",
            "🇸🇳",
            "🇷🇸",
            "🇸🇨",
            "🇸🇱",
            "🇸🇬",
            "🇸🇽",
            "🇸🇰",
            "🇸🇮",
            "🇬🇸",
            "🇸🇧",
            "🇸🇴",
            "🇿🇦",
            "🇰🇷",
            "🇸🇸",
            "🇪🇸",
            "🇱🇰",
            "🇧🇱",
            "🇸🇭",
            "🇰🇳",
            "🇱🇨",
            "🇵🇲",
            "🇻🇨",
            "🇸🇩",
            "🇸🇷",
            "🇸🇪",
            "🇨🇭",
            "🇸🇾",
            "🇹🇼",
            "🇹🇯",
            "🇹🇿",
            "🇹🇭",
            "🇹🇱",
            "🇹🇬",
            "🇹🇰",
            "🇹🇴",
            "🇹🇹",
            "🇹🇳",
            "🇹🇷",
            "🇹🇲",
            "🇹🇨",
            "🇹🇻",
            "🇻🇮",
            "🇺🇬",
            "🇺🇦",
            "🇦🇪",
            "🇬🇧",
            "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
            "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
            "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
            "🇺🇸",
            "🇺🇾",
            "🇺🇿",
            "🇻🇺",
            "🇻🇦",
            "🇻🇪",
            "🇻🇳",
            "🇼🇫",
            "🇪🇭",
            "🇾🇪",
            "🇿🇲",
            "🇿🇼",
        ]

        self.language_translate = {
            "us": {
                "{welcome_bot}": "Welcome to TurtleCoin Bot!",
                "{flag_detected}": "🤷🏻‍♂️ You have chosen a flag, but we cannot determine which language to translate into, help us, send a flag and ISO-639-1 Code for translation",
                "{flag_detected_example}": "🇺🇸#us",
                "{example_text}": "Example",
                "{flag_add_thank}": "🙏🏽 Thank you, we are grateful for the development of Turtle Coin Web Wallet",
                "{select_language}": "You have selected a language",
                "{send_flag_text}": "Please send your country flag to change language",
                "{create_wallet}": "🐢 Create new wallet",
                "{create_new_user}": "📄 Create new user wallet",
                "{create_wallet_sub}": "🐢 Creates a new, random address",
                "{import_wallet_sub}": "🔐 Import wallet",
                "{import_wallet_view_sub}": "🔐👁 Import wallet (only view)",
                "{import_wallet}": "🗝 Import wallet",
                "{open_wallet}": "📂 Open wallet",
                "{my_wallets}": "🐢 My wallets",
                "{sync_status}": "🔋 Sync status",
                "{wallet_block_count}": "🔳 Blocks in the wallet",
                "{local_daemon_block_count}": "🔲 Blocks in the node",
                "{network_block_count}": "⬜️ Blocks in the network",
                "{synchronized_on}": "Synchronized on",
                "{wallet_address}": "🐢 Wallet",
                "{note}": "🧻 The note:",
                "{_numbered_defferent}": "When create new, added, importing, the numbered wallet will be different",
                "{last_update}": "🔄 Last update:",
                "{all_balance}": "💰 Balance",
                "{all_transactions}": "🧮 Transactions",
                "{message_hide}": "Auto hide message",
                "{your_main_wallet}": "🐢 Your main wallet",
                "{get_balances}": "🐢 Your main wallet:\n{main_wallet}\n\n🐢 Balance:\n{other_wallets}",
                "{get_balance_confirmed}": "💰✅ Confirmed balance:",
                "{get_balance_unconfirmed}": "💰🚫 Unconfirmed balance:",
                "{get_balance_total}": "🐢💰 **Total balance:**",
                "{get_mnemonic_keys}": "🔐 Show confidential information",
                "{error_pincode_retry}": "🧐 You entered the wrong code 3 times, your actions are blocked until",
                "{mnemonic_phrase_text}": "🔏 Mnemonic phrase",
                "{private_key_text}": "🔒 Private key",
                "{view_key_text}": "🔓 Key for view",
                "{mnemonic_attention}": "🛑 **ATTENTION: Do not share this information with anyone.**",
                "{pre_get_mnemonic_keys}": "❌👁️ **ATTENTION:** 👁️❌\nTake a look back, make sure that no one can photograph your confidential information, then confirm your intention.",
                "{send_turtlecoin}": "🐢️ Send Turtle Coin",
                "{send_turtlecoin_text}": "🐢️ Enter the address to send or send a photo with a QR code",
                "{hide_lang}": "🔽 Hide language selection",
                "{show_lang}": "🔝 Show language selection",
                "{pre_init_wallet}": "⏳ Service loading initialization...",
                "{init_wallet}": "⌛️ Service loading initialization..",
                "{init_wallet_daemon}": "🧩 Service run successful...",
                "{init_wallet_node}": "🔌️ Successful setting node...",
                "{init_wallet_node_config}": "🔌️ Node setting configuration...",
                "{create_wallet_success}": "✅ **Wallet create successful... \nPlease wait...**",
                "{create_wallet_exists}": "❌ **Wallet container cannot be re-created, use import wallet**",
                "{validate_wallet_error}": "❌ Address wallet not validate",
                "{actual_address}": "🏷 Address",
                "{payment_id}": "🆔 Payment ID",
                "{unlocktime_text}": "⏲ Unlock coin",
                "{validate_wallet}": "📤 **Address wallet validate, choice action:**",
                "{wallet_error}": "⚠ Error in wallet: {error}",
                "{unknow_wallet_error}": "⚠️ Error in wallet: Unknown",
                "{user_obj_wallet_error}": "⚠️ Error in wallet: User not detected",
                "{generate_wallet_success}": "🐢️ Your main wallet: {_addresses_list}",
                "{wallet_open_false}": "⚠️ Wallet not open, please press button Open wallet",
                "{wallet_file_exists_false}": "⚠️ Wallet not created or not import, please press button Open wallet or Import wallet",
                "{sos}": "🆘",
                "{wallet_open_security}": "Your wallet is protected by a pin code, enter the pin code:",
                "{send_coin_text}": "📤 You want to send Turtle Coin to:",
                "{send_coin_amount_text}": "↘️ Enter the amount to transfer",
                "{synchronized_error}": "⚠️ Node sync error",
                "{amount}": "💰 Amount",
                "{total}": "🧾 Total",
                "{success_transfer}": "✅ You have successfully completed the transfer",
                "{send_to}": "Send to",
                "{hash_}": "Hash",
                "{transaction_text}": "Transaction",
                "{blockheight_text}": "🔳 Block",
                "{timestamp_text}": "⏰ Date",
                "{is_coinbase_transaction}": "💎 A coinbase transaction is the first transaction in a block. It is a unique type of transaction that can be created by a miner. The miners use it to collect the block reward for their work and any other transaction fees collected by the miner are also sent in this transaction.",
                "{empty_transactions}": "♿️ Your wallet is empty",
                "{wallet_import_process}": "🔩 Import wallet proccess run",
                "{wallet_import_success}": "🧲 Your wallet has been successfully imported from the mnemonic phrase",
                "{import_wallet_text}": "🧲 To import enter mnemonic phrase",
                "{wallet_import_wrong_one_word}": "🧲 Mnemonic phrase not validate, does not exist word(s)",
                "{wallet_import_error}": "✂️ Wallet has been error imported from the mnemonic phrase",
                "{yes}": "✅ Yes",
                "{no}": "❌  No",
                "{wallet_import_send_wrong_one_word}": "❌  No, no, expect the whole phrase at once",
                "{incoming}": "📥 Incoming",
                "{outcoming}": "📤 Outcoming",
                "{no_detected_photo}": "🖼 Please send only photo for detected QR Code",
                "{no_detected_qr_trtl}": "💯 There is no wallet QR code on the photo",
                "{no_detected_qr}": "⭕️ QR code not found",
                "{wallet_open_true}": "✅ ️ Your wallet is ready, enjoy your work",
                "{wallet_rescan}": "🔁 Wallet rescan blocks",
                "{wallet_rescan_update}": "🔄 Update information",
                "{fee}": "⛏ Network Transaction Fee",
                "{error_unknown}": "🚧 Engineering works 🚧",
                "{donate}": "**Use donation to motivate me. (in developing)**\n\nMy wallet:\n",
            }
        }

    def __dictonary(self, text, lang="us"):
        if lang in self.language_translate.keys():
            text = self.language_translate[lang][text]
            return {"text": text, "translate": False}
        else:
            try:
                self.translator = Translator()
                text_ = self.translator.translate(
                    self.language_translate["us"][text], dest=lang
                )
                if self.language_translate["us"][text] == text_.text:
                    return {
                        "text": self.language_translate["us"][text],
                        "translate": False,
                    }
                return {"text": text_.text, "translate": True}
            except ValueError as error:
                text = self.language_translate["us"][text]
                return {"text": text, "translate": None}

    async def translate(self, text, user_obj):
        try:
            self.translator = Translator()
            return self.translator.translate(text, dest=user_obj.language).text
        except ValueError:
            return text

    async def check_flag(self, flag):
        self.flag = {
            "ru": "🇷🇺",
            "us": "🇺🇸",
            "ar": "🇦🇪",
            "uk": "🇺🇦",
            "de": "🇩🇪",
            "ka": "🇬🇪",
            "ja": "🇯🇵",
            "id": "🇮🇩",
            "be": "🇧🇾",
            "zh-cn": "🇨🇳",
            # "xx-pirate": "🏴‍☠️",
        }
        return flag in self.flag.values()

    def choiceLanguage(self, say, obj):
        for lang, flag in self.flag.items():
            if flag == say:
                obj.language = lang
                return lang

    async def check_button(self, text, user_obj):
        rows = self.db.select(text)
        if rows:
            module, translate, lang = rows
            if lang != user_obj.language:
                user_obj.language = lang
            return (module, translate)
        else:
            if text in self.language_translate["us"].values():
                for module, translate in self.language_translate["us"].items():
                    if translate == text:
                        return (module, translate)
            return (False, False)

    def button(self, text, user_obj):
        rows = self.db.select_button(text, user_obj.language)
        if rows:
            module, translate, lang = rows
            return (module, translate)
        else:
            translate = self.__dictonary(text, user_obj.language)
            self.db.insert("button", text, translate, user_obj)
            return (text, translate["text"])

    def message(self, text, user_obj):
        rows = self.db.select_message(text, user_obj.language)
        if rows:
            message, translate, lang = rows
            return translate
        else:
            translate = self.__dictonary(text, user_obj.language)
            self.db.insert("message", text, translate, user_obj)
            return translate["text"]
