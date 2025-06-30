#!/bin/bash
# Quick Test Runner for Enterprise Mentorship Management System

echo "🎯 ENTERPRISE MENTORSHIP SYSTEM - QUICK TEST"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📂 Current directory: $(pwd)"
echo "🕐 Test started: $(date)"
echo ""

# Run the comprehensive test
echo "🧪 Running comprehensive system test..."
python3 simple_system_test.py

# Check the exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! All tests passed!"
    echo "✅ Your roll call system is working perfectly!"
    echo "✅ System is ready for production use!"
    echo ""
    echo "📝 Next steps:"
    echo "   • Review the test report JSON file"
    echo "   • Test manually in your browser"
    echo "   • Deploy to production when ready"
else
    echo ""
    echo "❌ TESTS FAILED!"
    echo "🔧 Please fix the issues and run again"
    echo ""
    echo "📝 Troubleshooting:"
    echo "   • Check the test output above for details"
    echo "   • Review TESTING_GUIDE.md for solutions"
    echo "   • Fix any database or file issues"
fi

echo ""
echo "📚 For detailed testing procedures, see: TESTING_GUIDE.md"
echo "🔧 For fixing issues, see the troubleshooting section"
