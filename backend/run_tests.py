# run_tests.py
import unittest

loader = unittest.TestLoader()
tests = loader.discover('product/tests')
testRunner = unittest.TextTestRunner()
testRunner.run(tests)
