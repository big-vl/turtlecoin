import os
import turtlecoin_api as turtlecoin
from datetime import datetime


class Wallet:
    def __init__(self, connect, wallet):
        self.id = id(self)
        self.connect = connect
        self.wallet = str()
        self.wallet_sub = []
        self.wallet_var = wallet
        self.wallet_api = turtlecoin.wallet(connect, wallet)
        self.node_d = {"daemonHost": "94.250.255.180", "daemonPort": 10800}
        self.rescan = False

    async def start(self):
        await self.wallet_api.start()

    async def daemon_start(self):
        if self.wallet_api.daemon_start:
            return True
        else:
            await self.start()
            return True

    async def daemon_stop(self):
        await self.wallet_api.daemon_stop()
        return True

    async def start_open_wallet(self):
        if "error" not in self.wallet_api:
            await self.wallet_api.open()
            return True
        return False

    def open_wallet(self):
        return self.wallet_api.open_wallet

    async def create_wallet(self):
        await self.wallet_api.create()
        if "error" not in self.wallet_api:
            return True
        return False

    async def create_wallet_sub(self):
        await self.wallet_api.addresses(create=True)
        if "error" not in self.wallet_api:
            return True
        return False

    async def set_node(self):
        await self.wallet_api.node(self.node_d)

    async def get_status(self):
        status = await self.wallet_api.status()
        return status

    async def get_wallet_api(self, args=True):
        address = await self.wallet_api.addresses(primary=args)
        if "address" in address.keys():
            self.wallet = address["address"]
            return self.wallet
        elif "addresses" in address.keys():
            self.wallet_sub = address["addresses"]
            return self.wallet_sub
        else:
            return str()

    def wallet_exists(self):
        if "filename" in self.wallet_var.keys():
            if os.path.isfile(self.wallet_var["filename"]):
                return True
        return False

    async def wallet_exists_async(self):
        if "filename" in self.wallet_var.keys():
            if os.path.isfile(self.wallet_var["filename"]):
                return True
        return False

    async def get_mnemonic_keys(self, main=True):
        n = {}
        if main:
            wallet = await self.get_wallet()
            mnemonic = await self.wallet_api.keys_(wallet, mnemonic=True)
            private = await self.wallet_api.keys_(wallet, private=True)
            view = await self.wallet_api.keys_(wallet)
            return (
                mnemonic["mnemonicSeed"],
                private["privateSpendKey"],
                view["publicSpendKey"],
            )

    def replace_balance(self, balance_list):
        format_main_wallet_balance = "%s.%s"
        for w in balance_list:
            if "unlocked" in w.keys():
                if w["unlocked"] != 0:
                    w["unlocked"] = str(w["unlocked"])
                    s = w["unlocked"][-2:]
                    w["unlocked"] = format_main_wallet_balance % (w["unlocked"][:-2], s)
            if "locked" in w.keys():
                if w["locked"] != 0:
                    w["locked"] = str(w["locked"])
                    s = w["locked"][-2:]
                    w["locked"] = format_main_wallet_balance % (w["locked"][:-2], s)

    async def get_balances(self):
        total_balance = [await self.wallet_api.balance()]
        other_wallets_balance = await self.wallet_api.balances()
        main_wallet = await self.get_wallet()
        main_wallet_balance = [await self.wallet_api.balance(address=main_wallet)]
        for w in other_wallets_balance:
            for wa in w.keys():
                if w["address"] == main_wallet:
                    index = other_wallets_balance.index(w)

                    # break
        other_wallets_balance.pop(index)
        self.replace_balance(total_balance)
        self.replace_balance(main_wallet_balance)
        self.replace_balance(other_wallets_balance)
        return (
            total_balance[0],
            main_wallet,
            main_wallet_balance[0],
            other_wallets_balance,
        )

    async def get_wallet(self):
        main_wallet = await self.get_wallet_api(True)
        return main_wallet

    async def get_wallet_sub(self):
        sub_wallet = await self.get_wallet_api(False)
        if self.wallet in sub_wallet:
            sub_wallet.pop(sub_wallet.index(self.wallet))
        return sub_wallet

    async def validate_wallet(self, address=str()):
        if address.startswith("TRTL"):
            response = await self.wallet_api.validate(address)
            if hasattr(self.wallet_api, "error"):
                return False
            return response
        else:
            return False

    async def transactions(self):
        transactions = await self.wallet_api.transactions(True)
        if transactions["transactions"]:
            for transaction in transactions["transactions"]:
                transaction["timestamp"] = datetime.utcfromtimestamp(
                    transaction["timestamp"]
                ).strftime("%Y-%m-%d %H:%M:%S")
                transaction["fee"] = str(transaction["fee"])[:-2]
                for transfer in transaction["transfers"]:
                    transfer["amount"] = str(transfer["amount"])[:-2]
            return transactions["transactions"]
        else:
            return False

    async def transaction_prepare(self, payment=None):
        if payment:
            payment = list(payment)
            payment[1] = int("{a}00".format(a=str(payment[1])))
            payment = tuple(payment)
            response = await self.wallet_api.prepare(*payment)
            if hasattr(self.wallet_api, "error"):
                return False
            return response
        return False

    async def import_seed(self, seed_=None):
        if seed_:
            response = await self.wallet_api.import_().seed(seed_)
            if hasattr(self.wallet_api, "error"):
                return response["error"]
            return True
        return False

    async def send_hash(self, hash_=None):
        if hash_:
            response = await self.wallet_api.send(hash_)
            if hasattr(self.wallet_api, "error"):
                return False
            return response
        return False

    async def rescan_wallet(self):
        self.rescan = True
        reset = await self.wallet_api.reset("0")
        if reset:
            return True
        return False

    async def delete_transaction(self, hash_=None):
        if hash_:
            response = await self.wallet_api.prepare(hash_)
            if hasattr(self.wallet_api, "error"):
                return False
            return response
        return False

    async def close(self):
        await self.daemon_stop()

    def __repr__(self):
        return "<Wallet id={id}, open={ow}, wallet_exists={we}>".format(
            **self.__dict__, ow=self.open_wallet(), we=self.wallet_exists()
        )
