import simpy
class SimTimer(object):

    def __init__(self, env, delay, callback):
        self.env      = env
        self.delay    = delay
        self.action   = None
        self.callback = callback
        self.running  = False
        self.canceled = False

    def wait(self):
        """
        Calls a callback after time has elapsed.
        """
        try:
            yield self.env.timeout(self.delay)
            self.callback()
            self.running  = False
        except simpy.Interrupt as i:
            print "Interrupted!"
            self.canceled = True
            self.running  = False

    def start(self):
        """
        Starts the timer
        """
        if not self.running:
            self.running = True
            self.action  = self.env.process(self.wait())

    def stop(self):
        """
        Stops the timer
        """
        if self.running:
            self.action.interrupt()
            self.action = None

    def reset(self):
        """
        Interrupts the current timer and restarts.
        """
        self.stop()
        self.start()