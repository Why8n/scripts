import unittest

from nn import ArgsParser
# TODO:: fix::due to gArgs creation,fail will occures
from nn.NickNameParser import NickNameParser


class TestNickNameParser(unittest.TestCase):
    def test_parse(self):
        argsParser = ArgsParser('aa -f test.json --add D:\\aa.exe ""'.split())
        nnParser = NickNameParser(argsParser)
        prog, args, isAdmin = nnParser.parse()
        self.assertEqual(prog, 'D:\\aa.exe')
        self.assertEqual(args, '""')


if __name__ == '__main__':
    unittest.main()
