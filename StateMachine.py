# -*- coding: UTF-8 -*-
'''
 * @Title: StateMachine
 * @Description: @TODO
 * @author fengshun
 * @date 2018/7/1
'''
from transitions import Machine


class StateMachine(object):
    def __init__(self):
        # 状态定义
        self.states = ['idle', 'pending_req', 'taken', 'granted']

        # 定义状态转移
        # The trigger argument defines the name of the new triggering method
        self.transitions = [
            {'trigger': 'ptt_down', 'source': 'idle', 'dest': 'pending_req'},  # 自己发送request
            {'trigger': 'recv_taken', 'source': 'idle', 'dest': 'granted'},  # 收到其他终端的taken
            {'trigger': 'request_timeout', 'source': 'pending_req', 'dest': 'taken'},  # 认为自己获得了发言权
            {'trigger': 'ptt_up', 'source': 'taken', 'dest': 'idle'}]  # 主动释放发言权

        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial='idle')
