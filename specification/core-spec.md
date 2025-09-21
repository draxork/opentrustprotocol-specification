# OpenTrust Protocol - Core Specification v1.0

## 1. Introduction

The OpenTrust Protocol (OTP) is an open standard for measuring and auditing trust using neutrosophic judgments. It provides a mathematical framework for representing uncertainty and confidence in trust assessments.

## 2. Core Concepts

### 2.1 Neutrosophic Judgment

A neutrosophic judgment is a mathematical structure that represents the degree of trust in a statement or assessment using three components:

- **T (Truth)**: The degree to which the statement is considered true [0.0, 1.0]
- **I (Indeterminacy)**: The degree of uncertainty or lack of information [0.0, 1.0]
- **F (Falsity)**: The degree to which the statement is considered false [0.0, 1.0]

### 2.2 Conservation Constraint

All neutrosophic judgments must satisfy the conservation constraint:

```
T + I + F ≤ 1.0
```

This ensures that the total "belief mass" does not exceed 100%.

### 2.3 Provenance Chain

Every judgment includes an immutable provenance chain that tracks:
- Source identification
- Timestamps
- Descriptions
- Metadata

## 3. Data Structures

### 3.1 NeutrosophicJudgment

```json
{
  "T": 0.85,
  "I": 0.15,
  "F": 0.0,
  "provenance_chain": [
    {
      "source_id": "model-text-bison-v1.2",
      "timestamp": "2025-09-20T20:30:00Z",
      "description": "AI model confidence score",
      "metadata": {
        "model_version": "1.2",
        "confidence_threshold": 0.8
      }
    }
  ]
}
```

### 3.2 ProvenanceEntry

```json
{
  "source_id": "string",
  "timestamp": "ISO8601",
  "description": "string",
  "metadata": {}
}
```

## 4. Validation Rules

### 4.1 Judgment Validation

1. **Range Validation**: T, I, F must be in range [0.0, 1.0]
2. **Conservation Constraint**: T + I + F ≤ 1.0
3. **Provenance Chain**: Must be a non-empty array of ProvenanceEntry objects
4. **Immutability**: Provenance chain cannot be modified after creation

### 4.2 Fusion Input Validation

1. **Non-empty**: Judgments array must contain at least one judgment
2. **Weight Matching**: Weights array length must match judgments array length
3. **Weight Range**: All weights must be non-negative
4. **Non-zero Weights**: At least one weight must be positive

## 5. Fusion Operators

### 5.1 Conflict-Aware Weighted Average (CAWA)

This is the primary fusion operator that adjusts weights based on conflicts between judgments.

#### Algorithm

```mathematical
For each judgment i:
  conflict_factor[i] = T[i] * F[i]
  adjusted_weight[i] = weight[i] * (1 - conflict_factor[i])

normalize_factor = sum(adjusted_weights)
normalized_weight[i] = adjusted_weight[i] / normalize_factor

T_result = Σ(T[i] * normalized_weight[i])
I_result = Σ(I[i] * normalized_weight[i])
F_result = Σ(F[i] * normalized_weight[i])
```

#### Special Cases

- **All weights zero**: Fallback to unweighted average
- **All conflicts = 1**: Use original weights
- **Single judgment**: Return judgment unchanged

### 5.2 Optimistic Fusion

Takes the most optimistic view by maximizing truth and minimizing falsity.

```mathematical
T_result = max(T[i])
F_result = min(F[i])
I_result = mean(I[i])
```

### 5.3 Pessimistic Fusion

Takes the most pessimistic view by minimizing truth and maximizing falsity.

```mathematical
T_result = min(T[i])
F_result = max(F[i])
I_result = mean(I[i])
```

## 6. Provenance Chain Management

### 6.1 Fusion Provenance

When performing fusion operations, a new provenance entry must be added:

```json
{
  "source_id": "otp-cawa-v1.0",
  "timestamp": "2025-09-20T20:30:00Z",
  "description": "Conflict-aware weighted average fusion",
  "metadata": {
    "operator": "conflict_aware_weighted_average",
    "weights": [0.6, 0.4],
    "input_count": 2,
    "version": "1.0"
  }
}
```

### 6.2 Chain Immutability

- Provenance chains are immutable once created
- Fusion operations create new judgments with extended chains
- Original judgments remain unchanged
- Chain length grows with each fusion operation

## 7. Error Handling

### 7.1 Validation Errors

| Error Type | Description | HTTP Status |
|------------|-------------|-------------|
| `INVALID_RANGE` | T, I, F values outside [0.0, 1.0] | 400 |
| `CONSERVATION_VIOLATION` | T + I + F > 1.0 | 400 |
| `INVALID_PROVENANCE` | Malformed provenance chain | 400 |
| `EMPTY_JUDGMENTS` | No judgments provided for fusion | 400 |
| `WEIGHT_MISMATCH` | Weights array length ≠ judgments array length | 400 |
| `ALL_ZERO_WEIGHTS` | All weights are zero | 400 |

### 7.2 Fallback Behavior

- **Zero weights**: Fallback to unweighted average
- **Empty judgments**: Return error (no fallback)
- **Invalid ranges**: Return validation error
- **Conservation violation**: Return validation error

## 8. Performance Requirements

### 8.1 Computational Complexity

- **Judgment Creation**: O(1)
- **Single Fusion**: O(n) where n = number of judgments
- **Provenance Chain Access**: O(1) for latest entry, O(n) for full chain

### 8.2 Memory Requirements

- **Judgment Storage**: O(p) where p = provenance chain length
- **Fusion Operations**: O(n) temporary memory for weight calculations

## 9. Security Considerations

### 9.1 Input Validation

- All inputs must be validated before processing
- No code injection through provenance metadata
- Bounds checking on all numerical values

### 9.2 Provenance Integrity

- Provenance chains cannot be tampered with
- Timestamps should be validated for reasonableness
- Source IDs should be sanitized

## 10. Extensibility

### 10.1 Custom Fusion Operators

Implementations may add custom fusion operators beyond the three standard ones:

1. **Conflict-Aware Weighted Average** (Required)
2. **Optimistic Fusion** (Required)
3. **Pessimistic Fusion** (Required)
4. **Custom Operators** (Optional)

### 10.2 Metadata Extensions

Provenance metadata can be extended with custom fields:

```json
{
  "source_id": "custom-source",
  "timestamp": "2025-09-20T20:30:00Z",
  "description": "Custom assessment",
  "metadata": {
    "custom_field": "value",
    "version": "1.0",
    "additional_data": {}
  }
}
```

## 11. Compliance Requirements

### 11.1 Must Implement

- All three standard fusion operators
- Complete input validation
- Provenance chain management
- Error handling for all specified cases
- Conservation constraint enforcement

### 11.2 Should Implement

- JSON serialization/deserialization
- Type safety (where applicable)
- Comprehensive test suite
- Performance benchmarks
- Documentation

### 11.3 May Implement

- Additional fusion operators
- Caching mechanisms
- Async operations
- Custom metadata validation
- Binary serialization formats
