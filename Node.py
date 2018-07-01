# -*- coding: UTF-8 -*-
import Queue
import random
import socket
import threading
import time

from GlobalSetting import const
from Signal import signal
from StateMachine import StateMachine


class Node(object):
    def __init__(self, name):
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((const.HOST, const.SERVER_PORT))
        self.client_socket.settimeout(10)
        self.start_time = time.time()
        self.isruning = True

        self.recv2fsm = Queue.Queue(3)
        self.state = StateMachine()

        # 启动接收线程
        node_recv_thread = threading.Thread(target=self.recv, name='node_recv')
        node_recv_thread.start()


        send_timer = threading.Timer(1, self.fun_timer)
        send_timer.start()

    def stop(self):
        self.isruning = False
        self.client_socket.close()

    def recv(self):
        while (self.isruning == True):
            try:
                data = self.client_socket.recv(1000)

                self.recv2fsm.put("sleep")
                print data

            except socket.timeout as e:
                print "socket time out"
                self.stop()
        print "recv done"

    def fsm(self):
        while (self.isruning == True):
            try:
                task = self.recv2fsm.get(block=True, timeout=20)
            except Queue.Empty:
                continue
            print 'receive task' + task

    def fun_timer(self):
        # simulator time: 100s
        if time.time() - self.start_time < 100 and self.isruning is True:
            try:
                print signal.FLOOR_REQUEST
                self.client_socket.send(signal.FLOOR_REQUEST)
                global timer
                timer = threading.Timer(self.get_exp(), self.fun_timer)
                timer.start()
            except:
                self.stop()
        else:
            self.stop()

    def get_exp(self):
        return random.expovariate(0.5)
