#!/usr/bin/python
# -*- coding: utf-8 -*-


def main():
    from nn.NickNameParser import NickNameParser, gArgs
    from nn import Cmder
    program, args, isAdmin = NickNameParser(gArgs).parse()
    print('program:{program}, args:{args}, isAdmin:{isAdmin}'.format(program=program, args=args, isAdmin=isAdmin))
    program and (Cmder.runAsAdmin if isAdmin else Cmder.run)(program, args=args)


def test():
    from nn import ArgsParser
    args = ArgsParser('--admin cmd'.split())
    print('admin', args.isAdmin)
    print('nickname', args.nickname)
    print('file', args.configFile)
    print('args', args.args)


if __name__ == '__main__':
    # test()
    main()
