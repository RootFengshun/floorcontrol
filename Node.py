# -*- coding: UTF-8 -*-
import Queue
import random
import socket
import threading
import time

from GlobalSetting import const


class Node(object):
    def __init__(self, name):
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((const.HOST, const.SERVER_PORT))
        self.client_socket.settimeout(10)
        self.start_time = time.time()
        self.isruning = True

        self.recv2fsm = Queue.Queue(3)

        # 启动接收线程
        node_recv_thread = threading.Thread(target=self.recv, name='node_recv')
        node_recv_thread.start()
        # # 启动发送线程
        # node_start_thread = threading.Thread(target=self.send, name='node_send')
        # node_start_thread.start()

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
            self.client_socket.send("request floor")
            global timer
            timer = threading.Timer(self.get_exp(), self.fun_timer)
            timer.start()
            pass
        else:
            self.stop()


    def get_exp(self):
        return random.expovariate(0.5)
