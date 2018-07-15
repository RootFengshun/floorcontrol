# -*- coding: UTF-8 -*-
import Queue
import random
import socket
import threading
import time

from GlobalSetting import const
from Signal import signal
from transitions import Machine
from LogUtils import Logger
import random


class Node(object):
    '''
    state idle : 空闲状态
    state pending req : 正在申请发言权
    state taken : 发言权授予自己
    state granted: 发言权授予其他人
    state pend req : 其他人正在申请
    '''

    def __init__(self, name):
        self.name = name
        ## socket初始化##
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.connect((const.HOST, const.SERVER_PORT))
        self.client_socket.settimeout(20)

        self.start_time = time.time()
        self.isruning = True
        # 启动接收线程
        node_recv_thread = threading.Thread(target=self.recv, name='node_recv')
        node_recv_thread.start()

        send_timer = threading.Timer(self.get_exp(), self.fun_timer)
        send_timer.start()

        self.states = ['state_idle', 'state_pending_req', 'state_taken', 'state_granted', 'state_pend_req']
        ## state初始化 ##
        self.transitions = [
            {'trigger': 'function_ptt_down', 'source': 'state_idle', 'dest': 'state_pending_req'},  # 自己发送request
            {'trigger': 'function_request_timeout', 'source': 'state_pending_req', 'dest': 'state_taken'},  # 认为自己获得了发言权
            {'trigger': 'function_ptt_up', 'source': 'state_taken', 'dest': 'state_idle'},  # 主动释放发言权
            {'trigger': 'function_recv_req', 'source': 'state_idle', 'dest': 'state_pend_req'},  # 收到其他终端的req
            {'trigger': 'function_recv_taken', 'source': 'state_pend_req', 'dest': 'state_granted'},  # 收到其他终端的taken
            {'trigger': 'function_recv_release', 'source': 'state_granted', 'dest': 'state_idle'},  # 收到其他终端的release
            {'trigger': 'function_recv_deny', 'source': 'state_pending_req', 'dest': 'state_idle'},  # 收到其他终端的release
            {'trigger': 'function_recv_release', 'source': 'state_taken', 'dest': 'state_idle'}  # 收到其他终端的release
        ]
        self.stateMachine = Machine(model=self, states=self.states, transitions=self.transitions, initial='state_idle')
        self.stateMachine.on_enter_state_pending_req('hhhhhh1')
        self.stateMachine.on_exit_state_idle('hhhhhh2')
    def enter_state_idle(self):
        pass
    def exit_state_idle(self):
        pass
    def enter_state_pending_req(self):
        time_out_timer = threading.Timer(const.REQ_TIME_OUT, self.fun_timer)
        time_out_timer.start()
        pass
    def exit_state_pending_req(self):
        pass
    def enter_state_taken(self):
        pass
    def exit_state_taken(self):
        pass
    def enter_state_granted(self):
        pass
    def exit_state_granted(self):
        pass
    def enter_state_pend_req(self):
        pass
    def exit_state_pend_req(self):
        pass

    def stop(self):
        self.isruning = False
        self.client_socket.close()

    def recv(self):
        while (self.isruning == True):
            try:
                data = self.client_socket.recv(1000)
                self.parse_signal(data)
            except socket.timeout as evb:
                print "socket time out"
                self.stop()
        print "recv done"

    def fun_timer(self):
        # simulator time: 100s
        if time.time() - self.start_time < 100 and self.isruning is True:
            try:
                Logger().do().info('send ' + str(self.name) +" "+ str(signal.FLOOR_REQUEST))
                self.client_socket.send(str(signal.FLOOR_REQUEST))
                self.function_ptt_down()

            except Exception, e:
                print str(e)
                self.stop()
        else:
            self.stop()

    # 申请发言权超时，认为自己得到发言权
    def fun_pending_req_timeout(self):
        if cmp(self.state, "state_pending_req") == 0:
            self.function_request_timeout()
    def get_exp(self):
        return random.expovariate(0.5)

    # def action_ptt_down(self):
    #     self.function_ptt_up()
    #     global timer
    #     timer = threading.Timer(self.get_exp(), self.fun_timer)
    #     timer.start()



    def parse_signal(self, data):
        if int(data) == signal.FLOOR_REQUEST:
            # 收到别人的请求
            if cmp(self.state, "state_idle") == 0:
                self.function_recv_req()
            elif cmp(self.state, "state_pending_req") == 0:
                # todo 执行退避算法
                pass
            elif cmp(self.state, "state_taken") == 0:
                #发送deny
                self.client_socket.send(str(signal.FLOOR_DENY))
            elif cmp(self.state, "state_granted") == 0:
                self.client_socket.send(str(signal.FLOOR_DENY))
            elif cmp(self.state, "state_pend_req") == 0:
                pass
        if int(data) == signal.FLOOR_TAKEN:
            # 收到taken，别人占有发言权
            if cmp(self.state, "state_idle") == 0:
                self.function_recv_taken()
            elif cmp(self.state, "state_pending_req") == 0:
                self.function_request_timeout()
            elif cmp(self.state, "state_taken") == 0:
                # todo error
                pass
            elif cmp(self.state, "state_granted") == 0:
                # todo error
                pass
            elif cmp(self.state, "state_pend_req") == 0:
                self.function_recv_taken()

        if int(data) == signal.FLOOR_DENY:
            if cmp(self.state, "state_idle") == 0:
                pass
            elif cmp(self.state, "state_pending_req") == 0:
                self.function_recv_deny()
            elif cmp(self.state, "state_taken") == 0:
                pass
            elif cmp(self.state, "state_granted") == 0:
                pass
            elif cmp(self.state, "state_pend_req") == 0:
                pass
        if int(data) == signal.FLOOR_RELEASE:
            if cmp(self.state, "state_idle") == 0:
                pass
            elif cmp(self.state, "state_pending_req") == 0:
                # 执行退避算法
                pass
            elif cmp(self.state, "state_taken") == 0:
                self.function_recv_release()
            elif cmp(self.state, "state_granted") == 0:
                pass
            elif cmp(self.state, "state_pend_req") == 0:
                pass
