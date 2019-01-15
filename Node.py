# -*- coding: UTF-8 -*-

import socket
import threading
import time

from GlobalSetting import paras
from GlobalSetting import final
from Signal import signal
from transitions import Machine
from LogUtils import Logger
from data import data
import random
import math


class Node(object):
    '''
    state idle : 空闲状态
    state pending req : 正在申请发言权
    state taken : 发言权授予自己
    state granted: 发言权授予其他人
    state pend req : 其他人正在申请
    '''
    count_all_req=0
    count_all_taken = 0



    def __init__(self, name):

        self.name = name
        ## socket初始化##
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.settimeout(2)
        try:
            self.client_socket.connect((final.HOST, final.SERVER_PORT))
            # self.client_socket.settimeout(200)

        except:
            print 'error'

        self.start_time = time.time()
        self.isRunning = True

        #### 初始化定时器####
        # 随机发起
        self.timer_req =  threading.Timer(1, self.fun_random_req_timer)
        # 发起等待
        self.timer_req_timeout = threading.Timer(paras.REQ_TIME_OUT, self.fun_pending_req_timeout)
        # 讲话时间
        self.timer_speak_timeout = threading.Timer(paras.TANKEN_TIME, self.fun_taken_time_timeout)
        self.root_timer = threading.Timer(paras.SIMULATOR_TIME, self.simulate_time_out)
        self.root_timer.start()
        # 用于统计
        self.count_req_number = 0
        self.count_taken_number = 0
        self.count_req_period_list = []
        self.count_req_timestamp = 0
        # 退避标志
        #　当前退避次数
        self.count_retreat = 0
        # 退避时间
        self.retreat_period = 0
        # 退避开始时间
        self.retreat_start_timestamp = 0

        # 启动接收线程
        self.node_recv_thread = threading.Thread(target=self.recv, name='node_recv' + str(name))
        self.node_recv_thread.start()

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
            {'trigger': 'function_recv_deny', 'source': 'state_pend_req', 'dest': 'state_idle',
             'before': 'exit_state_pend_req', 'after': 'enter_state_idle'},  # 其他终端req失败
            {'trigger': 'function_recv_release', 'source': 'state_taken', 'dest': 'state_idle',
             'before': 'exit_state_taken', 'after': 'enter_state_idle'}  # 收到其他终端的release
        ]
        self.state = 'state_idle'
        self.stateMachine = Machine(model=self, states=self.states, transitions=self.transitions, initial='state_idle')
        self.enter_state_idle()

    def enter_state_idle(self):
        '''there are 3 situations entering idle_state
        1,normal state, just finish a call process
        2,deny state, just got deny, maybe the first time or the 999th time
        3,retreat process.
        count_retrat 代表被拒绝了几次
        '''
        if self.count_retreat > 0:
            if self.retreat_period > 0:
                self.timer_req = threading.Timer(self.retreat_period, self.fun_random_req_timer)
                self.retreat_start_timestamp = time.time()
                self.timer_req.start()
            else:
                self.retreat_period = self.get_retreat_time()
                self.timer_req = threading.Timer(self.retreat_period, self.fun_random_req_timer)
                self.retreat_start_timestamp = time.time()
                self.timer_req.start()
        else:
            self.timer_req = threading.Timer(self.get_exp(paras.REQ_EXP_VALUE), self.fun_random_req_timer)
            self.timer_req.start()


    def exit_state_idle(self):
        self.timer_req.cancel()
        if self.count_retreat == 0:
            self.count_req_timestamp = time.time()
            return
        if time.time() - self.retreat_start_timestamp >= self.retreat_period:
            self.retreat_period = 0
        else:
            #记录下次退避时间
            self.retreat_period = self.retreat_period - (time.time() - self.retreat_start_timestamp)

    def enter_state_pending_req(self):
        if self.count_retreat == 0:
            self.count_req_number += 1
        # 重设定时器
        self.timer_req_timeout = threading.Timer(paras.REQ_TIME_OUT, self.fun_pending_req_timeout)
        self.timer_req_timeout.start()



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
        self.count_req_period_list.append(time.time() - self.count_req_timestamp)
        self.count_retreat = 0

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
                pass


    def fun_random_req_timer(self):
        # simulator time: 100s
        # 用于限制时间
        if self.isRunning is True and  cmp(self.state, "state_idle") == 0:
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
        tmp = random.expovariate(v)
        return tmp

    def action_ptt_down(self):
        # 如果是系统是空闲状态，就进入按下ptt流程
        if self.isRunning is False:
            return
        if cmp(self.state, "state_idle") == 0:
            Logger().do().info('send ' + str(self.name) + " " + str(signal.FLOOR_REQUEST))
            if self.client_socket is not None:
                self.client_socket.send(str(signal.FLOOR_REQUEST))
                self.function_ptt_down()
    def action_ptt_up(self):
        self.function_ptt_up()

    def parse_signal(self, data):
        # Logger().do().info('RECV '+str(self.name) +' '+data)
        if (data) == signal.FLOOR_REQUEST:
            # 收到别人的请求
            if cmp(self.state, "state_idle") == 0:

                self.function_recv_req()
            elif cmp(self.state, "state_pending_req") == 0:
                #发送deny
                if self.client_socket is not None:
                    self.client_socket.send(str(signal.FLOOR_DENY))
                else:
                    pass

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
                if paras.RETRY_OPEN is True:
                    self.count_retreat += 1
                self.function_recv_deny()

            elif cmp(self.state, "state_taken") == 0:
                pass
            elif cmp(self.state, "state_granted") == 0:
                pass
            elif cmp(self.state, "state_pend_req") == 0:
                self.function_recv_deny()
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
        if self.client_socket is not None:
            self.client_socket.send('exit')
            self.client_socket.close()
            self.client_socket = None
        # 回写数据
        # Logger().do().info('data')
        Logger().do().info(str(self.name)+' '+str(self.count_req_number)+' '+str(self.count_taken_number))
        Logger().do().info(str(self.count_req_period_list)+' '+str(self.name))
        Node.count_all_req += self.count_req_number
        Node.count_all_taken +=self.count_taken_number
    def get_retreat_time(self):
        #  merger
        tmp =  paras.NETWORK_DELAY * random.uniform(0, data.cw[0.02][paras.NODE_NUMBER])
        Logger().do().info('retreat ' +str(self.name) + ' '+str(self.count_retreat)+ ' '+str(tmp))
        return tmp



