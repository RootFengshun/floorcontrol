# -*- coding: UTF-8 -*-

from random import seed, randint
seed(23)

import simpy

class EV:
    def __init__(self, env):
        self.env = env
        self.drive_proc = env.process(self.drive(env))
        self.bat_ctrl_proc = env.process(self.bat_ctrl(env))
        self.bat_ctrl_reactivate = env.event()
        self.bat_ctrl_sleep = env.event()



    def drive(self, env):
        """驾驶进程"""
        while True:
            # 驾驶 20-40 分钟
            print("start drive: ", env.now)
            yield env.timeout(randint(20, 40))
            print("stop drive: ", env.now)

            # 停车 1-6 小时
            print("start park: ", env.now)
            print self.bat_ctrl_reactivate.triggered, self.bat_ctrl_reactivate.processed
            self.bat_ctrl_reactivate.succeed()  # 激活充电事件
            print self.bat_ctrl_reactivate.triggered, self.bat_ctrl_reactivate.processed
            self.bat_ctrl_reactivate = env.event()
            print self.bat_ctrl_reactivate.triggered, self.bat_ctrl_reactivate.processed
            yield env.timeout(randint(60, 360)) & self.bat_ctrl_sleep # 停车时间和充电程序同时都满足
            print("stop park:", env.now)

    def bat_ctrl(self, env):
        """电池充电进程"""
        while True:
            print("charge suspend:", env.now)
            yield self.bat_ctrl_reactivate  # 休眠直到充电事件被激活
            print("charge resume:", env.now)
            yield env.timeout(randint(30, 90))
            print("charge end:", env.now)
            self.bat_ctrl_sleep.succeed()
            self.bat_ctrl_sleep = env.event()

def main():
    env = simpy.Environment()
    ev = EV(env)
    env.run(until=600)

if __name__ == '__main__':
    main()

