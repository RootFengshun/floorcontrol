# -*- coding: UTF-8 -*-
import socket
import threading

from GlobalSetting import const
from LogUtils import Logger

socket_list = set()


def recv_signal():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = ((const.HOST, const.SERVER_PORT))
    server_socket.bind(addr)
    server_socket
    server_socket.listen(100)
    try:
        for i in range(100):
            sock, addr = server_socket.accept()
            socket_list.add(sock)
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=tcplink, args=(sock, addr), name='server_thread_' + str(i))
            t.start()
    except:
        server_socket = None


def tcplink(sock, addr):
    Logger().do().info("server thread " + threading.current_thread().getName())

    while True:
        data = sock.recv(1024)
        if not data or data.decode('utf-8') == 'exit':
            break
        relay(data, sock)
    sock.close()


def relay(data, selfSocket):
    for socket in socket_list:
        if (socket == selfSocket):
            continue
        socket.send(data)


def main():
    Logger().do().info("start server thread")
    recv_signal()


if __name__ == '__main__':
    main()
