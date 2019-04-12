
import GlobalSetting
class const(object):
    state_idle =0
    state_pending_req=0
    state_taken=0
    state_pend_req=0
    state_granted=0




class final:

    HOST = '127.0.0.1'
    SERVER_PORT = 50000
class paras:

    RETRY_OPEN = False

    SIMULATOR_TIME = 30
    NODE_NUMBER = 5

    REQ_TIME_OUT = 0.2
    REQ_EXP_VALUE = 0.01
    TANKEN_TIME = 0.333

    NETWORK_DELAY = 0.05

    BACKOFF_METHOD = 0
