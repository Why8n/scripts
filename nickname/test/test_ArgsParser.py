import unittest

from nickname.nn import ArgsParser, DEFAULT_CONFIGURE_FILE


class TestArgsParser(unittest.TestCase):
    def test_normal(self):
        args = ArgsParser('timeout /t 10'.split())
        self.assertEqual(args.nickname, 'timeout')
        self.assertEqual(args.args, ['/t', '10'])
        self.assertEqual(args.configFile, DEFAULT_CONFIGURE_FILE)

    def test_without_args(self):
        args = ArgsParser(['cmd'])
        self.assertEqual(args.nickname, 'cmd')
        self.assertEqual(args.args, [])
        self.assertEqual(args.configFile, DEFAULT_CONFIGURE_FILE)

    def test_configure_file(self):
        args = ArgsParser('-f nn.json cmd /c dir C:\\'.split())
        self.assertEqual(args.nickname, 'cmd')
        self.assertEqual(args.args, ['/c', 'dir', 'C:\\'])
        self.assertEqual(args.configFile, 'nn.json')


if __name__ == '__main__':
    unittest.main()
