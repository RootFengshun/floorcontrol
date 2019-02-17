# -*- coding: UTF-8 -*-
'''
 * @Title: UE.py
 * @Description: @TODO
 * @author fengshun
 * @date 2019/2/10
'''
import simpy
from LogUtils import Logger
import random
from GlobalSetting import const
from Signal import signal
import time

env = simpy.Environment()
count_all_req = 0
count_all_taken=0

class StateMachine(object):
    def __init__(self, node):
        print node
        self.userData = {}
        self.stateLookup = {}
        self.currentState = None
        self.isRunning = False

    def addState(self, state):
        if isinstance(state, State):
            state.attach(self)
            self.stateLookup[state.name] = state
        else:
            raise TypeError

    def setDefault(self, stateName):
        self.currentState = self.stateLookup[stateName]

    def start(self):
        self.isRunning = True

    def do(self, signal):
        for signalType in self.currentState.signals:
            if isinstance(signal, signalType):
                self.currentState.signals[signalType](signal.data)
                return
        raise ValueError("State %s not allow signal %s!" % (self.currentState.name, signal.name))

    def getUserData(self, key):
        if key in self.userData:
            return self.userData[key]
        else:
            raise ValueError

    def setUserData(self, key, value):
        self.userData[key] = value

    def transfer(self, statusName):
        if statusName in self.stateLookup:
            self.currentState.leave()
            self.currentState = self.stateLookup[statusName]
            self.currentState.enter()

        else:
            raise ValueError("Can't find state %s!" % (statusName))



class State(object):
    def __init__(self, name, id):
        self.id=id
        self.name = name
        self.machine = None
        self.signals = {}

    def attach(self, machine):
        if isinstance(machine, StateMachine):
            self.machine = machine
        else:
            raise TypeError

    def register(self, signalType, callback):
        self.signals[signalType] = callback

    def enter(self):
        print("Enter State %s %d" % (self.name, self.id))

    def leave(self):
        # print("Leave State %s %d" % (self.name,self.id))
        pass

    def do(self, signal):
        pass
class Startup(State):
    def __init__(self,id):
        State.__init__(self, "state_startup", id)


class Idle(State):
    def __init__(self,id):
        State.__init__(self, "state_idle", id)

    def enter(self):
        State.enter(self)
        self.recv_other_req = False
        self.recv_other_req_event = env.event()
        #
        # '''there are 3 situations entering idle_state
        # 1,normal state, just finish a call process
        # 2,deny state, just got deny, maybe the first time or the 999th time
        # 3,retreat process.
        # count_retrat 代表被拒绝了几次
        # '''
        # if self.count_retreat > 0:
        #     if self.retreat_period > 0:
        #         env.process(self.req_timer(self.retreat_period))
        #     else:
        #         if env.now - self.count_req_timestamp > 20:
        #             self.count_retreat = 0
        #             self.retreat_period = 0
        #             env.process(self.req_timer(self.get_exp(paras.REQ_EXP_VALUE)))
        #             return
        #         self.retreat_period = self.get_retreat_time()
        #         self.timer_req = threading.Timer(self.retreat_period, self.fun_random_req_timer)
        #         self.retreat_start_timestamp = time.time()
        #         self.timer_req.start()
        # else:
        #     self.timer_req = threading.Timer(self.get_exp(paras.REQ_EXP_VALUE), self.fun_random_req_timer)
        #     self.timer_req.start()
        env.process(self.req_timer(2))




    def leave(self):
        self.recv_other_req = True
        self.recv_other_req_event.succeed()
        State.leave(self)
    def req_timer(self, time):
        yield env.timeout(time)|self.recv_other_req_event
        if self.recv_other_req == True:
            return
        self.machine.transfer("state_pending_req")


class PendingReq(State):
    def __init__(self, id):
        State.__init__(self, "state_pending_req",id)


    def enter(self):
        State.enter(self)
        send(signal.FLOOR_REQUEST, self.id, env)
        self.recv_other_signal = False
        self.recv_other_signal_event = env.event()
        env.process(self.taken_timer())
    def leave(self):
        self.recv_other_signal = True
        self.recv_other_signal_event.succeed()
        State.leave(self)
    def taken_timer(self):
        yield env.timeout(2)|self.recv_other_signal_event
        if self.recv_other_signal == True:
            return
        self.machine.transfer("state_taken")


