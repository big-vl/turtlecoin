import asyncio


class NodeMethod:
    async def node(self, *args, **kwargs):
        self.method = "{server}/node".format(**self)
        if args:
            self.body = args[0]
            self.method_type = "PUT"
            return await self.send_request()
        else:
            self.method_type = "GET"
            return await self.send_request()
        return False
