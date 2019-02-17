import time


class StateMachine(object):
    def __init__(self):
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
    def __init__(self, name):
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
        print("Entry State %s" % (self.name))
        pass

    def leave(self):
        print("Leave State %s" % (self.name))
        pass

    def do(self, signal):
        pass


class Signal(object):
    def __init__(self, name, data=None):
        self.name = name
        self.data = data


class Auth(Signal):
    def __init__(self, data):
        Signal.__init__(self, "auth", data)


class Work(Signal):
    def __init__(self):
        Signal.__init__(self, "work")


class Sleep(Signal):
    def __init__(self):
        Signal.__init__(self, "sleep")


class Quit(Signal):
    def __init__(self):
        Signal.__init__(self, "quit")


class Idle(State):
    def __init__(self):
        State.__init__(self, "idle")
        self.register(Auth, self.authCallback)

    def authCallback(self, data):
        self.machine.transfer("grant")


class Grant(State):
    def __init__(self):
        State.__init__(self, "grant")
        self.register(Work, self.workCallback)
        self.register(Quit, self.quitCallback)
    def enter(self):
        State.enter(self)
        print('hhhh')



    def workCallback(self, data):
        self.machine.transfer("busy")

    def quitCallback(self, data):
        self.machine.transfer("idle")


class Busy(State):
    def __init__(self):
        State.__init__(self, "busy")
        self.register(Sleep, self.sleepCallback)

    def sleepCallback(self, data):
        self.machine.transfer("grant")


sm = StateMachine()
sm.addState(Idle())
sm.addState(Grant())
sm.addState(Busy())
sm.setDefault("idle")
sm.start()

signals = [Auth({}), Work(), Sleep(), Quit()]

print 'hello'
start = time.time()
for i in range(0, 1000000):
    for s in signals:
        sm.do(s)
end = time.time()
print(end - start)
