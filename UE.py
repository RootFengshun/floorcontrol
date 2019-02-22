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
import math
from GlobalSetting import paras
from data import data
import threading




class StateMachine(object):
    def __init__(self, node):
        self.nodeHandler = node
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
    def __init__(self, name, id, env):
        self.id=id
        self.name = name
        self.machine = None
        self.signals = {}
        self.env = env

    def attach(self, machine):
        if isinstance(machine, StateMachine):
            self.machine = machine
        else:
            raise TypeError

    def register(self, signalType, callback):
        self.signals[signalType] = callback

    def enter(self):
        pass
        # Logger().do().info("Enter State %s %d" % (self.name, self.id))


    def leave(self):
        pass
        # Logger().do().info("Leave State %s %d" % (self.name, self.id))


    def do(self, signal):
        pass
class Startup(State):
    def __init__(self,id, env):
        State.__init__(self, "state_startup", id,env)


class Idle(State):
    def __init__(self,id,env):
        State.__init__(self, "state_idle", id,env)

    def enter(self):
        State.enter(self)

        '''there are 3 situations entering idle_state
        1,normal state, just finish a call process
        2,deny state, just got deny, maybe the first time or the 999th time
        3,retreat process.
        count_retrat 代表被拒绝了几次
        '''
        if self.machine.nodeHandler.count_retreat > 0:
            if self.machine.nodeHandler.retreat_period > 0:
                self.machine.nodeHandler.retreat_start_timestamp = self.env.now
                self.req_timer_proc = self.env.process(self.req_timer(self.machine.nodeHandler.retreat_period))
            else:
                if self.env.now - self.machine.nodeHandler.count_req_timestamp > 20:
                    self.machine.nodeHandler.count_retreat = 0
                    self.machine.nodeHandler.retreat_period = 0
                    self.req_timer_proc = self.env.process(self.req_timer(random.expovariate(paras.REQ_EXP_VALUE)))
                    return
                self.machine.nodeHandler.retreat_period = self.machine.nodeHandler.get_retreat_time()
                self.retreat_start_timestamp = self.env.now
                self.req_timer_proc = self.env.process(self.req_timer(self.machine.nodeHandler.retreat_period))
        else:
            self.req_timer_proc = self.env.process(self.req_timer(random.expovariate(paras.REQ_EXP_VALUE)))


    def leave(self):
        self.env.process(self.interrupting())
        if self.machine.nodeHandler.count_retreat == 0:
            self.machine.nodeHandler.count_req_timestamp = self.env.now
            State.leave(self)
            return
        if self.env.now - self.machine.nodeHandler.retreat_start_timestamp >= self.machine.nodeHandler.retreat_period:
            self.machine.nodeHandler.retreat_period = 0
        else:
            #记录下次退避时间
            self.machine.nodeHandler.retreat_period = self.machine.nodeHandler.retreat_period - (self.env.now - self.machine.nodeHandler.retreat_start_timestamp)

        State.leave(self)
    def interrupting(self):
        yield self.env.timeout(0)
        if not self.req_timer_proc.triggered:
            self.req_timer_proc.interrupt('hhh')
    def req_timer(self, time):

        try:
            yield self.env.timeout(time)
            self.machine.transfer("state_pending_req")
        except Exception,e:
           # print  e
            pass

class PendingReq(State):
    def __init__(self, id,env):
        State.__init__(self, "state_pending_req",id, env)


    def enter(self):
        State.enter(self)
        if self.machine.nodeHandler.count_retreat == 0:
            self.machine.nodeHandler.count_req_number += 1
        Logger().do().info('time@'+str(self.env.now)+'@ send ' + str(self.id) + " " + str(signal.FLOOR_REQUEST))
        send(signal.FLOOR_REQUEST, self.id, self.env)
        self.tanken_timer_proc = self.env.process(self.taken_timer())
    def leave(self):
        self.env.process(self.interrupting())
        State.leave(self)

    def interrupting(self):
        yield self.env.timeout(0)
        if not self.tanken_timer_proc.triggered:
            self.tanken_timer_proc.interrupt('hhh')
    def taken_timer(self):
        try:
            yield self.env.timeout(paras.REQ_TIME_OUT)
            self.machine.transfer("state_taken")
        except Exception, e:
            # print e
            pass


class Granted(State):
    def __init__(self,id,env):
        State.__init__(self, "state_granted",id,env)

