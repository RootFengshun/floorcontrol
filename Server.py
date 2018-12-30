# -*- coding: UTF-8 -*-
import socket
import threading
import time
from GlobalSetting import final
from GlobalSetting import paras
from LogUtils import Logger


socket_list = set()
start_time = time.time()

def recv_signal():
    start_time = time.time()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = (final.HOST, final.SERVER_PORT)
    server_socket.bind(addr)
    server_socket.listen(100)
    # 仅在仿真的前半程允许连接
    Logger().do().info('start server thread')

    try:
        for i in range(paras.NODE_NUMBER):

            sock, addr = server_socket.accept()
            socket_list.add(sock)
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=tcplink, args=(sock, ), name='server_thread_' + str(i))
            t.start()
    except:
        server_socket = None


def relay(data, selfSocket):
    for socket in socket_list:

        if (socket == selfSocket or  socket is None):
            continue
        socket.send(data)


def tcplink(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data or data.decode('utf-8') == 'exit':
                break
            relay_delay = threading.Timer(paras.NETWORK_DELAY, relay, [data, sock])
            relay_delay.start()
    except:
        pass
    sock.close()
    socket_list.remove(sock)




def main():
    recv_signal()

if __name__ == '__main__':
    main()
