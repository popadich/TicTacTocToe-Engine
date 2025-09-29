#!/bin/bash
# Quick Integration Test Runner
# Runs essential integration tests for CI/CD environments

echo "🚀 Quick Integration Test Runner"
echo "================================"

# Check prerequisites 
if [ ! -f "./tttt" ]; then
    echo "❌ Engine executable missing. Run 'make' first."
    exit 1
fi

echo "⚡ Running essential integration tests..."

# Run core functionality tests only (faster for CI/CD)
python3 -c "
from integration_test_suite import IntegrationTestSuite
import sys

suite = IntegrationTestSuite()
suite.setup()

# Run critical tests only
print('Testing engine functionality...')
suite.test_engine_functionality()

print('Testing tournament system...')  
suite.test_tournament_system_basic()

print('Testing randomization...')
suite.test_randomization_functionality()

print('Testing performance...')
suite.test_performance_regression()

# Check results
total = len(suite.test_results)
passed = sum(1 for t in suite.test_results if t['success'])

print(f'\\nQuick Test Results: {passed}/{total} passed')

if passed == total:
    print('✅ All critical tests passed!')
    sys.exit(0)
else:
    print('❌ Some critical tests failed!')
    sys.exit(1)
"

echo "📋 For full integration test suite, run: python3 integration_test_suite.py"