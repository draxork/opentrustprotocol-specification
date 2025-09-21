# OpenTrust Protocol Specification

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/opentrustprotocol/specification)
[![Spec Status](https://img.shields.io/badge/spec-stable-green.svg)](https://opentrustprotocol.com)

## 📋 Overview

This repository contains the official specification for the OpenTrust Protocol (OTP), the open standard for auditable trust using neutrosophic judgments.

## 🏗️ Architecture

The OpenTrust Protocol provides a standardized way to:
- **Measure trust** using Truth (T), Indeterminacy (I), and Falsity (F) components
- **Fuse multiple judgments** with conflict-aware algorithms
- **Maintain provenance chains** for complete auditability
- **Ensure interoperability** across different implementations

## 📁 Repository Structure

```
├── specification/          # Core protocol specification
│   ├── core-spec.md       # Main specification document
│   ├── fusion-operators.md # Mathematical definitions
│   ├── provenance-chain.md # Audit trail specification
│   └── api-spec.yaml      # OpenAPI 3.0 specification
├── test-vectors/          # Standard test cases
│   ├── judgments.json     # Judgment creation tests
│   ├── fusion-tests.json  # Fusion operation tests
│   └── edge-cases.json    # Edge case scenarios
├── compliance/            # Conformance requirements
│   ├── validation-rules.md # Validation requirements
│   └── conformance-tests.md # Test suite requirements
├── tools/                 # Validation and testing tools
│   ├── validator/         # Conformance validator
│   └── test-runner/       # Test vector runner
└── implementations/       # Reference implementations
    ├── python/            # Python SDK reference
    ├── javascript/        # JavaScript SDK reference
    └── rust/              # Rust SDK reference
```

## 🎯 Quick Start

### For Implementers

1. **Read the specification**: Start with [`specification/core-spec.md`](specification/core-spec.md)
2. **Run test vectors**: Use the provided test cases to validate your implementation
3. **Check conformance**: Run the compliance validator against your SDK

### For Users

1. **Choose your SDK**: Check the [implementations](implementations/) directory
2. **Install and use**: Follow the SDK-specific documentation
3. **Report issues**: Use the GitHub issue tracker

## 🧪 Testing

### Run Test Vectors

```bash
# Validate against test vectors
python tools/test-runner/validate_vectors.py --sdk your-implementation
```

### Check Conformance

```bash
# Run conformance tests
python tools/validator/check_conformance.py --sdk your-implementation
```

## 📚 Documentation

- **[Core Specification](specification/core-spec.md)** - Complete protocol definition
- **[API Specification](specification/api-spec.yaml)** - OpenAPI 3.0 definition
- **[Test Vectors](test-vectors/)** - Standard test cases
- **[Compliance Guide](compliance/)** - Conformance requirements

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Run the test suite**
5. **Submit a pull request**

### Contribution Guidelines

- All changes must be backward compatible
- New features require test vectors
- Documentation must be updated
- All tests must pass

## 📄 License

This specification is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Links

- **Website**: https://opentrustprotocol.com
- **Documentation**: https://docs.opentrustprotocol.com
- **SDKs**: https://github.com/opentrustprotocol/sdks
- **Community**: https://discord.gg/opentrustprotocol

## 📊 Status

| Component | Status | Version |
|-----------|--------|---------|
| Core Spec | ✅ Stable | 1.0.0 |
| Test Vectors | ✅ Stable | 1.0.0 |
| API Spec | ✅ Stable | 1.0.0 |
| Python SDK | ✅ Stable | 1.0.2 |
| JavaScript SDK | 🚧 In Progress | - |
| Rust SDK | 📋 Planned | - |
