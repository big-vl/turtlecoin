import asyncio
import subprocess
from .connect import WalletAPIConnect, TurtleCoinDaemon
from .node import NodeMethod
from .addresses import AddressesMethod
from .transactions import TransactionsMethod
from .keys import KeysMethod
from .balance import BalanceMethod
from .misc import MiscMethod


class WalletMethod(
    WalletAPIConnect,
    NodeMethod,
    MiscMethod,
    AddressesMethod,
    TransactionsMethod,
    KeysMethod,
    BalanceMethod,
):
    def __init__(self, connect, wallet=dict()):
        super(WalletMethod, self).__init__(**connect)
        self.method = "{server}/wallet".format(**self)
        self.method_type = "POST"
        self.body = wallet
        self.open_wallet = False
        self.daemon_start = False
        if self.debug:
            print("*" * 25, "START", "*" * 25)
            print("CREATE CLASS WalletMethod (dir):", id(self), dir(self))
            print("CLASS WalletMethod (headers):", self.headers)
            print("CLASS WalletMethod (connect):", connect)
            print("*" * 25, "END", "*" * 25)

    async def open(self):
        self.method = "{server}/wallet/open".format(**self)
        if await self.required_fields("wallet"):
            r = await self.request()
            if "error" not in self:
                self.open_wallet = True
        return self

    def __setattr__(self, *args, **kwargs):
        super(WalletMethod, self).__setattr__(*args, **kwargs)

        async def send_():
            if "wallet" in self.method and self.method_type != "DELETE":
                c = None
                r = await self.request()
                if r:
                    print("Open wallet success!")
                    if hasattr(self, "body"):
                        del self.body
                else:
                    self.open_wallet = False
            if hasattr(self, "close_wallet"):
                if self.close_wallet:
                    c = await self.close_()

        name, value = args

    def import_(self, *args, **kwargs):
        if len(args) == 1:
            scanHeight = args[0]
        elif "scanHeight" in kwargs.keys():
            scanHeight = kwargs["scanHeight"]
        else:
            scanHeight = 0
        self.body = {**self.body, "scanHeight": scanHeight}
        self.method = "{server}/import".format(**self)
        return self

    async def view(self, *args, **kwargs):
        self.method = "{server}/wallet/import/view".format(**self)
        self.body = {**kwargs, **self.body}
        if await self.use_import():
            if await self.required_fields("wallet"):
                if (
                    "privateViewKey" in self.body.keys()
                    and "address" in self.body.keys()
                ) or len(args) == 2:
                    if len(args) == 2:
                        self.body["privateViewKey"] = args[0]
                        self.body["address"] = args[1]
                    if self.body["address"].startswith("TRTL"):
                        self.open_wallet = True
                        r = await self.request()
                        return self
                    else:
                        self.error = "ERROR: Wrong address TurtleCoin"
                        if self.debug:
                            print(self.error)
                else:
                    self.error = 'ERROR: Not set "privateViewKey" and "privateSpendKey"'
                    if self.debug:
                        print(self.error)
        return self

    async def key(self, *args, **kwargs):
        self.method = "{server}/wallet/import/key".format(**self)
        self.body = {**kwargs, **self.body}
        if await self.use_import():
            if await self.required_fields("wallet"):
                if (
                    "privateViewKey" in self.body.keys()
                    and "privateSpendKey" in self.body.keys()
                ) or len(args) == 2:
                    if len(args) == 2:
                        self.body["privateViewKey"] = args[0]
                        self.body["privateSpendKey"] = args[1]
                    self.open_wallet = True
                    r = await self.request()
                else:
                    self.error = (
                        'ERROR: Not set "privateViewKey" or/and "privateSpendKey"'
                    )
                    if self.debug:
                        print(self.error)
        return self

    async def seed(self, mnemonic=None):
        self.method = "{server}/wallet/import/seed".format(**self)
        if await self.use_import():
            if await self.required_fields("wallet"):
                if isinstance(mnemonic, str) or isinstance(mnemonic, list):
                    if isinstance(mnemonic, str):
                        mnemonic = mnemonic.split()
                    if len(mnemonic) == 25:
                        if isinstance(mnemonic, list):
                            mnemonic = " ".join(mnemonic)
                        self.body = {**self.body, "mnemonicSeed": mnemonic}
                        self.open_wallet = True
                        r = await self.request()
                    else:
                        self.error = (
                            "WARNING: Mnemonic the phrase wrong length, set 25 words"
                        )
                        if self.debug:
                            print(self.warning)
                else:
                    self.error = "ERROR: Mnemonic is not set"
                    if self.debug:
                        print(self.error)
        return self

    async def create(self):
        self.method = "{server}/wallet/create".format(**self)
        if await self.required_fields("wallet"):
            self.open_wallet = True
            r = await self.request()
            return self
        if self.debug:
            print("CREATE WALLET:", self)
        return self

    async def close(self):
        self.method = "{server}/wallet".format(**self)
        self.method_type = "DELETE"
        self.open_wallet = False
        del self.body
        r = await self.request()
        return self

    async def required_fields(self, fields):
        fields_ = {
            "wallet": {
                "fields": ["filename", "password"],
                "message": 'ERROR: Missing wallet "filename" or "password"',
            },
            "key": {
                "fields": ["privateViewKey", "privateSpendKey"],
                "message": 'ERROR: Missing wallet "privateViewKey", "privateSpendKey"',
            },
        }
        for f in fields_[fields]["fields"]:
            if f not in self.body:
                self.error = fields_[fields]["message"]
                if self.debug:
                    print(self.error)
                return False
        return True

    async def check_open_wallet(self):
        if self.open_wallet:
            return True
        else:
            self.error = "Wallet is not open see log"
            if self.debug:
                print(self.error)
            return False

    async def use_import(self):
        if "scanHeight" not in self.body.keys():
            self.error = (
                "ERROR: .seed(), .key(), .view() method is called through import"
            )
            if self.debug:
                print(self.error)
            return False
        else:
            return True
