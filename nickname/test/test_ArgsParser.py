import unittest

from nn import DEFAULT_CONFIGURE_FILE, ArgsParser


class TestArgsParser(unittest.TestCase):
    def test_normal(self):
        args = ArgsParser('timeout /t 10'.split())
        self.assertEqual(args.nickname, 'timeout')
        self.assertEqual(args.args, ['/t', '10'])
        self.assertEqual(args.configFile, DEFAULT_CONFIGURE_FILE)
        self.assertFalse(args.isAdmin)

    def test_without_args(self):
        args = ArgsParser(['cmd'])
        self.assertEqual(args.nickname, 'cmd')
        self.assertEqual(args.args, [])
        self.assertEqual(args.configFile, DEFAULT_CONFIGURE_FILE)
        self.assertFalse(args.isAdmin)

    def test_configure_file(self):
        args = ArgsParser('-f nn.json cmd /c dir C:\\'.split())
        self.assertEqual(args.nickname, 'cmd')
        self.assertEqual(args.args, ['/c', 'dir', 'C:\\'])
        self.assertEqual(args.configFile, 'nn.json')
        self.assertFalse(args.isAdmin)

    def test_admin(self):
        args = ArgsParser('--admin calc'.split())
        self.assertEqual(args.nickname, 'calc')
        self.assertTrue(args.isAdmin)
        self.assertFalse(args.addConfig)

    def test_addConfig(self):
        args = ArgsParser('--add D:\\potplayer.exe "" pt'.split())
        self.assertEqual(args.nickname, 'pt')
        self.assertEqual(args.addConfig, ['D:\\potplayer.exe', '""'])


if __name__ == '__main__':
    unittest.main()
