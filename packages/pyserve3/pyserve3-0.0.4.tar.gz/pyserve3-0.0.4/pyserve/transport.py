"""
AsyncIO Implementations of session-based servers
"""
import asyncio
from dataclasses import dataclass, field
from typing import Type, Optional, Dict, Any

from .abc import RawAddr, Address, Writer, Session

#** Variables **#
__all__ = ['UdpProtocol', 'TcpProtocol']

#** Classes **#

@dataclass
class UdpWriter(Writer):
    addr:      Address
    transport: asyncio.DatagramTransport
    
    def write(self, data: bytes, addr: Optional[Address] = None):
        self.transport.sendto(data, addr or self.addr)

    def close(self):
        self.transport.close()

    def is_closing(self) -> bool:
        return self.transport.is_closing()

@dataclass
class BaseProtocol:
    factory:   Type[Session]
    args:      tuple           = field(default_factory=tuple)
    kwargs:    Dict[str, Any]  = field(default_factory=dict)

    def test_factory(self):
        """validate session can be generated w/ args and kwargs"""
        self.factory(*self.args, **self.kwargs)

    def set_timeout(self, timeout: int, tport: asyncio.Transport):
        """implement timeout handling for async servers"""
        # generate async expiration function
        async def expire():
            await asyncio.sleep(timeout)
            if not tport.is_closing():
                tport.abort()
        # spawn future to kill transport
        loop = asyncio.get_event_loop()
        loop.create_task(expire())

class UdpProtocol(BaseProtocol, asyncio.DatagramTransport):
 
    def connection_made(self, transport: asyncio.DatagramTransport):
        """"""
        # handle modifying socket and making changes for handling
        self.transport = transport
 
    def datagram_received(self, data: bytes, addr: RawAddr):
        """"""
        # generate session w/ attributes and notify on connection-made
        address      = Address(*addr)
        writer       = UdpWriter(address, self.transport)
        self.session = self.factory(*self.args, **self.kwargs)
        self.session.connection_made(address, writer)
        self.session.data_recieved(data)

    def connection_lost(self, err: Optional[Exception]):
        """"""
        self.session.connection_lost(err)

@dataclass
class TcpProtocol(BaseProtocol, asyncio.Protocol):
    timeout: Optional[int] = None
   
    def connection_made(self, transport: asyncio.Transport):
        """"""
        # collect attributes and prepare socket for session
        address = Address(*transport.get_extra_info('peername'))
        # handle modifying socket and making changes for handling
        if self.timeout is not None:
            self.set_timeout(self.timeout, transport)
        # generate session w/ attributes and notify on connection-made
        self.session = self.factory(*self.args, **self.kwargs)
        self.session.connection_made(address, transport)

    def data_received(self, data: bytes):
        """"""
        self.session.data_recieved(data)

    def connection_lost(self, err: Optional[Exception]):
        """"""
        self.session.connection_lost(err)
