#!/usr/bin/env python3
"""
Comprehensive test runner for MesaPass Backend
Runs all tests with coverage, security checks, and SonarQube analysis
"""
import subprocess
import sys
import os
from pathlib import Path


class TestRunner:
    """Orchestrate all testing tasks"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.failed_commands = []
        self.passed_commands = []
    
    def run_command(self, cmd, description):
        """Run a command and track success/failure"""
        print(f"\n{'='*60}")
        print(f"▶ {description}")
        print(f"{'='*60}")
        print(f"Command: {' '.join(cmd)}\n")
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=False)
            if result.returncode == 0:
                print(f"\n✓ {description} - PASSED")
                self.passed_commands.append(description)
            else:
                print(f"\n✗ {description} - FAILED")
                self.failed_commands.append(description)
            return result.returncode
        except Exception as e:
            print(f"\n✗ ERROR running {description}: {e}")
            self.failed_commands.append(description)
            return 1
    
    def run_all_tests(self):
        """Run all tests"""
        return self.run_command(
            ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
            "All Tests (Unit + Integration + Security)"
        )
    
    def run_unit_tests(self):
        """Run only unit tests"""
        return self.run_command(
            ["python", "-m", "pytest", "tests/unit/", "-v", "-m", "unit"],
            "Unit Tests Only"
        )
    
    def run_integration_tests(self):
        """Run only integration tests"""
        return self.run_command(
            ["python", "-m", "pytest", "tests/integration/", "-v", "-m", "integration"],
            "Integration Tests Only"
        )
    
    def run_security_tests(self):
        """Run only security tests"""
        return self.run_command(
            ["python", "-m", "pytest", "tests/security/", "-v", "-m", "security"],
            "Security Tests Only"
        )
    
    def run_coverage(self):
        """Run tests with coverage report"""
        return self.run_command(
            ["python", "-m", "pytest", "tests/", "--cov=app", "--cov-report=html", "--cov-report=term-missing"],
            "Tests with Coverage Report"
        )
    
    def run_bandit_security(self):
        """Run Bandit for security scanning"""
        return self.run_command(
            ["python", "-m", "bandit", "-r", "app/", "-f", "json", "-o", "bandit-report.json"],
            "Bandit Security Scan"
        )
    
    def run_safety_check(self):
        """Check for known vulnerabilities in dependencies"""
        return self.run_command(
            ["python", "-m", "safety", "check", "--json", "-o", "safety-report.json"],
            "Safety Dependency Check"
        )
    
    def run_pylint(self):
        """Run Pylint for code quality"""
        return self.run_command(
            ["python", "-m", "pylint", "app/", "--output-format=json", "--exit-zero", ">", "pylint-report.json"],
            "Pylint Code Quality Analysis"
        )
    
    def run_sonarqube_analysis(self):
        """Run SonarQube analysis"""
        return self.run_command(
            ["sonar-scanner", "-Dsonar.projectBaseDir=.", "-Dsonar.python.coverage.reportPaths=coverage.xml"],
            "SonarQube Analysis"
        )
    
    def print_summary(self):
        """Print test execution summary"""
        print(f"\n\n{'='*60}")
        print("TEST EXECUTION SUMMARY")
        print(f"{'='*60}\n")
        
        if self.passed_commands:
            print(f"✓ PASSED ({len(self.passed_commands)}):")
            for cmd in self.passed_commands:
                print(f"  • {cmd}")
        
        if self.failed_commands:
            print(f"\n✗ FAILED ({len(self.failed_commands)}):")
            for cmd in self.failed_commands:
                print(f"  • {cmd}")
        
        print(f"\n{'='*60}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MesaPass Backend Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --all          # Run all tests
  python run_tests.py --coverage     # Run tests with coverage
  python run_tests.py --security     # Run security tests
  python run_tests.py --full         # Run everything including SonarQube
        """
    )
    
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--security", action="store_true", help="Run security tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--bandit", action="store_true", help="Run Bandit security scan")
    parser.add_argument("--safety", action="store_true", help="Check for vulnerable dependencies")
    parser.add_argument("--pylint", action="store_true", help="Run Pylint code quality check")
    parser.add_argument("--sonar", action="store_true", help="Run SonarQube analysis")
    parser.add_argument("--full", action="store_true", help="Run complete test suite")
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if not any(vars(args).values()):
        parser.print_help()
        return 1
    
    runner = TestRunner()
    
    if args.all or args.full:
        runner.run_all_tests()
    else:
        if args.unit:
            runner.run_unit_tests()
        if args.integration:
            runner.run_integration_tests()
        if args.security:
            runner.run_security_tests()
    
    if args.coverage or args.full:
        runner.run_coverage()
    
    if args.bandit or args.full:
        runner.run_bandit_security()
    
    if args.safety or args.full:
        runner.run_safety_check()
    
    if args.pylint or args.full:
        runner.run_pylint()
    
    if args.sonar or args.full:
        runner.run_sonarqube_analysis()
    
    runner.print_summary()
    
    # Exit with error code if any tests failed
    return 1 if runner.failed_commands else 0


if __name__ == "__main__":
    sys.exit(main())
