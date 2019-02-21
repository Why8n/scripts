from .. import DEFAULT_CONFIGURE_FILE

class ArgsParser(object):
    def __init__(self, args=None):
        print(args)
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
