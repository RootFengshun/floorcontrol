class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


const = _const()
# internal paras config start #
const.HOST = '127.0.0.1'
const.SERVER_PORT = 50000
# internal paras config end   #

# tips show config start #
const.WELCOMSTRING = 'welcome to floor control system'
# tips show config end   #

# system simulator config start #
const.REQ_TIME_OUT = 2


# system simulator config end   #
