import unittest

from mymodule import add

class TestAdd(unittest.TestCase): 
    def test1(self): 
        self.assertEqual(add(2, 4), 6) # test when 2 and 4 are given as input the output must be 6.
        self.assertEqual(add(0 ,0), 0)  # test when 0 and 0 are given as input the output must be 0.
        self.assertEqual(add(2.3, 3.6), 5.9)  # test when 2.3 and 3.6 are given as input the output must be 5.9.
        self.assertEqual(add('hello', 'world'), 'helloworld')  # test when 2.3 and 3.6 are given as input the output must be 5.9.
        self.assertEqual(add(2.3000, 4.300), 6.6)  # test when 2.3 and 3.6 are given as input the output must be 5.9.
        self.assertNotEqual(add(-2, -2), 0)  # test when 2.3 and 3.6 are given as input the output must be 5.9.
        
unittest.main()