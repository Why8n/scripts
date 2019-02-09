#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json


def getUserDir():
    return os.path.expanduser('~')


DEFAULT_CONFIGURE_FILE = os.path.join(getUserDir(), 'nn.json')


class FileUtil(object):
    @staticmethod
    def createFileIfNotExists(fileName):
        if not os.path.exists(fileName):
            with open(fileName, 'w'):
                pass

    @staticmethod
    def readFile(fileName, ):
        with open(fileName, mode='rt', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def writeFile(fileName, content):
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(content)


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
        parser.add_argument('--add', nargs=2, dest='addConfig', metavar=('program', 'arguments'),
                            help='add nickname configure: --add-config program arguments nickname')
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

    @property
    def addConfig(self):
        return self._args.addConfig


gArgs = ArgsParser()


def addConfig(argsParser):
    def decorator(func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not argsParser.addConfig:
                return func(*args, **kwargs)
            configFile = argsParser.configFile or DEFAULT_CONFIGURE_FILE
            config = json.loads(FileUtil.readFile(configFile)) if os.path.exists(configFile) else []
            config.append({
                'nickname': argsParser.nickname,
                'program': argsParser.addConfig[0],
                'defaultArgs': argsParser.addConfig[1]
            })
            print(config)
            return FileUtil.writeFile(configFile, json.dumps(config))

        return wrapper

    return decorator


class NickNameParser(object):
    '''
    configure file format:
    [{
        "program" : executable program absolute path,
        "nickname" : nickname for program,
        "defaultArgs" : args for program
    },]
    '''

    def __init__(self, argsParser):
        self.argsParser = argsParser

    @addConfig(gArgs)
    def parse(self):
        progInfo = self.__nickname2program(self.argsParser.nickname, self.argsParser.configFile)
        prog = progInfo.get('program', self.argsParser.nickname)
        args = self.argsParser.args or progInfo.get('defaultArgs')
        print(prog, args)
        run = Cmder.runAsAdmin if self.argsParser.isAdmin else Cmder.run
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
            nicknameConfig = json.load(jsonFile)

        return nicknameConfig


gNickNameParser = NickNameParser(gArgs)


def main():
    # NickNameParser().parse(ArgsParser())
    gNickNameParser.parse()


def test():
    args = ArgsParser()
    print('admin', args.isAdmin)
    print('nickname', args.nickname)
    print('file', args.configFile)
    print('args', args.args)


if __name__ == '__main__':
    # test()
    main()
