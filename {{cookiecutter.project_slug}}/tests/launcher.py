import os
import sys
import unittest

# Add parent dir to modules path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Discover and run tests
test_paths = ['tests']
for path in test_paths:
    loader = unittest.TestLoader()
    suite = loader.discover(path)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
