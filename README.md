# OpenTrust Protocol Specification

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/draxork/opentrustprotocol-specification)
[![Spec Status](https://img.shields.io/badge/spec-stable-green.svg)](https://github.com/draxork/opentrustprotocol-specification)

## 📋 Overview

This repository contains the official specification for the OpenTrust Protocol (OTP), the open standard for auditable trust using neutrosophic judgments.

## 🏗️ Architecture

The OpenTrust Protocol provides a standardized way to:
- **Measure trust** using Truth (T), Indeterminacy (I), and Falsity (F) components
- **Fuse multiple judgments** with conflict-aware algorithms
- **Maintain provenance chains** for complete auditability
- **Transform data** using OTP Mappers (Numerical, Categorical, Boolean)
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

- **Python SDK**: https://github.com/draxork/opentrustprotocol-py
- **JavaScript SDK**: https://github.com/draxork/opentrustprotocol-js
- **Rust SDK**: https://github.com/draxork/opentrustprotocol-rs
- **PyPI Package**: https://pypi.org/project/opentrustprotocol/
- **npm Package**: https://www.npmjs.com/package/opentrustprotocol
- **Crates.io Package**: https://crates.io/crates/opentrustprotocol

## 📊 Status

| Component | Status | Version | Package Manager |
|-----------|--------|---------|-----------------|
| Core Spec | ✅ Stable | 2.0.0 | - |
| Test Vectors | ✅ Stable | 2.0.0 | - |
| API Spec | ✅ Stable | 2.0.0 | - |
| Python SDK | ✅ Published | 1.0.6 | [PyPI](https://pypi.org/project/opentrustprotocol/) |
| JavaScript SDK | ✅ Published | 1.0.3 | [npm](https://www.npmjs.com/package/opentrustprotocol) |
| Rust SDK | ✅ Published | 0.2.0 | [crates.io](https://crates.io/crates/opentrustprotocol) |

## 🆕 OTP v2.0 Features

### **OTP Mapper System**
- **NumericalMapper**: Continuous data interpolation (DeFi health factors, IoT sensors)
- **CategoricalMapper**: Discrete category mapping (KYC status, product categories)
- **BooleanMapper**: Boolean value transformation (SSL certificates, feature flags)

### **Enhanced Fusion Operators**
- **Conflict-Aware Weighted Average**: Primary fusion operator with conflict detection
- **Optimistic Fusion**: Maximum truth, minimum falsity
- **Pessimistic Fusion**: Minimum truth, maximum falsity

### **Provenance Chain**
- **Complete Audit Trail**: Every transformation tracked
- **Immutable History**: Cannot be modified after creation
- **Source Attribution**: Full traceability to original data

## 🌐 Ecosystem

The OpenTrust Protocol is now available across multiple platforms:

| Platform | Package | Version | Status |
|----------|---------|---------|--------|
| **Python** | `opentrustprotocol` | 1.0.6 | ✅ Published |
| **JavaScript** | `opentrustprotocol` | 1.0.3 | ✅ Published |
| **Rust** | `opentrustprotocol` | 0.2.0 | ✅ Published |

## 📈 Installation

```bash
# Python
pip install opentrustprotocol

# JavaScript/Node.js
npm install opentrustprotocol

# Rust
cargo add opentrustprotocol
```

## 🎯 Use Cases

- **🔗 Blockchain & DeFi**: Risk assessment, KYC/AML, oracle reliability
- **🤖 AI & Machine Learning**: Uncertainty quantification, model validation
- **🌐 IoT & Sensors**: Sensor reliability, data fusion, anomaly detection
- **🏭 Supply Chain**: Product tracking, quality control, compliance

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/draxork/opentrustprotocol-specification/issues)
- **Discussions**: [GitHub Discussions](https://github.com/draxork/opentrustprotocol-specification/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/draxork/opentrustprotocol-specification/wiki)

---

<div align="center">

**🌟 Star this repository if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/draxork/opentrustprotocol-specification?style=social)](https://github.com/draxork/opentrustprotocol-specification)

**Made with ❤️ by the OpenTrust Protocol Team**

</div>