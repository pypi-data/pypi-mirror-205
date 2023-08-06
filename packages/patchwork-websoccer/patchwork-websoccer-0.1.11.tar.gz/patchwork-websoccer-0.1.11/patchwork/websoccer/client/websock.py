# -*- coding: utf-8 -*-
import asyncio

import logging

from secrets import token_urlsafe
from typing import Protocol, Union

from patchwork.websoccer.client.base import BaseClient

try:
    from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
except ImportError:
    raise RuntimeError("Websock client requires starlette lib installed")


logger = logging.getLogger('patchwork.websoccer.client')


class WebsockClient(BaseClient):

    def __init__(self, sock: WebSocket, binary: bool, timeout: int = None):
        super().__init__()
        self._id = token_urlsafe(16)
        self._binary = binary
        self._sock = sock
        self._timeout = timeout

    @property
    def session_id(self):
        return self._id

    async def get(self) -> Union[bytes, str]:
        if self._binary:
            return await self._sock.receive_bytes()
        else:
            return await self._sock.receive_text()

    async def disconnect(self, court):
        await super().disconnect(court)
        # usually disconnect() is called when listen() completes, so socket is already
        # disconnected, but it might be also called when server is going down
        if self._sock.application_state != WebSocketState.DISCONNECTED and \
                self._sock.client_state != WebSocketState.DISCONNECTED:
            await self._sock.close(1001)

    async def listen(self):
        while True:
            try:
                data = await asyncio.wait_for(self.get(), timeout=self._timeout)
            except TimeoutError:
                # no data in given keep alive period, close connection by sending cutoff close code
                await self._sock.close(code=1013)
                break
            except WebSocketDisconnect:
                logger.debug(f"{self}: connection closed, get returned EOF")
                break

            try:
                await self.handle(data)
            except PermissionError:
                logger.info(f"{self}: connection closed, operation not permitted")
                await self._sock.close(code=1008)
                break
            except ValueError as e:
                logger.info(f"{self}: unprocessable request: {e}")
                await self._sock.close(code=1007)
                break
            except Exception as e:
                logger.warning(f"{self}: request handler failed: {e.__class__.__name__}({e})")
                await self._sock.close(code=1011)
                break

    async def send(self, data: Union[bytes, str]):
        if self._binary:
            if isinstance(data, str):
                raise ValueError('Unable to send text data over binary socket')
            await self._sock.send_bytes(data)
        else:
            if isinstance(data, bytes):
                raise ValueError('Unable to send binary data over text socket')
            await self._sock.send_text(data)

    async def handle(self, data: Union[bytes, str]):
        raise NotImplementedError()
