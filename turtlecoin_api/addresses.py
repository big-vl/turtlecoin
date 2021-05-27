import asyncio


class AddressesMethod:
    async def addresses(self, *args, **kwargs):
        self.method_type = "GET"
        if len(args) == 1:
            if isinstance(args[0], bool):
                if args[0]:
                    self.method = "{server}/addresses/primary".format(**self)
                    return await self.send_request()
                else:
                    self.method = "{server}/addresses".format(**self)
                    return await self.send_request()
        elif len(args) == 2:
            if args[0].isdigit():
                self.body = {"scanHeight": 0}
                if int(args[0]) > 0:
                    self.body = {"scanHeight": kwargs["scanHeight"]}
            else:
                return False
            if isinstance(args[1], str):
                self.method = "{server}/addresses/import".format(**self)
                self.method_type = "POST"
                self.body = {**self.body, "privateSpendKey": args[1]}
                return await self.send_request()
            else:
                return False
        elif len(args) == 0 and bool(len(kwargs.keys())):
            self.method = "{server}/addresses".format(**self)
            if "primary" in kwargs.keys():
                if kwargs["primary"]:
                    self.method = "{server}/addresses/primary".format(**self)
                    return await self.send_request()
                else:
                    self.method = "{server}/addresses".format(**self)
                    return await self.send_request()
            elif "create" in kwargs.keys():
                if kwargs["create"]:
                    self.method = "{server}/addresses/create".format(**self)
                    self.method_type = "POST"
                    return await self.send_request()
                else:
                    return False
            elif "privateSpendKey" or "publicSpendKey" in kwargs.keys():
                self.body = {"scanHeight": 0}
                if "scanHeight" in kwargs.keys():
                    if isinstance(kwargs["scanHeight"], int):
                        if kwargs["scanHeight"] > 0:
                            self.body = {"scanHeight": kwargs["scanHeight"]}
                    if isinstance(kwargs["scanHeight"], str):
                        if kwargs["scanHeight"].isdigit():
                            if int(kwargs["scanHeight"]) > 0:
                                self.body = {"scanHeight": kwargs["scanHeight"]}
                if "privateSpendKey" in kwargs.keys():
                    self.method = "{server}/addresses/import".format(**self)
                    self.method_type = "POST"
                    self.body = {
                        **self.body,
                        "privateSpendKey": kwargs["privateSpendKey"],
                    }
                    return await self.send_request()
                elif "publicSpendKey" in kwargs.keys():
                    self.method = "{server}/addresses/import/view".format(**self)
                    self.method_type = "POST"
                    self.body = {
                        **self.body,
                        "publicSpendKey": kwargs["publicSpendKey"],
                    }
                    return await self.send_request()
        return False

    async def validate(self, *args, **kwargs):
        if args or "address" in kwargs.dict():
            if args[0].startswith("TRTL"):
                address = args[0]
            elif "address" in kwargs.dict():
                address = kwargs["address"]
            self.method = "{server}/addresses/validate".format(**self)
            self.method_type = "POST"
            self.body = {"address": address}
            return await self.send_request()