class Taken(State):
    def __init__(self,id,env):
        State.__init__(self, "state_taken",id,env)
    def enter(self):
        State.enter(self)
        Logger().do().info('time@'+str(self.env.now)+'@ send ' + str(self.id) + " " + str(signal.FLOOR_TAKEN))
        self.machine.nodeHandler.count_taken_number = self.machine.nodeHandler.count_taken_number+1
        self.machine.nodeHandler.count_req_period_list.append(time.time() - self.machine.nodeHandler.count_req_timestamp)
        self.machine.nodeHandler.count_retreat = 0
        send(signal.FLOOR_TAKEN, self.id, self.env)
        self.env.process(self.speak_timer())
    def speak_timer(self):
        yield self.env.timeout(paras.TANKEN_TIME)
        Logger().do().info('time@'+str(self.env.now)+'@ send ' + str(self.id) + " " + str(signal.FLOOR_RELEASE))
        send(signal.FLOOR_RELEASE, self.id, self.env)
        self.machine.transfer("state_idle")
class PendReq(State):
    def __init__(self,id,env):
        State.__init__(self, "state_pend_req",id,env)


'''node''''''node''''''node''''''node''''''node''''''node'''
'''node''''''node''''''node''''''node''''''node''''''node'''
'''node''''''node''''''node''''''node''''''node''''''node'''
'''node''''''node''''''node''''''node''''''node''''''node'''
'''node''''''node''''''node''''''node''''''node''''''node'''




class Node:
    count_all_req = 0
    count_all_taken=0

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
        self.sm.addState(Idle(self.name,env))
        self.sm.addState(PendingReq(self.name,env))
        self.sm.addState(PendReq(self.name,env))
        self.sm.addState(Granted(self.name,env))
        self.sm.addState(Taken(self.name,env))
        self.sm.addState(Startup(self.name,env))
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

        # self.timer_speak_timeout = threading.Timer(60, self.simulate_time_out)
        # self.timer_speak_timeout.start()
    def test(self):
        self.sm.transfer("state_idle")

        yield self.env.timeout(0)

    def get_retreat_time(self):

        win = math.pow(2, self.count_retreat) > data.cw[0.02][paras.NODE_NUMBER] and math.pow(2, self.count_retreat) or data.cw[0.02][paras.NODE_NUMBER]
        if paras.BACKOFF_METHOD == 0:
            win =  math.pow(2, self.count_retreat)
        tmp =  paras.NETWORK_DELAY * random.uniform(0,win)
        Logger().do().info('retreat ' +str(self.name) + ' '+str(self.count_retreat)+ ' '+str(tmp))
        return tmp




    def recv_process(self):
        while(True):
            yield Node.recv_dict[self.name]
            cur_signal = Node.last_signal
            Logger().do().info('recv'+str(self.name) + ' ' + cur_signal)

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
                    self.sm.transfer("state_granted")
                elif cmp(self.sm.currentState.name, "state_pending_req") == 0:
                    self.sm.transfer("state_granted")
                elif cmp(self.sm.currentState.name, "state_pend_req") == 0:
                    self.sm.transfer("state_granted")
            if cmp(cur_signal, signal.FLOOR_DENY)==0:
                if cmp(self.sm.currentState.name, "state_pending_req") == 0:
                    if paras.RETRY_OPEN is True:
                        self.count_retreat += 1
                    # 发送release
                    send(signal.FLOOR_RELEASE, self.name, self.env)
                    self.sm.transfer("state_idle")
                    # print 'deny'

                elif cmp(self.sm.currentState.name, "state_pend_req") == 0:
                    self.sm.transfer("state_idle")
            if cmp(cur_signal, signal.FLOOR_RELEASE)==0:
                if cmp(self.sm.currentState.name, "state_granted") == 0:
                    self.sm.transfer("state_idle")
                elif cmp(self.sm.currentState.name, "state_pend_req") == 0:
                    self.sm.transfer("state_idle")

    def simulate_time_out(self):
        #停止所有计时器


        # 回写数据
        # Logger().do().info('data')
        Logger().do().info(str(self.name)+' '+str(self.count_req_number)+' '+str(self.count_taken_number))
        Logger().do().info(str(self.count_req_period_list)+' '+str(self.name))
        Node.count_all_req += self.count_req_number
        Node.count_all_taken +=self.count_taken_number


def send(sig, send_node, env):
    env.process(send_process(sig,send_node,env))


def send_process(sig, send_node, env):
    yield env.timeout(paras.NETWORK_DELAY)
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
def main():
    env = simpy.Environment()
    env.process(source(env))
    env.run(until=paras.SIMULATOR_TIME)
    Logger().do().info('time@' + str(env.now) + 'done')

    Logger().do().info('req :'+str(Node.count_all_req) + ' taken: '+str(Node.count_all_taken))
    Node.count_all_taken = 0
    Node.count_all_req=0
