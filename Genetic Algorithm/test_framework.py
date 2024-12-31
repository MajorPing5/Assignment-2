# test_framework.py

class TestFramework:
    def __init__(self):
        self.tests = []

    def register(self, func):
        """Register a test case function."""
        self.tests.append(func)

    def run(self):
        """Run all registered test cases and report results."""
        results = {"passed": 0, "failed": 0}
        for test in self.tests:
            try:
                test()
                results["passed"] += 1
                print(f"PASSED: {test.__name__}")
            except AssertionError as e:
                results["failed"] += 1
                print(f"FAILED: {test.__name__} - {str(e)}")
        print("\nSummary:")
        print(f"{results['passed']} passed, {results['failed']} failed")

# Instantiate a test framework instance
test_framework = TestFramework()

# Decorator to register tests
def test_case(func):
    test_framework.register(func)
    return func
