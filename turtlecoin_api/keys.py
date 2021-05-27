import asyncio


class KeysMethod:
    async def keys_(self, *args, **kwargs):
        if args:
            self.method_type = "GET"
            address = args[0]
            if "mnemonic" in kwargs.keys():
                if kwargs["mnemonic"]:
                    if address.startswith("TRTL"):
                        self.method = "{server}/keys/mnemonic/{address}".format(
                            **self, address=address
                        )
            if "private" in kwargs.keys():
                if kwargs["private"]:
                    self.method = "{server}/keys/{address}".format(
                        **self, address=address
                    )
            return await self.send_request()
        else:
            self.method = "{server}/keys".format(**self)
            self.method_type = "GET"
            return await self.send_request()
        # error = """{s} ERROR {s}""".format(s="-"*25)
        # error += """Read keys_() documentation, empty parameters."""
        # error += """Your args: {args}""".format(args=args)
        # error += """Your kwargs: {kwargs}""".format(kwargs=kwargs)
        # if self.debug:
        # print(error)
        # # self.error = error
        # return self
        # return False
