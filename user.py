import random
import uuid
import qrcode
import io
import numpy as np
from datetime import datetime, timedelta
from wallet import Wallet
from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode


class User:
    def __init__(self, user_id=int(), lang="us"):
        super().__init__()
        self.id = id(self)
        self.language = lang
        self.user_id = user_id
        self.admin = True
        self.moderate = False
        self.hide_lang = False
        self.load_wallet = None
        self.pincode = ""
        self.pincode_retry = 3
        self.auth = False
        self.send_coin = {}
        self.counter_message = set()
        self.counter_message_break = set()
        self.wallet_var = {
            "filename": "wallet/%s.wallet" % (self.user_id),
            "password": "123456",
        }
        self.connect_cons = {
            "server": "http://127.0.0.1:{port}".format(port=random.randint(8100, 8300)),
            "password": "{passw}".format(passw=self.passw()),
            "timeout": "10",
            "cmd": "./wallet-api",
        }
        self.wallet = Wallet(self.connect_cons, self.wallet_var)
        self.command = None
        self.last_visit = datetime.today()
        self.block_time = dict(hours=24)
        self.watermark_text_bot = "Telegram: @TurtleCoin_bot"
        self.active_time = dict(minutes=10)

    async def run_command(self):
        await self.command()

    def passw(self):
        return uuid.uuid4().hex

    def security_pincode(self, num=None):
        print(
            "num keys",
            num,
            len(self.pincode),
            (len(self.pincode) == 4),
            ("bY" in num.values()),
            self,
        )
        if "pin" in num.keys():
            if not hasattr(self, "pincode_tmp"):
                self.pincode_tmp = str()
            if self.pincode_retry <= 0 and self.block_wallet() > datetime.today():
                return {"error": "pincode_retry"}
            if "bN" in num.values():
                del self.pincode_tmp
                if self.block_wallet() > datetime.today():
                    self.pincode_retry = 3
                return {"button": "bN"}
            if (self.pincode == self.pincode_tmp and "bY" in num.values()) or (
                self.auth
            ):
                self.auth = True
                self.last_visit = datetime.now()
                return {"success": True}
            elif self.pincode != self.pincode_tmp and "bY" in num.values():
                del self.pincode_tmp
                self.pincode_retry -= 1
                # else:
                self.last_visit = datetime.now()
                return {"error": "pincode"}
            if num["pin"][-1].isdigit():
                self.pincode_tmp += num["pin"][-1]
        else:
            return {"error": "no_pincode"}

    def pincode_len(self):
        if hasattr(self, "pincode_tmp"):
            ll = "🟢" * len(self.pincode_tmp)
            return ll
        else:
            return str()

    def block_wallet(self):
        return self.last_visit + timedelta(**self.block_time)

    def block_wallet_str(self):
        return datetime.strftime(self.block_wallet(), "%Y-%m-%d %H:%M:%S")

    def create_qr(self, data):
        img_io = io.BytesIO()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=5,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(img_io)
        return img_io.getvalue()

    def watermark(self, img, text):
        qr_code = self.read_qr(img)
        img_buffer = io.BytesIO(img)
        img = io.BytesIO(img)
        img = Image.open(img)
        width, height = img.size
        fnt = ImageFont.truetype("font/font.ttf", 18)
        qr_code = qr_code[0]
        text_list = []
        for t in range(0, width, 2):
            font_width, font_height = fnt.getsize(text[:t])
            if font_width >= width - (qr_code.rect.left * 2):
                text_list.append(text[:t])
                text_list.append(text[t:])
                break
        draw = ImageDraw.Draw(img)
        padding = 4
        for text in text_list:
            font_width, font_height = fnt.getsize(text)
            draw.text(((width - font_width) / 2, padding), text, font=fnt)
            padding += font_height
        font_width, font_height = fnt.getsize(self.watermark_text_bot)
        draw.text(
            (qr_code.rect.left, height - (font_height * 2)),
            self.watermark_text_bot,
            font=fnt,
        )
        img_logo = Image.open("images/logo.png")
        correct = 3
        size = [round(((10 * s) / 100.0)) + correct for s in img.size]
        img_logo = img_logo.resize(size, Image.BOX)
        correct = 0
        offset = [
            round(((i / 2) - (l / 2))) - correct
            for l, i in zip(img_logo.size, img.size)
        ]
        img.paste(img_logo, offset)
        resize = [round((98 * s) / 100) for s in img.size]
        img = img.resize(resize, Image.BICUBIC)
        img.save(img_buffer, format="PNG")
        return img_buffer.getvalue()

    def read_qr(self, image):
        image = io.BytesIO(image)
        image = Image.open(image)
        data = decode(image)
        if len(data) > 0:
            return data
        return False

    def deactive(self):
        last_visit = self.last_visit + timedelta(**self.active_time)
        if last_visit < datetime.today():
            self.auth = False
            if not self.wallet.rescan:
                self.wallet.daemon_stop()

    def __repr__(self):
        return "<User id={id}, tg_user_id={user_id}, language={language}, last_visit={last_visit}, wallet={wallet}>".format(
            **self.__dict__
        )
