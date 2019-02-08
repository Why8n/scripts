#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


def getUserDir():
    return os.path.expanduser('~')


DEFAULT_CONFIGURE_FILE = os.path.join(getUserDir(), 'nn.json')


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


class NickNameParser(object):
    '''
    configure file format:
    [{
        "program" : executable program absolute path,
        "nickname" : nickname for program,
        "args" : args for program
    },]
    '''

    def __init__(self):
        self.argsParser = ArgsParser()

    def parse(nickname):
        pass


class ArgsParser(object):
    def __init__(self, args=None):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'nickname', help='nickname for executable program')
        parser.add_argument(
            'args', nargs=argparse.REMAINDER, help='arguments pass to the executable program')
        parser.add_argument('-f', '--file', nargs='?', metavar='configure-file', dest='configFile',
                            default=DEFAULT_CONFIGURE_FILE,
                            const=DEFAULT_CONFIGURE_FILE)
        self._args = parser.parse_args(args)

    @property
    def nickname(self):
        return self._args.nickname

    @property
    def args(self):
        return self._args.args

    @property
    def configFile(self):
        return self._args.configFile


def main():
    Cmder.run('timeout', args='/t 10')


if __name__ == '__main__':
    main()
