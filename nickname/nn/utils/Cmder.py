class Cmder(object):
    @staticmethod
    def __run(file, args=None, *, isAdmin=False):
        import ctypes
        return ctypes.windll.shell32.ShellExecuteW(
            None,
            'runas' if isAdmin else 'open',
            file,
            args if not isinstance(args, (list, tuple)) else ' '.join(args),
            None, 1)

    @staticmethod
    def run(file, *, args=None):
        return Cmder.__run(file, args, isAdmin=False)

    @staticmethod
    def runAsAdmin(file, *, args=None):
        return Cmder.__run(file, args, isAdmin=True)
