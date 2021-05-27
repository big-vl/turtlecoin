import requests
import asyncio
import re
import subprocess
import os
from shlex import quote
from requests.exceptions import ConnectionError, ReadTimeout
from urllib3.exceptions import ReadTimeoutError


class TurtleCoinDaemon:
    async def subprocessCreate(self):
        cmd = self.cmd
        proc = await asyncio.create_subprocess_shell(
            "{cmd} -p {port} -r {passw}".format(
                cmd=quote(cmd),
                port=quote(self.port),
                passw=quote(self.headers["X-API-KEY"]),
            ),
            stdout=asyncio.subprocess.PIPE,
        )
        # proc = await asyncio.create_subprocess_exec(
        # cmd, '-p', str(quote(self.port)), '-r', str(quote(self.headers["X-API-KEY"])),
        # stdout=subprocess.PIPE,
        # )
        return proc

    async def start(self):
        if not hasattr(self, "cmd"):
            self.error = 'ERROR: Cannot be started without specifying a parameter "cmd"'
            if self.debug:
                print(self.error)
            return self
        if not os.path.isfile(self.cmd):
            self.error = "ERROR: Cannot be started without is not file"
            if self.debug:
                print(self.error)
            return self
        if self.debug:
            print(
                "START DAEMON",
                id(self),
                "PORT:",
                self.port,
                "PASSWORD:",
                self.headers["X-API-KEY"],
            )
        proc = await self.subprocessCreate()
        while True:
            data = await proc.stdout.readline()
            line = data.decode("utf-8").rstrip()
            if (
                line
                == "The api has been launched on {schema}://{server_host}:{port}.".format(
                    schema=self.schema, server_host=self.server_host, port=self.port
                )
            ):
                if self.debug:
                    print(
                        "CREATE DAEMON:",
                        proc,
                        "START API SERVER: {schema}://{server_host}:{port}".format(
                            schema=self.schema,
                            server_host=self.server_host,
                            port=self.port,
                        ),
                    )
                    print("*" * 50)
                self.daemon_start = True
                break
            elif (
                line
                == "Failed to start RPC server: The host and port specified are already in use."
            ):
                if self.debug:
                    print("CREATE DAEMON (port use) (retry):", self.port)
                self.port = str(int(self.port) + 1)
                self.server = "{schema}://{server_host}:{port}".format(
                    schema=self.schema, server_host=self.server_host, port=self.port
                )
                proc = await self.subprocessCreate()
        print("*" * 50)
        self.daemon = proc
        return self

    async def daemon_stop(self):
        if hasattr(self, "open_wallet"):
            if self.open_wallet:
                print("Close wallet...")
                self.close()
        else:
            print("Note: The demon was launched without a wallet")
        if hasattr(self, "daemon"):
            self.daemon_start = False
            self.daemon.terminate()
            print("Daemon stop")
        else:
            print("Daemon not run")


class WalletAPIConnect(dict, TurtleCoinDaemon):
    def __init__(self, *args, **kwargs):
        super(WalletAPIConnect, self).__init__(*args, **kwargs)
        self.__dict__ = self
        if not hasattr(self, "debug"):
            self.debug = True
        if not hasattr(self, "server"):
            print('ERROR: Attribute "server" not found')
            if self.debug:
                print("Connect var:", args)
        if hasattr(self, "port"):
            print('ERROR: Attribute "port" not found')
        if not hasattr(self, "password"):
            print('ERROR: Attribute "password" not found')
        else:
            self.headers = {"X-API-KEY": self.password}
        if hasattr(self, "timeout"):
            if isinstance(self.timeout, int):
                if self.timeout < 0:
                    print('ERROR: "timeout" cannot be negative number')
            elif isinstance(self.timeout, str):
                self.timeout = int(self.timeout)
        self.retry_connect = 5
        connect_cons_ = re.findall(
            r"(http|https):\/\/([A-Za-z.0-9]+):(\d*)", self.server
        )
        if len(connect_cons_[0]) != 3:
            print("ERROR: Wrong parametr server")
        else:
            self.schema, self.server_host, self.port = connect_cons_[0]
            if not self.port:
                print("ERROR: Port is empty in server")
            if not self.schema:
                print("ERROR: http or https schemas in server")
        if self.debug:
            print("WalletAPIConnect (dir)", dir(self))

    async def request(self):
        try:
            if self.method_type == "GET":
                response = requests.get(
                    self.method, headers=self.headers, timeout=self.timeout
                )
            elif self.method_type == "DELETE":
                response = requests.delete(
                    self.method, headers=self.headers, timeout=self.timeout
                )
                if self.debug:
                    print("DELETE", self.method, self.body, self.headers, self.timeout)
                    print(
                        "DELETE ANSWER",
                        self.method,
                        response.status_code,
                        response.content,
                    )
                    print("*" * 50)
            elif self.method_type == "PUT":
                response = requests.put(
                    self.method,
                    json=self.body,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                if self.debug:
                    print("PUT", self.method, self.body, self.headers, self.timeout)
                    print(
                        "PUT ANSWER:",
                        self.method,
                        response.status_code,
                        response.content,
                    )
                    print("*" * 50)
            elif self.method_type == "POST":
                response = requests.post(
                    self.method,
                    json=self.body,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                if self.debug:
                    print("POST", self.method, self.body, self.headers, self.timeout)
                    print(
                        "POST ANSWER:",
                        self.method,
                        response.status_code,
                        response.content,
                    )
                    print("*" * 50)
            else:
                self.error = "ERROR: METHOD NOT AWAIBLE"
                if self.debug:
                    print(self.error)
                return False
            if hasattr(self, "error"):
                del self.error
            if hasattr(response, "status_code"):
                self.response = response
                if response.status_code == 200:
                    if response.content:
                        if "error" in response.json():
                            error = response.json()
                            self.error = error["error"]["message"]
                            if self.debug:
                                print("ERROR:", error["error"]["message"])
                            return False
                    return True
                elif response.status_code in [201, 202]:
                    return True
                elif response.status_code == 404:
                    self.error = "ERROR: Method not found [404] {method}".format(
                        method=self.method.format(**self)
                    )
                    if self.debug:
                        print(self.error)
                    return False
                else:
                    if self.debug:
                        print(
                            "Error status_code:",
                            response.status_code,
                            self.method,
                            self.body,
                            self.headers,
                            self.timeout,
                        )
                    error = response.json()
                    self.error = error["error"]["message"]
                    return False
        except ConnectionError:
            self.error = "ERROR: Server is not connected"
            if self.debug:
                print(self.error)
            return self
        except ReadTimeout:
            self.retry_connect -= 1
            s = self.request()
            if self.retry_connect == 2:
                if hasattr(self, "daemon"):
                    if self.debug:
                        print(
                            "Daemon restart, initiator requests.exceptions.ReadTimeout"
                        )
                    self.daemon.terminate()
                    self.start()
            if self.retry_connect == 0:
                self.error = "ERROR: Response requests.ReadTimeout reload daemon..."
                self.retry_connect = 5
            return self
        except ReadTimeoutError:
            if hasattr(self, "daemon"):
                self.error = "ERROR: Response ReadTimeoutError reload daemon..."
                if self.debug:
                    print(self.error)
                self.daemon.terminate()
                self.start()
            else:
                self.error = "ERROR: Response ReadTimeoutError"
            return self

    async def send_request(self):
        if await self.check_open_wallet():
            result = await self.request()
            if result:
                if self.response.content:
                    return self.response.json()
                elif self.response.status_code == 200:
                    return True
            return False
