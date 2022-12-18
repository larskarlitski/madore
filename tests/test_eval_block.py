import unittest

from madore.render import eval_block


cases = [
    ("", None),
    ("a = 7", None),
    ("a = 7\nb = 6", None),
    ("a = 7\na * 6", 42)
]


class TestEvalBlock(unittest.TestCase):
    def test_all(self):
        for block, expected in cases:
            with self.subTest():
                value = eval_block(block)
                self.assertEqual(value, expected)

    def test_exception(self):
        with self.assertRaises(NameError):
            eval_block("a")
