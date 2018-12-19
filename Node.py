# -*- coding: UTF-8 -*-

import socket
import threading
import time

from GlobalSetting import paras
from GlobalSetting import final
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
        try:
            self.client_socket.connect((final.HOST, final.SERVER_PORT))
            self.client_socket.settimeout(200)

        except:
            print 'error'

        self.start_time = time.time()
        self.isRunning = True

        # 启动接收线程
        node_recv_thread = threading.Thread(target=self.recv, name='node_recv'+str(name))
        node_recv_thread.start()

        self.states = ['state_idle', 'state_pending_req', 'state_taken', 'state_granted', 'state_pend_req']
        ## state初始化 ##
        self.transitions = [
            {'trigger': 'function_ptt_down', 'source': 'state_idle', 'dest': 'state_pending_req',
             'before': 'exit_state_idle', 'after': 'enter_state_pending_req'},  # 自己发送request
            {'trigger': 'function_request_timeout', 'source': 'state_pending_req', 'dest': 'state_taken',
             'before': 'exit_state_pending_req', 'after': 'enter_state_taken'},  # 认为自己获得了发言权
            {'trigger': 'function_ptt_up', 'source': 'state_taken', 'dest': 'state_idle', 'before': 'exit_state_taken',
             'after': 'enter_state_idle'},  # 主动释放发言权

            {'trigger': 'function_recv_req', 'source': 'state_idle', 'dest': 'state_pend_req',
             'before': 'exit_state_idle', 'after': 'enter_state_pend_req'},  # 收到其他终端的req
            {'trigger': 'function_recv_taken', 'source': 'state_pend_req', 'dest': 'state_granted',
             'before': 'exit_state_pend_req', 'after': 'enter_state_granted'},  # 收到其他终端的taken
            {'trigger': 'function_recv_release', 'source': 'state_granted', 'dest': 'state_idle',
             'before': 'exit_state_granted', 'after': 'enter_state_idle'},  # 收到其他终端的release
            {'trigger': 'function_recv_deny', 'source': 'state_pending_req', 'dest': 'state_idle',
             'before': 'exit_state_pending_req', 'after': 'enter_state_idle'},  # 收到其他终端的deny
            {'trigger': 'function_recv_release', 'source': 'state_taken', 'dest': 'state_idle',
             'before': 'exit_state_taken', 'after': 'enter_state_idle'}  # 收到其他终端的release
        ]
        self.state = 'state_idle'
        self.stateMachine = Machine(model=self, states=self.states, transitions=self.transitions, initial='state_idle')
        self.enter_state_idle()

        #### 初始化定时器####
        # 随机发起
        self.timer_req =  threading.Timer(1, self.fun_random_req_timer)
        # 发起等待
        self.timer_req_timeout = threading.Timer(paras.REQ_TIME_OUT, self.fun_pending_req_timeout)
        # 讲话时间
        self.timer_speak_timeout = threading.Timer(paras.TANKEN_TIME, self.fun_taken_time_timeout)
        self.root_timer = threading.Timer(paras.SIMULATOR_TIME, self.simulate_time_out)
        self.root_timer.start()

        self.count_req_number = 0
        self.count_taken_number = 0
        self.count_req_period_list = []
        self.count_req_time = 0

    def enter_state_idle(self):
        self.timer_req = threading.Timer(self.get_exp(paras.REQ_EXP_VALUE), self.fun_random_req_timer)
        self.timer_req.start()

    def exit_state_idle(self):
        self.timer_req.cancel()

    def enter_state_pending_req(self):
        # 重设定时器
        self.timer_req_timeout = threading.Timer(paras.REQ_TIME_OUT, self.fun_pending_req_timeout)
        self.timer_req_timeout.start()
        self.count_req_number = self.count_req_number + 1
        self.count_req_time = time.time()

    def exit_state_pending_req(self):
        # 清空pending_req计时器
        # 为什么不管用
        # 再不顶事儿砸了你

        self.timer_req_timeout.cancel()



    def enter_state_taken(self):
        # 获得发言权
        if self.client_socket is not None and self.isRunning == True:
            self.client_socket.send(str(signal.FLOOR_TAKEN))
        self.timer_speak_timeout = threading.Timer(paras.TANKEN_TIME, self.fun_taken_time_timeout)
        self.timer_speak_timeout.start()
        self.count_taken_number = self.count_taken_number+1
        self.count_req_period_list.append(time.time() - self.count_req_time)

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
        self.isRunning = False
        self.client_socket.close()

    def recv(self):
        while (self.isRunning == True):
            try:
                data = self.client_socket.recv(1000)
                self.parse_signal(data)
            except:
                self.stop()

    def fun_random_req_timer(self):
        # simulator time: 100s
        # 用于限制时间
        if self.isRunning is True:
            self.action_ptt_down()

    # 申请发言权超时，认为自己得到发言权
    def fun_pending_req_timeout(self):

        if cmp(self.state, "state_pending_req") == 0:
            self.function_request_timeout()
            Logger().do().info('send ' + str(self.name) + " " + str(signal.FLOOR_TAKEN))

    # 讲话时间到
    def fun_taken_time_timeout(self):

        if cmp(self.state, "state_taken") == 0:
            self.action_ptt_up()
            if self.client_socket is not None and self.isRunning == True:

                Logger().do().info('send ' + str(self.name) + " " + str(signal.FLOOR_RELEASE))
                self.client_socket.send(str(signal.FLOOR_RELEASE))

    def get_exp(self, v):
        return random.expovariate(v)

    def action_ptt_down(self):
        # 如果是系统是空闲状态，就进入按下ptt流程
        if cmp(self.state, "state_idle") == 0:
            Logger().do().info('send ' + str(self.name) + " " + str(signal.FLOOR_REQUEST))
            if self.client_socket is not None:
                self.client_socket.send(str(signal.FLOOR_REQUEST))
                self.function_ptt_down()
    def action_ptt_up(self):
        self.function_ptt_up()

    def parse_signal(self, data):

        if (data) == signal.FLOOR_REQUEST:
            # 收到别人的请求
            if cmp(self.state, "state_idle") == 0:

                self.function_recv_req()
            elif cmp(self.state, "state_pending_req") == 0:
                #发送deny
                if self.client_socket is not None:

                    self.client_socket.send(str(signal.FLOOR_DENY))
            elif cmp(self.state, "state_taken") == 0:
                # 发送deny
                if self.client_socket is not None:

                    self.client_socket.send(str(signal.FLOOR_DENY))
            elif cmp(self.state, "state_granted") == 0:
                if self.client_socket is not None:

                    self.client_socket.send(str(signal.FLOOR_DENY))
            elif cmp(self.state, "state_pend_req") == 0:
                pass
        if (data) == signal.FLOOR_TAKEN:

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

        if (data) == signal.FLOOR_DENY:
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
        if (data) == signal.FLOOR_RELEASE:
            if cmp(self.state, "state_idle") == 0:
                pass
            elif cmp(self.state, "state_pending_req") == 0:
                # 执行退避算法
                pass
            elif cmp(self.state, "state_taken") == 0:
                self.function_recv_release()
            elif cmp(self.state, "state_granted") == 0:
                self.function_recv_release()
            elif cmp(self.state, "state_pend_req") == 0:
                pass

    def simulate_time_out(self):
        #停止所有计时器
        self.isRunning = False
        self.timer_req.cancel()
        self.timer_req_timeout.cancel()
        self.client_socket.send('exit')
        self.client_socket.close()
        self.client_socket = None
        # 回写数据
        Logger().do().info('data')
        Logger().do().info(self.count_req_number)
        Logger().do().info(self.count_taken_number)
        Logger().do().info(self.count_req_period_list)

