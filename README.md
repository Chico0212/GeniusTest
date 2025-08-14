# Multi-Agent Calculator Project

A comprehensive Python project featuring a calculator with CLI interface, automated test generation using AI agents, and quality benchmarking tools.

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Setup & Installation](#setup--installation)
- [Calculator Usage](#calculator-usage)
- [GeniusTest - AI Test Generator](#geniustest---ai-test-generator)
- [Benchmark - Quality Analysis](#benchmark---quality-analysis)
- [Development Workflow](#development-workflow)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🏗️ Project Structure

```
multi_agents/
├── calculator/                 # Main calculator project
│   ├── src/calculator/        # Source code
│   │   ├── calculator.py      # Core calculator logic
│   │   ├── cli.py            # Command-line interface
│   │   └── main.py           # Application entry point
│   ├── tests/                # Test files
│   │   ├── test_calculator.py
│   │   ├── test_cli.py
│   │   └── test_main.py
│   └── pyproject.toml        # Project dependencies
├── geniustest.py             # AI-powered test generator
├── benchmark.py              # Quality & coverage analyzer
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🚀 Quick Start

1. **Clone and setup:**
```bash
git clone <your-repo>
cd multi_agents
```

2. **Setup environment:**
```bash
uv sync
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

3. **Run calculator:**
```bash
cd calculator
uv run calc add 5 3
```

4. **Generate tests:**
```bash
uv run python ../geniustest.py --directory ./calculator/src --write-files
```

5. **Run benchmark:**
```bash
cd calculator
uv run python ../benchmark.py
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Google Gemini API key

### Installation Steps

1. **Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Initialize the project:**
```bash
cd multi_agents
uv sync
```

3. **Configure environment variables:**
```bash
# Create .env file with your Google API key
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

4. **Install calculator as package:**
```bash
cd calculator
uv pip install -e .
```

5. **Verify installation:**
```bash
uv run calc --help
```

## 🧮 Calculator Usage

The calculator provides a CLI interface for mathematical operations with history tracking.

### Basic Operations

```bash
cd calculator

# Addition
uv run calc add 5 3
# Result: 8.0

# Subtraction  
uv run calc subtract 10 4
# Result: 6.0

# Multiplication
uv run calc multiply 6 7
# Result: 42.0

# Division
uv run calc divide 15 3
# Result: 5.0

# Power
uv run calc power 2 8
# Result: 256.0
```

### Advanced Features

**Working with negative numbers:**
```bash
# Use -- to separate negative numbers from options
uv run calc add -- -5 -3
# Result: -8.0

uv run calc subtract -- 5 -3
# Result: 8.0
```

**History management:**
```bash
# View calculation history
uv run calc history

# Clear history
uv run calc clear
```

### Python API Usage

```python
from calculator.calculator import Calculator

calc = Calculator()
result = calc.add(5, 3)
print(f"Result: {result}")
print(f"History: {calc.get_history()}")
```

## 🤖 GeniusTest - AI Test Generator

GeniusTest is a multi-agent system that automatically generates comprehensive unit tests for Python code using AI.

### Features

- **Multi-agent analysis**: Code analyzer, test generator, pattern specialist, quality evaluator
- **Real functional tests**: Generates executable tests, not just examples
- **Comprehensive coverage**: Tests success cases, errors, and edge cases
- **Multiple output formats**: Console display or file generation

### Usage Examples

**Analyze and display tests for a single file:**
```bash
uv run python geniustest.py --file ./calculator/src/calculator/calculator.py
```

**Generate test files for entire directory:**
```bash
uv run python geniustest.py --directory ./calculator/src --write-files --output ./calculator/tests_generated
```

**Process with custom output directory:**
```bash
uv run python geniustest.py --directory ./my_project --write-files --output ./my_tests
```

**Run with example code:**
```bash
uv run python geniustest.py
```

### Command Line Options

```bash
uv run python geniustest.py --help

Options:
  -d, --directory TEXT    Directory path to scan for Python files
  -f, --file TEXT        Single Python file to process  
  -o, --output TEXT      Output directory for generated test files (default: tests)
  -w, --write-files      Write generated tests to files
  --example              Run with example code
```

### Generated Test Structure

GeniusTest generates tests following this structure:

```python
import unittest
import sys
import os

# Path setup for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator.calculator import Calculator

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = Calculator()
    
    def test_add_positive_numbers(self):
        result = self.calculator.add(5, 3)
        self.assertEqual(result, 8)
    
    def test_add_negative_numbers(self):
        result = self.calculator.add(-5, -3)
        self.assertEqual(result, -8)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.divide(5, 0)

if __name__ == '__main__':
    unittest.main()
```

## 📊 Benchmark - Quality Analysis

The benchmark script provides comprehensive analysis of test coverage and quality metrics.

### Features

- **Coverage Analysis**: Line and branch coverage using pytest-cov
- **Test Quality Metrics**: Test density, assertion quality, best practices
- **Quality Scoring**: Overall score (0-100) with letter grades
- **Multiple Output Formats**: Text reports and JSON data

### Usage Examples

**Basic benchmark analysis:**
```bash
cd calculator
uv run python ../benchmark.py
```

**Generate report file:**
```bash
cd calculator
uv run python ../benchmark.py --output benchmark_report.txt
```

**JSON output for CI/CD:**
```bash
cd calculator
uv run python ../benchmark.py --json --output results.json
```

**Custom project paths:**
```bash
uv run python benchmark.py --project ./my_project --tests my_tests --source my_src
```

### Command Line Options

```bash
uv run python benchmark.py --help

Options:
  -p, --project TEXT     Project directory path (default: .)
  -t, --tests TEXT       Tests directory path (default: tests)  
  -s, --source TEXT      Source code directory (default: src)
  -o, --output TEXT      Output report file
  --json                 Output results as JSON
```

### Sample Benchmark Report

```
# Test Quality and Coverage Benchmark Report
Generated: 2025-08-13 22:15:23
Project: calculator

## Overall Quality Score: 85.42/100 (Grade: B)

### Coverage Analysis
- Line Coverage: 94.94%
- Branch Coverage: 87.50%
- Coverage Score: 94.94/100

### Test Quality Metrics
- Total Test Files: 3
- Total Test Methods: 44
- Total Assertions: 92
- Avg Assertions per Test: 2.09
- Setup/Teardown Methods: 3
- Mock Usage: 8
- Parameterized Tests: 0

### Quality Scores Breakdown
- Test Density Score: 100/100
- Assertion Quality Score: 41.82/100
- Best Practices Score: 59.09/100

### File-by-File Coverage
- calculator.py: 100.0% lines
- cli.py: 97.7% lines
- main.py: 0.0% lines

✅ Coverage analysis completed successfully
```

## 🔧 Development Workflow

### Running Tests

```bash
cd calculator

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/calculator --cov-report=html

# Run specific test file
uv run pytest tests/test_calculator.py

# Run with verbose output
uv run pytest -v
```

### Code Quality Checks

```bash
cd calculator

# Run benchmark analysis
uv run python ../benchmark.py

# Generate coverage report
uv run pytest --cov=src/calculator --cov-report=html
open htmlcov/index.html  # View in browser
```

### Continuous Integration

Example GitHub Actions workflow:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v1
    
    - name: Install dependencies
      run: uv sync
      
    - name: Run tests
      run: |
        cd calculator
        uv run pytest --cov=src/calculator --cov-report=xml
        
    - name: Run benchmark
      run: |
        cd calculator  
        uv run python ../benchmark.py --json --output benchmark.json
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required for GeniusTest AI features
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Custom model settings
GEMINI_MODEL=gemini-2.0-flash
TEMPERATURE=0.7
```

### Project Configuration

**pyproject.toml** for calculator:

```toml
[project]
name = "calculator"
version = "0.1.0"
dependencies = [
    "typer>=0.9.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/calculator --cov-report=term-missing"
```

### IDE Setup

**VS Code settings.json:**

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": true
}
```

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" errors:**
```bash
# Ensure you're using uv run
uv run pytest

# Or activate the virtual environment
source .venv/bin/activate
pytest
```

**2. Negative numbers treated as options:**
```bash
# Use -- separator
uv run calc add -- -5 -3

# Or quote the numbers
uv run calc add "-5" "-3"
```

**3. Coverage not collecting data:**
```bash
# Make sure to use uv run
cd calculator
uv run pytest --cov=src/calculator

# Check if tests are actually importing the code
uv run pytest -v
```

**4. GeniusTest API errors:**
```bash
# Check if API key is set
echo $GOOGLE_API_KEY

# Verify .env file exists
cat .env
```

**5. Import errors in generated tests:**
- Generated tests include proper path setup
- Ensure source code structure matches imports
- Run tests with `uv run pytest`

### Getting Help

1. **Check logs**: Most commands provide verbose output with `-v` flag
2. **Validate environment**: Run `uv run python -c "import calculator; print('OK')"`
3. **Test connectivity**: Run GeniusTest with example code first
4. **Check dependencies**: Run `uv sync` to ensure all packages are installed

### Performance Tips

- **Use `--write-files`** with GeniusTest for large projects to avoid console spam
- **Run benchmark periodically** to track quality improvements
- **Use JSON output** for automated processing in CI/CD
- **Cache virtual environment** in CI systems for faster builds

## 📚 Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/docs)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run quality checks: `uv run python benchmark.py`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.