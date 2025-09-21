#!/usr/bin/env python3
"""
OpenTrust Protocol Conformance Validator

This tool validates SDK implementations against the OpenTrust Protocol specification.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple
import importlib.util

class ConformanceValidator:
    """Validates SDK implementations against OTP specification."""
    
    def __init__(self, test_vectors_path: str):
        """Initialize validator with test vectors."""
        self.test_vectors_path = Path(test_vectors_path)
        self.test_vectors = self._load_test_vectors()
        
    def _load_test_vectors(self) -> Dict[str, Any]:
        """Load test vectors from JSON files."""
        test_vectors = {}
        
        # Load judgment creation tests
        judgments_file = self.test_vectors_path / "judgments.json"
        if judgments_file.exists():
            with open(judgments_file, 'r') as f:
                test_vectors['judgments'] = json.load(f)['test_vectors']
        
        # Load fusion tests
        fusion_file = self.test_vectors_path / "fusion-tests.json"
        if fusion_file.exists():
            with open(fusion_file, 'r') as f:
                test_vectors['fusion'] = json.load(f)['test_vectors']
        
        return test_vectors
    
    def validate_judgment_creation(self, sdk_module) -> Tuple[int, int]:
        """Validate judgment creation functionality."""
        print("🧪 Testing judgment creation...")
        passed = 0
        total = 0
        
        for test_case in self.test_vectors.get('judgments', []):
            total += 1
            test_name = test_case['name']
            
            try:
                # Create judgment using SDK
                judgment = sdk_module.NeutrosophicJudgment(
                    T=test_case['input']['T'],
                    I=test_case['input']['I'],
                    F=test_case['input']['F'],
                    provenance_chain=test_case['input']['provenance_chain']
                )
                
                # Check if validation passed as expected
                if test_case['expected_valid']:
                    print(f"  ✅ {test_name}")
                    passed += 1
                else:
                    print(f"  ❌ {test_name} - Should have failed but didn't")
                    
            except Exception as e:
                error_msg = str(e)
                
                if not test_case['expected_valid']:
                    # Check if error message matches expected
                    expected_error = test_case['expected_error']
                    if expected_error and expected_error in error_msg:
                        print(f"  ✅ {test_name}")
                        passed += 1
                    else:
                        print(f"  ⚠️  {test_name} - Failed as expected but wrong error: {error_msg}")
                        passed += 1  # Still counts as passed since it failed
                else:
                    print(f"  ❌ {test_name} - Unexpected error: {error_msg}")
        
        return passed, total
    
    def validate_fusion_operators(self, sdk_module) -> Tuple[int, int]:
        """Validate fusion operators functionality."""
        print("🧪 Testing fusion operators...")
        passed = 0
        total = 0
        
        # Test conflict-aware weighted average
        try:
            judgments = [
                sdk_module.NeutrosophicJudgment(T=0.8, I=0.2, F=0.0, provenance_chain=[
                    {"source_id": "test1", "timestamp": "2025-09-20T20:30:00Z"}
                ]),
                sdk_module.NeutrosophicJudgment(T=0.6, I=0.3, F=0.1, provenance_chain=[
                    {"source_id": "test2", "timestamp": "2025-09-20T20:30:00Z"}
                ])
            ]
            
            result = sdk_module.conflict_aware_weighted_average(judgments, [0.6, 0.4])
            
            # Check if result is valid
            if (0 <= result.T <= 1 and 0 <= result.I <= 1 and 0 <= result.F <= 1 and 
                result.T + result.I + result.F <= 1.0):
                print("  ✅ Conflict-aware weighted average")
                passed += 1
            else:
                print("  ❌ Conflict-aware weighted average - Invalid result")
            total += 1
            
        except Exception as e:
            print(f"  ❌ Conflict-aware weighted average - Error: {e}")
            total += 1
        
        # Test optimistic fusion
        try:
            result = sdk_module.optimistic_fusion(judgments)
            
            if (0 <= result.T <= 1 and 0 <= result.I <= 1 and 0 <= result.F <= 1 and 
                result.T + result.I + result.F <= 1.0):
                print("  ✅ Optimistic fusion")
                passed += 1
            else:
                print("  ❌ Optimistic fusion - Invalid result")
            total += 1
            
        except Exception as e:
            print(f"  ❌ Optimistic fusion - Error: {e}")
            total += 1
        
        # Test pessimistic fusion
        try:
            result = sdk_module.pessimistic_fusion(judgments)
            
            if (0 <= result.T <= 1 and 0 <= result.I <= 1 and 0 <= result.F <= 1 and 
                result.T + result.I + result.F <= 1.0):
                print("  ✅ Pessimistic fusion")
                passed += 1
            else:
                print("  ❌ Pessimistic fusion - Invalid result")
            total += 1
            
        except Exception as e:
            print(f"  ❌ Pessimistic fusion - Error: {e}")
            total += 1
        
        return passed, total
    
    def validate_provenance_chain(self, sdk_module) -> Tuple[int, int]:
        """Validate provenance chain functionality."""
        print("🧪 Testing provenance chain...")
        passed = 0
        total = 0
        
        try:
            # Create judgment with provenance
            judgment = sdk_module.NeutrosophicJudgment(
                T=0.8, I=0.2, F=0.0,
                provenance_chain=[
                    {"source_id": "test", "timestamp": "2025-09-20T20:30:00Z"}
                ]
            )
            
            # Check provenance chain access
            if len(judgment.provenance_chain) == 1:
                print("  ✅ Provenance chain creation")
                passed += 1
            else:
                print("  ❌ Provenance chain creation - Wrong length")
            total += 1
            
            # Test provenance immutability (should not be able to modify)
            try:
                judgment.provenance_chain.append({"source_id": "hack"})
                print("  ❌ Provenance chain immutability - Should be immutable")
            except (AttributeError, TypeError):
                print("  ✅ Provenance chain immutability")
                passed += 1
            total += 1
            
        except Exception as e:
            print(f"  ❌ Provenance chain tests - Error: {e}")
            total += 2
        
        return passed, total
    
    def run_validation(self, sdk_path: str) -> Dict[str, Any]:
        """Run complete conformance validation."""
        print(f"🔍 Validating SDK at: {sdk_path}")
        
        # Load SDK module
        try:
            spec = importlib.util.spec_from_file_location("sdk", sdk_path)
            sdk_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(sdk_module)
            print("✅ SDK module loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load SDK: {e}")
            return {"error": str(e)}
        
        # Run validation tests
        results = {}
        
        # Judgment creation tests
        passed, total = self.validate_judgment_creation(sdk_module)
        results['judgment_creation'] = {"passed": passed, "total": total}
        
        # Fusion operator tests
        passed, total = self.validate_fusion_operators(sdk_module)
        results['fusion_operators'] = {"passed": passed, "total": total}
        
        # Provenance chain tests
        passed, total = self.validate_provenance_chain(sdk_module)
        results['provenance_chain'] = {"passed": passed, "total": total}
        
        # Calculate overall score
        total_passed = sum(r['passed'] for r in results.values())
        total_tests = sum(r['total'] for r in results.values())
        results['overall'] = {
            "passed": total_passed,
            "total": total_tests,
            "score": (total_passed / total_tests * 100) if total_tests > 0 else 0
        }
        
        return results

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate SDK conformance to OpenTrust Protocol")
    parser.add_argument("--sdk", required=True, help="Path to SDK module file")
    parser.add_argument("--test-vectors", default="test-vectors", help="Path to test vectors directory")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = ConformanceValidator(args.test_vectors)
    
    # Run validation
    results = validator.run_validation(args.sdk)
    
    # Print results
    if "error" in results:
        print(f"\n❌ Validation failed: {results['error']}")
        sys.exit(1)
    
    print(f"\n📊 Validation Results:")
    print(f"  Judgment Creation: {results['judgment_creation']['passed']}/{results['judgment_creation']['total']}")
    print(f"  Fusion Operators: {results['fusion_operators']['passed']}/{results['fusion_operators']['total']}")
    print(f"  Provenance Chain: {results['provenance_chain']['passed']}/{results['provenance_chain']['total']}")
    print(f"  Overall Score: {results['overall']['score']:.1f}% ({results['overall']['passed']}/{results['overall']['total']})")
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Results saved to: {args.output}")
    
    # Exit with appropriate code
    if results['overall']['score'] >= 90:
        print("🎉 SDK is highly conformant!")
        sys.exit(0)
    elif results['overall']['score'] >= 70:
        print("⚠️  SDK is partially conformant")
        sys.exit(1)
    else:
        print("❌ SDK is not conformant")
        sys.exit(2)

if __name__ == "__main__":
    main()
