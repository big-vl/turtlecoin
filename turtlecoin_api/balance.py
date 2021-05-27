import asyncio


class BalanceMethod:
    async def balance(self, *args, **kwargs):
        if args or "address" in kwargs.keys():
            if args:
                address = args[0]
            if kwargs["address"]:
                address = kwargs["address"]
            else:
                return False
            self.method = "{server}/balance/{address}".format(**self, address=address)
            self.method_type = "GET"
            self.body = {"address": address}
            return await self.send_request()
        else:
            self.method = "{server}/balance".format(**self)
            self.method_type = "GET"
            return await self.send_request()
        return False

    async def balances(self, *args, **kwargs):
        self.method = "{server}/balances".format(**self)
        self.method_type = "GET"
        return await self.send_request()
