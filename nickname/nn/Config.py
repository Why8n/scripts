import os


def getUserDir():
    return os.path.expanduser('~')


DEFAULT_CONFIGURE_FILE = os.path.join(getUserDir(), 'nn.json')
