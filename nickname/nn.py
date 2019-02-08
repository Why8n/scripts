#!/usr/bin/python
# -*- coding: utf-8 -*-


class Cmder(object):
    @staticmethod
    def __run(file, args=None, *, isAdmin=False):
        import ctypes
        return ctypes.windll.shell32.ShellExecuteW(
            None, 'runas' if isAdmin else 'open', file, args, None, 1)

    @staticmethod
    def run(file, *, args=None):
        return Cmder.__run(file, args, isAdmin=False)

    @staticmethod
    def runAsAdmin(file, *, args=None):
        return Cmder.__run(file, args, isAdmin=True)


class NickNameConfig(object):
    pass


def getUserDir():
    import os
    return os.path.expanduser('~')


def main():
    Cmder.run('timeout', args='/t 10')


if __name__ == '__main__':
    main()
