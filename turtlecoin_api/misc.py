class MiscMethod:
    async def status(self, *args, **kwargs):
        self.method = "{server}/status".format(**self)
        self.method_type = "GET"
        return await self.send_request()

    async def reset(self, *args, **kwargs):
        if args:
            if isinstance(args[0], int) or args[0].isdigit():
                scan_height = int(args[0])
            else:
                return False
        elif isinstance(kwargs["scanHeight"], int) or "scanHeight" in kwargs:
            if kwargs["scanHeight"].isdigit():
                scan_height = int(kwargs["scanHeight"])
            else:
                return False
        else:
            scan_height = 0
        self.method_type = "PUT"
        self.method = "{server}/reset".format(**self)
        self.body = {"scanHeight": scan_height}
        return await self.send_request()
