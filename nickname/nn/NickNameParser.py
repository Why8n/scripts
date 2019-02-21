import json
import os

from . import DEFAULT_CONFIGURE_FILE, FileUtil, ArgsParser

gArgs = ArgsParser()


def addConfig(argsParser):
    def decorator(func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not argsParser.addConfig:
                return func(*args, **kwargs)
            configFile = argsParser.configFile or DEFAULT_CONFIGURE_FILE
            config = json.loads(FileUtil.readFile(configFile)) if os.path.exists(configFile) else {}
            config[argsParser.nickname] = {
                'program': argsParser.addConfig[0],
                'defaultArgs': argsParser.addConfig[1]
            }
            print(config)
            FileUtil.writeFile(configFile, json.dumps(config))
            return None, None, None

        return wrapper

    return decorator


class NickNameParser(object):
    '''
    configure file format:
    {
        nickname : {
            "program" : executable program absolute path,
            "defaultArgs" : args for program
        },
    }
    '''

    def __init__(self, argsParser):
        self.argsParser = argsParser

    @addConfig(gArgs)
    def parse(self):
        progInfo = self.__nickname2program(self.argsParser.nickname, self.argsParser.configFile)
        program = progInfo.get('program', self.argsParser.nickname)
        args = self.argsParser.args or progInfo.get('defaultArgs')
        return program, args, self.argsParser.isAdmin

    def __nickname2program(self, nickname, configFile):
        jsonConfig = self.__loadConfig(configFile)
        default = {'program': nickname}
        if jsonConfig:
            return jsonConfig.get(nickname, default)
        return default

    def __loadConfig(self, configFile=DEFAULT_CONFIGURE_FILE):
        with open(configFile, 'rt', encoding='utf-8') as jsonFile:
            nicknameConfig = json.load(jsonFile)

        return nicknameConfig
