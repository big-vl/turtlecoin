import asyncio


class TransactionsMethod:
    async def transactions(self, *args, **kwargs):
        # if "get" in kwargs.keys() or len(args) == 1:
        if True in kwargs.values() or len(args) == 1:
            self.method = "{server}/transactions".format(**self)
            self.method_type = "GET"
            return await self.send_request()
        else:
            error = """{s} ERROR {s}\n""".format(s="-" * 25)
            error += """Read transactions() documentation, empty parameters.\n"""
            error += """Your args: {args}\n""".format(args=args)
            error += """Your kwargs: {kwargs}\n""".format(kwargs=kwargs)
            if self.debug:
                print(error)
            # self.error = error
        return self

    async def prepare(self, *args, **kwargs):
        try:
            if args or kwargs:
                if len(args) == 1 or "hash_" in kwargs:
                    if "hash_" in kwargs:
                        hash_ = kwargs["hash"]
                    else:
                        hash_ = args[0]
                    self.method = "{server}/transactions/prepare/{hash_}".format(
                        **self, hash_=hash_
                    )
                    self.method_type = "DELETE"
                elif (len(args) == 2 or len(args) == 3) or (
                    "destination" in kwargs and "amount" in kwargs
                ):
                    self.method = "{server}/transactions/prepare/basic".format(**self)
                    self.method_type = "POST"
                    if "destination" in kwargs:
                        destination = {"destination": kwargs["destination"]}
                    else:
                        destination = {"destination": args[0]}
                    if "amount" in kwargs:
                        amount = {"amount": kwargs["amount"]}
                    else:
                        amount = {"amount": args[1]}
                    if "paymentID" in kwargs:
                        paymentid = {"amount": kwargs["paymentID"]}
                    else:
                        paymentid = {}
                        if len(args) == 3:
                            paymentid = {"paymentID": args[2]}
                    self.body = {**destination, **amount, **paymentid}
                else:
                    return False
                return await self.send_request()
            return self
        except UnboundLocalError:
            error = """{s} ERROR {s}\n""".format(s="-" * 25)
            error += """Read prepare() documentation, wrong parameters.\n"""
            error += """Your args: {args}\n""".format(args=args)
            error += """Your kwargs: {kwargs}\n""".format(kwargs=kwargs)
            # self.error = error
            if self.debug:
                print(error)
            return self

    async def send(self, *args, **kwargs):
        if args:
            if len(args) == 1:
                self.method = "{server}/transactions/send/prepared".format(**self)
                self.method_type = "POST"
                self.body = {"transactionHash": args[0]}
                return await self.send_request()
            else:
                error = """{s} ERROR {s}\n""".format(s="-" * 25)
                error += """Read send() documentation, wrong parameters.\n"""
                error += """Your args: {args}\n""".format(args=args)
                error += """Your kwargs: {kwargs}\n""".format(kwargs=kwargs)
                # self.error = error
                if self.debug:
                    print(error)
                return self
        else:
            error = """{s} ERROR {s}\n""".format(s="-" * 25)
            error += """Read send() documentation, empty parameters.\n"""
            error += """Your args: {args}\n""".format(args=args)
            error += """Your kwargs: {kwargs}\n""".format(kwargs=kwargs)
            # self.error = error
            if self.debug:
                print(error)
        return self
