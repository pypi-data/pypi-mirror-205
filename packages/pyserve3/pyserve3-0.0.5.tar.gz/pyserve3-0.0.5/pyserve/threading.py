"""
Threading Implementations of session-based servers
"""
import socket
import socketserver
from ssl import SSLContext, wrap_socket
from dataclasses import dataclass, field
from typing import Type, Optional, Dict, Any, ClassVar

from .abc import RawAddr, Address, Writer, Session, modify_socket

#** Variables **#
__all__ = ['UdpThreadServer', 'TcpThreadServer']

#** Functions **#

def new_handler(
    base:      Type['BaseRequestHandler'],
    factory:   Type[Session],
    args:      tuple           = (),
    kwargs:    Dict[str, Any]  = {},
    blocksize: int             = 8192
) -> Type['BaseRequestHandler']:
    """
    spawn new request-handler class w/ configured settings
    """
    # test factory generation
    factory(*args, **kwargs)
    # generate new request handler
    name = f'{base.__name__}Instance'
    return type(name, (base, ), dict(
        factory=factory,
        args=args,
        kwargs=kwargs,
        blocksize=blocksize,
    ))

#** Classes **#

@dataclass
class UdpWriter(Writer):
    addr: Address
    sock: socket.socket
    closing: bool = False
    
    def write(self, data: bytes, addr: Optional[Address] = None):
        self.sock.sendto(data, addr or self.addr)

    def close(self):
        self.sock.close()
        self.closing = True

    def is_closing(self) -> bool:
        return self.closing

@dataclass
class TcpWriter(Writer):
    sock: socket.socket
    closing: bool = False

    def write(self, data: bytes):
        self.sock.sendall(data)

    def close(self):
        self.closing = True
        self.sock.close()

    def is_closing(self) -> bool:
        return self.closing

class BaseRequestHandler(socketserver.BaseRequestHandler):
    factory:   Type[Session]
    args:      tuple           
    kwargs:    Dict[str, Any]
    blocksize: int

    def setup(self):
        """configure and generate session w/ information collected"""
        self.addr:   Address = Address(*self.client_address)
        self.writer: Writer
        self.error:  Optional[Exception] = None
        # spawn session object
        self.session = self.factory(*self.args, **self.kwargs)
        self.session.connection_made(self.addr, self.writer)
    
    def finish(self):
        """notify that connection disconnected"""
        self.session.connection_lost(self.error)

class UdpHandler(BaseRequestHandler):
    
    def setup(self):
        """handle connection spawn"""
        self.addr    = Address(*self.client_address) 
        self.sock    = self.request[1]
        self.writer: UdpWriter = UdpWriter(self.addr, self.sock)
        super().setup()
    
    def handle(self):
        """handle single inbound udp packet"""
        try:
            data = self.request[0]
            self.session.data_recieved(data)
        except socket.error as e:
            self.error = e
            if not self.writer.closing:
                self.writer.close()

class TcpHandler(BaseRequestHandler):
    
    def setup(self):
        """handle setup of server"""
        self.sock = self.request
        self.writer: TcpWriter = TcpWriter(self.sock)
        super().setup()

    def handle(self):
        """handle subsequent reads of inbound data"""
        while not self.writer.closing:
            try:
                data = self.sock.recv(self.blocksize)
                if not data:
                    break
                self.session.data_recieved(data)
            except socket.error as e:
                self.error = e
                if not self.writer.closing:
                    self.writer.close()
                break

@dataclass
class BaseThreadServer(socketserver.ThreadingMixIn):
    handler: ClassVar[Type[BaseRequestHandler]]

    address:    RawAddr
    factory:    Type[Session]
    args:       tuple           = field(default_factory=tuple)
    kwargs:     Dict[str, Any]  = field(default_factory=dict)
    interface:  Optional[bytes] = None
    reuse_port: bool            = False
    blocksize: int              = 8192
 
    def __post_init__(self):
        self.max_packet_size  = self.blocksize
        self.allow_reuse_port = self.reuse_port

    def new_handler(self) -> Type[BaseRequestHandler]:
        return new_handler(
            base=self.handler, 
            factory=self.factory, 
            args=self.args, 
            kwargs=self.kwargs,
            blocksize=self.blocksize,
        )

    def rebuild_socket(self, s: socketserver.BaseServer):
        """rebuild socket to recover from socket failure"""
        s.socket.close()
        s.socket = socket.socket(s.address_family, s.socket_type)
        s.server_bind()

@dataclass
class UdpThreadServer(BaseThreadServer, socketserver.UDPServer):
    handler = UdpHandler

    allow_broadcast: bool = False
 
    def __post_init__(self):
        super().__post_init__()
        socketserver.UDPServer.__init__(self, self.address, self.new_handler())

    def __exit__(self, *_):
        self.shutdown()

    def server_bind(self):
        """additional socket modification controls on server-bind"""
        super().server_bind()
        modify_socket(self.socket, None, self.interface)
        if self.allow_broadcast:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def get_request(self):
        """respawn socket after socket error to prevent infinite hanging loop"""
        try:
            return super().get_request()
        except socket.error as e:
            self.rebuild_socket(self)
            raise e

    def shutdown(self):
        """override shutdown behavior"""
        super().shutdown()
        self.socket.close()
        self.server_close()

@dataclass
class TcpThreadServer(BaseThreadServer, socketserver.TCPServer):
    handler = TcpHandler

    ssl:     Optional[SSLContext] = None
    timeout: Optional[int]        = None
 
    def __post_init__(self):
        super().__post_init__()
        socketserver.TCPServer.__init__(self, self.address, self.new_handler())

    def __exit__(self, *_):
        self.shutdown()
 
    def server_bind(self):
        """additional socket modification controls on server-bind"""
        super().server_bind()
        modify_socket(self.socket, None, self.interface)
        if self.ssl:
            self.socket = wrap_socket(self.socket, server_side=True)

    def get_request(self):
        """respawn socket after socket error to prevent infinite hanging loop"""
        try:
            sock, addr = super().get_request()
            modify_socket(sock, self.timeout, None)
            return (sock, addr)
        except socket.timeout as e:
            raise e
        except socket.error as e:
            self.rebuild_socket(self)
            raise e

    def shutdown(self):
        """override shutdown behavior"""
        super().shutdown()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.server_close()
