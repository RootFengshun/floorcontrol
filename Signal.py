'''
 * @Title: Signal
 * @Description: @TODO
 * @author fengshun
 * @date 2018/6/20
'''


class _signal:
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


signal = _signal()
signal.FLOOR_REQUEST = 'FLOOR_REQUEST'
signal.FLOOR_TAKEN = 'FLOOR_TAKEN'
signal.FLOOR_DENY = 'FLOOR_DENY'
signal.FLOOR_RELEASE = 'FLOOR_RELEASE'