class Granted(State):
    def __init__(self,id):
        State.__init__(self, "state_granted",id)

class Taken(State):
    def __init__(self,id):
        State.__init__(self, "state_taken",id)
    def enter(self):
        State.enter(self)
        send(signal.FLOOR_TAKEN, self.id, env)
        env.process(self.speak_timer())
    def speak_timer(self):
        yield env.timeout(2)
        send(signal.FLOOR_RELEASE, self.id, env)
        self.machine.transfer("state_idle")
class PendReq(State):
    def __init__(self,id):
        State.__init__(self, "state_pend_req",id)




class Node:

    recv_dict=dict()
    last_signal = None



    def __init__(self, env, name):
        self.env = env
        self.name=name
        self.recv_process_event = env.process(self.recv_process())
        env.process(self.test())
        self.recv_event =env.event()
        Node.recv_dict[name] = self.recv_event


        self.sm = StateMachine(self)
        self.sm.addState(Idle(self.name))
        self.sm.addState(PendingReq(self.name))
        self.sm.addState(PendReq(self.name))
        self.sm.addState(Granted(self.name))
        self.sm.addState(Taken(self.name))
        self.sm.addState(Startup(self.name))
        self.sm.setDefault("state_startup")
        self.sm.start()


        # 统计相关的
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
    def test(self):
        self.sm.transfer("state_idle")

        yield env.timeout(5)




    def recv_process(self):
        yield env.timeout(0.5)
        while(True):
            yield Node.recv_dict[self.name]
            cur_signal = Node.last_signal
            print 'receive ',self.name, cur_signal

            if cur_signal is None:
                return
            if cmp(cur_signal, signal.FLOOR_REQUEST) == 0:

                if cmp(self.sm.currentState.name, "state_idle") == 0:

                    self.sm.transfer("state_pend_req")
                elif cmp(self.sm.currentState.name, "state_pending_req") == 0:
                    send(signal.FLOOR_DENY,self.name, self.env)
                elif cmp(self.sm.currentState.name, "state_taken") == 0:
                    # 发送deny
                    send(signal.FLOOR_DENY,self.name, self.env)
                elif cmp(self.sm.currentState.name, "state_granted") == 0:
                    send(signal.FLOOR_DENY,self.name, self.env)

            if cmp(cur_signal, signal.FLOOR_TAKEN)==0:
                # 收到taken，别人占有发言权
                if cmp(self.sm.currentState.name, "state_idle") == 0:
                    self.sm.transfer("state_taken")
                elif cmp(self.sm.currentState.name, "state_pending_req") == 0:
                    self.sm.transfer("state_taken")
                elif cmp(self.sm.currentState.name, "state_pend_req") == 0:
                    self.sm.transfer("state_granted")
            if cmp(cur_signal, signal.FLOOR_DENY)==0:
                if cmp(self.sm.currentState.name, "state_pending_req") == 0:

                    # 发送release
                    send(signal.FLOOR_RELEASE, self.name, self.env)
                    self.sm.transfer("state_idle")

                elif cmp(self.sm.currentState.name, "state_pend_req") == 0:
                    self.sm.transfer("state_idle")
            if cmp(cur_signal, signal.FLOOR_RELEASE)==0:
                if cmp(self.sm.currentState.name, "state_granted") == 0:
                    self.sm.transfer("state_idle")
                elif cmp(self.sm.currentState.name, "state_pend_req") == 0:
                    self.sm.transfer("state_idle")


def send(sig, send_node, env):
    env.process(send_process(sig,send_node))


def send_process(sig, send_node):
    yield env.timeout(0.5)
    Node.last_signal = sig
    for i in range(len(Node.recv_dict)):
        if i == send_node:
            continue
        Node.recv_dict[i].succeed()
        Node.recv_dict[i] = env.event()


def source(env):
    for i in range(2):
        ev = Node(env,i)
    yield env.timeout(0)

env.process(source(env))
env.run(until=200)