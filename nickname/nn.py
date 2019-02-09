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


class NickNameParser(object):
    '''
    configure file format:
    [{
        "program" : executable program absolute path,
        "nickname" : nickname for program,
        "defaultArgs" : args for program
    },]
    '''

    def parse(self, argsParser):
        progInfo = self.__nickname2program(argsParser.nickname, argsParser.configFile)
        prog = progInfo.get('program', argsParser.nickname)
        print(prog)
        args = argsParser.args or progInfo.get('defaultArgs')
        run = Cmder.runAsAdmin if argsParser.isAdmin else Cmder.run
        run(prog, args=args)

    def __nickname2program(self, nickname, configFile):
        try:
            for info in self.__loadConfig(configFile):
                if info.get('nickname') == nickname:
                    return info
        except Exception as e:
            print(e)
        return {'program': nickname}

    def __loadConfig(self, configFile=DEFAULT_CONFIGURE_FILE):
        with open(configFile, 'rt', encoding='utf-8') as jsonFile:
            import json
            nicknameConfig = json.load(jsonFile)

        return nicknameConfig


class ArgsParser(object):
    def __init__(self, args=None):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'nickname', help='nickname for executable program')
        parser.add_argument('-f', '--file', nargs='?', metavar='configure-file', dest='configFile',
                            default=DEFAULT_CONFIGURE_FILE,
                            const=DEFAULT_CONFIGURE_FILE, help='set configure file (json format)')
        parser.add_argument('--admin', action='store_true', help='run as Administrator')
        parser.add_argument(
            'args', nargs='*', help='arguments pass to the executable program')
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

    @property
    def isAdmin(self):
        return self._args.admin


def main():
    NickNameParser().parse(ArgsParser())


def test():
    args = ArgsParser()
    print('admin', args.isAdmin)
    print('nickname', args.nickname)
    print('file', args.configFile)
    print('args', args.args)


if __name__ == '__main__':
    # test()
    main()
