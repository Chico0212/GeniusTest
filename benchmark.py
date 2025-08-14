#!/usr/bin/env python3
"""
Test Quality and Coverage Benchmark Script

This script analyzes test coverage and quality metrics for Python projects.
It uses pytest-cov for coverage analysis and custom metrics for test quality.
"""

import os
import sys
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
from datetime import datetime
import re


class BenchmarkAnalyzer:
    """Analyzes test coverage and quality metrics."""
    
    def __init__(self, project_path: str, test_path: str = "tests"):
        self.project_path = Path(project_path)
        self.test_path = Path(test_path)
        self.results = {}
        
    def run_coverage_analysis(self, source_dir: str = "src") -> Dict[str, Any]:
        """Run pytest with coverage analysis."""
        print("🔍 Running coverage analysis...")
        
        # Auto-detect source structure
        source_path = self.project_path / source_dir
        if (source_path / "calculator").exists():
            # Structure: src/calculator/
            cov_target = f"{source_dir}/calculator"
        elif source_path.exists() and any(source_path.glob("*.py")):
            # Structure: src/ with Python files
            cov_target = source_dir
        else:
            # Fallback: try to find Python package
            cov_target = "calculator"
        
        print(f"📦 Coverage target: {cov_target}")
        
        # Run pytest with coverage using uv
        cmd = [
            "uv", "run",
            "pytest", 
            f"--cov={cov_target}",
            "--cov-report=xml",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v"
        ]
        
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.project_path, 
                capture_output=True, 
                text=True,
                timeout=300
            )
            
            coverage_data = {
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
            # Parse XML coverage report if it exists
            xml_report_path = self.project_path / "coverage.xml"
            if xml_report_path.exists():
                coverage_data.update(self._parse_coverage_xml(xml_report_path))
            
            return coverage_data
            
        except subprocess.TimeoutExpired:
            return {"error": "Coverage analysis timed out", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _parse_coverage_xml(self, xml_path: Path) -> Dict[str, Any]:
        """Parse coverage XML report."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extract overall coverage
            coverage_elem = root.find('.//coverage')
            if coverage_elem is not None:
                line_rate = float(coverage_elem.get('line-rate', 0)) * 100
                branch_rate = float(coverage_elem.get('branch-rate', 0)) * 100
            else:
                line_rate = branch_rate = 0
            
            # Extract file-level coverage
            files_coverage = []
            for package in root.findall('.//package'):
                for cls in package.findall('.//class'):
                    filename = cls.get('filename', '')
                    line_rate_file = float(cls.get('line-rate', 0)) * 100
                    branch_rate_file = float(cls.get('branch-rate', 0)) * 100
                    
                    files_coverage.append({
                        'filename': filename,
                        'line_coverage': line_rate_file,
                        'branch_coverage': branch_rate_file
                    })
            
            return {
                'overall_line_coverage': line_rate,
                'overall_branch_coverage': branch_rate,
                'files_coverage': files_coverage
            }
            
        except Exception as e:
            return {'xml_parse_error': str(e)}
    
    def analyze_test_quality(self) -> Dict[str, Any]:
        """Analyze test quality metrics."""
        print("📊 Analyzing test quality...")
        
        test_files = list(self.test_path.rglob("test_*.py"))
        if not test_files:
            test_files = list(self.test_path.rglob("*_test.py"))
        
        metrics = {
            'total_test_files': len(test_files),
            'test_methods_count': 0,
            'assertion_count': 0,
            'setup_teardown_count': 0,
            'mock_usage_count': 0,
            'parameterized_tests': 0,
            'files_analysis': []
        }
        
        for test_file in test_files:
            file_analysis = self._analyze_test_file(test_file)
            metrics['files_analysis'].append(file_analysis)
            
            # Aggregate metrics
            metrics['test_methods_count'] += file_analysis['test_methods']
            metrics['assertion_count'] += file_analysis['assertions']
            metrics['setup_teardown_count'] += file_analysis['setup_teardown']
            metrics['mock_usage_count'] += file_analysis['mock_usage']
            metrics['parameterized_tests'] += file_analysis['parameterized']
        
        # Calculate quality scores
        if metrics['test_methods_count'] > 0:
            metrics['avg_assertions_per_test'] = metrics['assertion_count'] / metrics['test_methods_count']
        else:
            metrics['avg_assertions_per_test'] = 0
        
        return metrics
    
    def _analyze_test_file(self, test_file: Path) -> Dict[str, Any]:
        """Analyze individual test file."""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                'filename': str(test_file),
                'test_methods': len(re.findall(r'def test_\w+', content)),
                'assertions': len(re.findall(r'assert\w*\(', content)),
                'setup_teardown': len(re.findall(r'def (setUp|tearDown|setUpClass|tearDownClass)', content)),
                'mock_usage': len(re.findall(r'mock|Mock|patch', content)),
                'parameterized': len(re.findall(r'@pytest\.mark\.parametrize|@parameterized', content)),
                'lines_of_code': len(content.splitlines()),
                'has_docstrings': '"""' in content or "'''" in content
            }
            
            return analysis
            
        except Exception as e:
            return {
                'filename': str(test_file),
                'error': str(e),
                'test_methods': 0,
                'assertions': 0,
                'setup_teardown': 0,
                'mock_usage': 0,
                'parameterized': 0,
                'lines_of_code': 0,
                'has_docstrings': False
            }
    
    def calculate_quality_score(self, coverage_data: Dict, quality_data: Dict) -> Dict[str, Any]:
        """Calculate overall quality score."""
        print("🎯 Calculating quality scores...")
        
        # Coverage score (40% weight)
        coverage_score = coverage_data.get('overall_line_coverage', 0)
        
        # Test density score (20% weight)
        test_density = 0
        if quality_data['total_test_files'] > 0:
            test_density = min(quality_data['test_methods_count'] / max(quality_data['total_test_files'], 1) * 10, 100)
        
        # Assertion quality score (20% weight)
        assertion_quality = min(quality_data['avg_assertions_per_test'] * 20, 100)
        
        # Best practices score (20% weight)
        best_practices = 0
        if quality_data['test_methods_count'] > 0:
            mock_ratio = quality_data['mock_usage_count'] / quality_data['test_methods_count']
            setup_ratio = quality_data['setup_teardown_count'] / quality_data['total_test_files']
            best_practices = min((mock_ratio + setup_ratio) * 50, 100)
        
        # Overall score
        overall_score = (
            coverage_score * 0.4 + 
            test_density * 0.2 + 
            assertion_quality * 0.2 + 
            best_practices * 0.2
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'coverage_score': round(coverage_score, 2),
            'test_density_score': round(test_density, 2),
            'assertion_quality_score': round(assertion_quality, 2),
            'best_practices_score': round(best_practices, 2),
            'grade': self._get_grade(overall_score)
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate comprehensive report."""
        print("📋 Generating report...")
        
        coverage_data = self.run_coverage_analysis()
        quality_data = self.analyze_test_quality()
        scores = self.calculate_quality_score(coverage_data, quality_data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# Test Quality and Coverage Benchmark Report
Generated: {timestamp}
Project: {self.project_path.name}

## Overall Quality Score: {scores['overall_score']}/100 (Grade: {scores['grade']})

### Coverage Analysis
- Line Coverage: {coverage_data.get('overall_line_coverage', 0):.2f}%
- Branch Coverage: {coverage_data.get('overall_branch_coverage', 0):.2f}%
- Coverage Score: {scores['coverage_score']}/100

### Test Quality Metrics
- Total Test Files: {quality_data['total_test_files']}
- Total Test Methods: {quality_data['test_methods_count']}
- Total Assertions: {quality_data['assertion_count']}
- Avg Assertions per Test: {quality_data['avg_assertions_per_test']:.2f}
- Setup/Teardown Methods: {quality_data['setup_teardown_count']}
- Mock Usage: {quality_data['mock_usage_count']}
- Parameterized Tests: {quality_data['parameterized_tests']}

### Quality Scores Breakdown
- Test Density Score: {scores['test_density_score']}/100
- Assertion Quality Score: {scores['assertion_quality_score']}/100
- Best Practices Score: {scores['best_practices_score']}/100

### File-by-File Coverage"""

        if 'files_coverage' in coverage_data:
            for file_cov in coverage_data['files_coverage']:
                report += f"\n- {file_cov['filename']}: {file_cov['line_coverage']:.1f}% lines"

        report += "\n\n### Test Files Analysis"
        for file_analysis in quality_data['files_analysis']:
            report += f"\n- {Path(file_analysis['filename']).name}:"
            report += f" {file_analysis['test_methods']} tests, {file_analysis['assertions']} assertions"

        if coverage_data.get('success'):
            report += "\n\n✅ Coverage analysis completed successfully"
        else:
            report += f"\n\n❌ Coverage analysis failed: {coverage_data.get('error', 'Unknown error')}"

        # Save to file if requested
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {output_file}")

        return report


def main():
    """Main function with CLI interface."""
    parser = argparse.ArgumentParser(description="Test Quality and Coverage Benchmark")
    parser.add_argument("--project", "-p", default=".", help="Project directory path")
    parser.add_argument("--tests", "-t", default="tests", help="Tests directory path")
    parser.add_argument("--source", "-s", default="src", help="Source code directory")
    parser.add_argument("--output", "-o", help="Output report file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    print("🚀 Starting Test Quality and Coverage Benchmark")
    print(f"📁 Project: {args.project}")
    print(f"🧪 Tests: {args.tests}")
    print(f"💻 Source: {args.source}")
    
    analyzer = BenchmarkAnalyzer(args.project, args.tests)
    
    if args.json:
        # Generate JSON output
        coverage_data = analyzer.run_coverage_analysis(args.source)
        quality_data = analyzer.analyze_test_quality()
        scores = analyzer.calculate_quality_score(coverage_data, quality_data)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "coverage": coverage_data,
            "quality": quality_data,
            "scores": scores
        }
        
        output = json.dumps(results, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)
    else:
        # Generate text report
        report = analyzer.generate_report(args.output)
        if not args.output:
            print("\n" + "="*60)
            print(report)


if __name__ == "__main__":
    main()