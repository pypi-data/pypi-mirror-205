import unittest
from ztestupload.ztestupload import add


class TestAdd(unittest.TestCase):
    def test_add(self):
        i = add.add(1, 2)
        iv = 1 + 2
        self.assertEquals(i, iv)


if __name__ == "__main__":
    unittest.main()
