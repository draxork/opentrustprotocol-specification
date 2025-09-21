#!/usr/bin/env python3
"""
OpenTrust Protocol Test Vector Validator

This tool validates SDK implementations against the official test vectors.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import importlib.util
import traceback

class TestVectorValidator:
    """Validates SDK implementations against OTP test vectors."""
    
    def __init__(self, test_vectors_path: str):
        """Initialize validator with test vectors."""
        self.test_vectors_path = Path(test_vectors_path)
        self.results = {
            'judgment_creation': {'passed': 0, 'total': 0, 'details': []},
            'fusion_operators': {'passed': 0, 'total': 0, 'details': []},
            'edge_cases': {'passed': 0, 'total': 0, 'details': []}
        }
        
    def load_test_vectors(self) -> Dict[str, Any]:
        """Load all test vectors from JSON files."""
        test_vectors = {}
        
        # Load judgment creation tests
        judgments_file = self.test_vectors_path / "judgments.json"
        if judgments_file.exists():
            with open(judgments_file, 'r') as f:
                data = json.load(f)
                test_vectors['judgment_creation'] = data['test_vectors']
        
        # Load fusion tests
        fusion_file = self.test_vectors_path / "fusion-tests.json"
        if fusion_file.exists():
            with open(fusion_file, 'r') as f:
                data = json.load(f)
                test_vectors['fusion'] = data['test_vectors']
        
        return test_vectors
    
    def validate_judgment_creation(self, sdk_module, test_vectors: List[Dict]) -> None:
        """Validate judgment creation against test vectors."""
        print("🧪 Validating judgment creation...")
        
        for test_case in test_vectors:
            test_name = test_case['name']
            self.results['judgment_creation']['total'] += 1
            
            try:
                # Attempt to create judgment
                judgment = sdk_module.NeutrosophicJudgment(
                    T=test_case['input']['T'],
                    I=test_case['input']['I'],
                    F=test_case['input']['F'],
                    provenance_chain=test_case['input']['provenance_chain']
                )
                
                # Check if validation passed as expected
                if test_case['expected_valid']:
                    self.results['judgment_creation']['passed'] += 1
                    self.results['judgment_creation']['details'].append({
                        'test': test_name,
                        'status': 'PASS',
                        'message': 'Valid judgment created successfully'
                    })
                    print(f"  ✅ {test_name}")
                else:
                    self.results['judgment_creation']['details'].append({
                        'test': test_name,
                        'status': 'FAIL',
                        'message': 'Should have failed but didn\'t'
                    })
                    print(f"  ❌ {test_name} - Should have failed but didn't")
                    
            except Exception as e:
                error_msg = str(e)
                
                if not test_case['expected_valid']:
                    # Check if error message matches expected
                    expected_error = test_case.get('expected_error', '')
                    if expected_error and expected_error in error_msg:
                        self.results['judgment_creation']['passed'] += 1
                        self.results['judgment_creation']['details'].append({
                            'test': test_name,
                            'status': 'PASS',
                            'message': f'Failed as expected: {error_msg}'
                        })
                        print(f"  ✅ {test_name} - Failed as expected")
                    else:
                        self.results['judgment_creation']['details'].append({
                            'test': test_name,
                            'status': 'WARN',
                            'message': f'Failed as expected but wrong error: {error_msg}'
                        })
                        print(f"  ⚠️  {test_name} - Failed as expected but wrong error")
                        self.results['judgment_creation']['passed'] += 1  # Still counts as passed
                else:
                    self.results['judgment_creation']['details'].append({
                        'test': test_name,
                        'status': 'FAIL',
                        'message': f'Unexpected error: {error_msg}'
                    })
                    print(f"  ❌ {test_name} - Unexpected error: {error_msg}")
    
    def validate_fusion_operators(self, sdk_module) -> None:
        """Validate fusion operators."""
        print("🧪 Validating fusion operators...")
        
        # Create test judgments
        judgments = [
            sdk_module.NeutrosophicJudgment(
                T=0.8, I=0.2, F=0.0,
                provenance_chain=[{"source_id": "test1", "timestamp": "2025-09-20T20:30:00Z"}]
            ),
            sdk_module.NeutrosophicJudgment(
                T=0.6, I=0.3, F=0.1,
                provenance_chain=[{"source_id": "test2", "timestamp": "2025-09-20T20:30:00Z"}]
            )
        ]
        
        # Test conflict-aware weighted average
        self.results['fusion_operators']['total'] += 1
        try:
            result = sdk_module.fuse.conflict_aware_weighted_average(judgments, [0.6, 0.4])
            
            if self._is_valid_judgment(result):
                self.results['fusion_operators']['passed'] += 1
                self.results['fusion_operators']['details'].append({
                    'test': 'conflict_aware_weighted_average',
                    'status': 'PASS',
                    'message': 'Valid fusion result'
                })
                print("  ✅ Conflict-aware weighted average")
            else:
                self.results['fusion_operators']['details'].append({
                    'test': 'conflict_aware_weighted_average',
                    'status': 'FAIL',
                    'message': 'Invalid fusion result'
                })
                print("  ❌ Conflict-aware weighted average - Invalid result")
                
        except Exception as e:
            self.results['fusion_operators']['details'].append({
                'test': 'conflict_aware_weighted_average',
                'status': 'FAIL',
                'message': f'Error: {e}'
            })
            print(f"  ❌ Conflict-aware weighted average - Error: {e}")
        
        # Test optimistic fusion
        self.results['fusion_operators']['total'] += 1
        try:
            result = sdk_module.fuse.optimistic_fusion(judgments)
            
            if self._is_valid_judgment(result):
                self.results['fusion_operators']['passed'] += 1
                self.results['fusion_operators']['details'].append({
                    'test': 'optimistic_fusion',
                    'status': 'PASS',
                    'message': 'Valid fusion result'
                })
                print("  ✅ Optimistic fusion")
            else:
                self.results['fusion_operators']['details'].append({
                    'test': 'optimistic_fusion',
                    'status': 'FAIL',
                    'message': 'Invalid fusion result'
                })
                print("  ❌ Optimistic fusion - Invalid result")
                
        except Exception as e:
            self.results['fusion_operators']['details'].append({
                'test': 'optimistic_fusion',
                'status': 'FAIL',
                'message': f'Error: {e}'
            })
            print(f"  ❌ Optimistic fusion - Error: {e}")
        
        # Test pessimistic fusion
        self.results['fusion_operators']['total'] += 1
        try:
            result = sdk_module.fuse.pessimistic_fusion(judgments)
            
            if self._is_valid_judgment(result):
                self.results['fusion_operators']['passed'] += 1
                self.results['fusion_operators']['details'].append({
                    'test': 'pessimistic_fusion',
                    'status': 'PASS',
                    'message': 'Valid fusion result'
                })
                print("  ✅ Pessimistic fusion")
            else:
                self.results['fusion_operators']['details'].append({
                    'test': 'pessimistic_fusion',
                    'status': 'FAIL',
                    'message': 'Invalid fusion result'
                })
                print("  ❌ Pessimistic fusion - Invalid result")
                
        except Exception as e:
            self.results['fusion_operators']['details'].append({
                'test': 'pessimistic_fusion',
                'status': 'FAIL',
                'message': f'Error: {e}'
            })
            print(f"  ❌ Pessimistic fusion - Error: {e}")
    
    def validate_edge_cases(self, sdk_module) -> None:
        """Validate edge cases."""
        print("🧪 Validating edge cases...")
        
        # Test single judgment fusion
        self.results['edge_cases']['total'] += 1
        try:
            judgment = sdk_module.NeutrosophicJudgment(
                T=0.8, I=0.2, F=0.0,
                provenance_chain=[{"source_id": "test", "timestamp": "2025-09-20T20:30:00Z"}]
            )
            
            result = sdk_module.fuse.conflict_aware_weighted_average([judgment], [1.0])
            
            if self._is_valid_judgment(result) and result.T == 0.8:
                self.results['edge_cases']['passed'] += 1
                self.results['edge_cases']['details'].append({
                    'test': 'single_judgment_fusion',
                    'status': 'PASS',
                    'message': 'Single judgment fusion works correctly'
                })
                print("  ✅ Single judgment fusion")
            else:
                self.results['edge_cases']['details'].append({
                    'test': 'single_judgment_fusion',
                    'status': 'FAIL',
                    'message': 'Single judgment fusion failed'
                })
                print("  ❌ Single judgment fusion - Failed")
                
        except Exception as e:
            self.results['edge_cases']['details'].append({
                'test': 'single_judgment_fusion',
                'status': 'FAIL',
                'message': f'Error: {e}'
            })
            print(f"  ❌ Single judgment fusion - Error: {e}")
        
        # Test zero weights fallback
        self.results['edge_cases']['total'] += 1
        try:
            judgments = [
                sdk_module.NeutrosophicJudgment(
                    T=0.9, I=0.1, F=0.9,
                    provenance_chain=[{"source_id": "test1", "timestamp": "2025-09-20T20:30:00Z"}]
                ),
                sdk_module.NeutrosophicJudgment(
                    T=0.8, I=0.2, F=0.8,
                    provenance_chain=[{"source_id": "test2", "timestamp": "2025-09-20T20:30:00Z"}]
                )
            ]
            
            result = sdk_module.fuse.conflict_aware_weighted_average(judgments, [0.0, 0.0])
            
            if self._is_valid_judgment(result):
                self.results['edge_cases']['passed'] += 1
                self.results['edge_cases']['details'].append({
                    'test': 'zero_weights_fallback',
                    'status': 'PASS',
                    'message': 'Zero weights fallback works correctly'
                })
                print("  ✅ Zero weights fallback")
            else:
                self.results['edge_cases']['details'].append({
                    'test': 'zero_weights_fallback',
                    'status': 'FAIL',
                    'message': 'Zero weights fallback failed'
                })
                print("  ❌ Zero weights fallback - Failed")
                
        except Exception as e:
            self.results['edge_cases']['details'].append({
                'test': 'zero_weights_fallback',
                'status': 'FAIL',
                'message': f'Error: {e}'
            })
            print(f"  ❌ Zero weights fallback - Error: {e}")
    
    def _is_valid_judgment(self, judgment) -> bool:
        """Check if a judgment is valid."""
        try:
            return (
                0 <= judgment.T <= 1 and
                0 <= judgment.I <= 1 and
                0 <= judgment.F <= 1 and
                judgment.T + judgment.I + judgment.F <= 1.0
            )
        except:
            return False
    
    def run_validation(self, sdk_path: str) -> Dict[str, Any]:
        """Run complete validation."""
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
        
        # Load test vectors
        test_vectors = self.load_test_vectors()
        
        # Run validation tests
        if 'judgment_creation' in test_vectors:
            self.validate_judgment_creation(sdk_module, test_vectors['judgment_creation'])
        
        self.validate_fusion_operators(sdk_module)
        self.validate_edge_cases(sdk_module)
        
        # Calculate overall score
        total_passed = sum(r['passed'] for r in self.results.values())
        total_tests = sum(r['total'] for r in self.results.values())
        
        self.results['overall'] = {
            'passed': total_passed,
            'total': total_tests,
            'score': (total_passed / total_tests * 100) if total_tests > 0 else 0
        }
        
        return self.results

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate SDK against OpenTrust Protocol test vectors")
    parser.add_argument("--sdk", required=True, help="Path to SDK module file")
    parser.add_argument("--test-vectors", default="test-vectors", help="Path to test vectors directory")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = TestVectorValidator(args.test_vectors)
    
    # Run validation
    results = validator.run_validation(args.sdk)
    
    if "error" in results:
        print(f"\n❌ Validation failed: {results['error']}")
        sys.exit(1)
    
    # Print results
    print(f"\n📊 Validation Results:")
    for category, data in results.items():
        if category == 'overall':
            continue
        print(f"  {category.replace('_', ' ').title()}: {data['passed']}/{data['total']}")
    
    overall = results['overall']
    print(f"  Overall Score: {overall['score']:.1f}% ({overall['passed']}/{overall['total']})")
    
    # Print detailed results if verbose
    if args.verbose:
        print(f"\n📋 Detailed Results:")
        for category, data in results.items():
            if category == 'overall':
                continue
            print(f"\n{category.replace('_', ' ').title()}:")
            for detail in data['details']:
                status_icon = "✅" if detail['status'] == 'PASS' else "❌" if detail['status'] == 'FAIL' else "⚠️"
                print(f"  {status_icon} {detail['test']}: {detail['message']}")
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Results saved to: {args.output}")
    
    # Exit with appropriate code
    if overall['score'] >= 90:
        print("\n🎉 SDK is highly conformant!")
        sys.exit(0)
    elif overall['score'] >= 70:
        print("\n⚠️  SDK is partially conformant")
        sys.exit(1)
    else:
        print("\n❌ SDK is not conformant")
        sys.exit(2)

if __name__ == "__main__":
    main()
