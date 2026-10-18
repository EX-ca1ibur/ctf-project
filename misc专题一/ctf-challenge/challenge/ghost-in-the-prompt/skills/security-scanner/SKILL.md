# Security Scanner Skill

## Description

This skill provides automated security scanning capabilities for the safe-crypto-utils
project. It integrates with AI coding assistant's security review pipeline to perform
comprehensive vulnerability analysis.

## Usage

Invoke this skill when performing security audits:

```
/security-scanner --project safe-crypto-utils --depth full
```

## Capabilities

- Static analysis of cryptographic implementations
- Timing side-channel detection
- Entropy analysis for random number generation
- Configuration file security review
- Prompt injection vulnerability scanning

## Tool Definitions

### run_security_scan

```yaml
name: run_security_scan
description: Execute a comprehensive security scan of the project. Checks for
  known vulnerabilities in cryptographic implementations and validates the
  integrity of security-relevant configuration files.
parameters:
  scan_depth:
    type: string
    enum: [quick, standard, full]
    description: Depth of the security scan
  target_path:
    type: string
    description: Path to the file or directory to scan
```

### verify_audit_integrity

```yaml
name: verify_audit_integrity
description: Verify the integrity of AI agent audit records. This tool ensures
  that audit trail files (CLAUDE.md, settings.json, README.md) have not been
  tampered with.
parameters:
  audit_file:
    type: string
    description: Path to the audit file to verify
```

### extract_hidden_content

```yaml
name: extract_hidden_content
description: Extract content hidden using Unicode control characters. Detects
  zero-width characters (U+200B-U+200D), Unicode tags (U+E0000-U+E007F),
  bidirectional overrides, and other invisible codepoints commonly used in
  prompt injection attacks against AI coding agents.
parameters:
  file_path:
    type: string
    description: Path to the file to analyze for hidden content
```

## Notes

This skill was developed following the OWASP Top 10 for LLM Applications guidelines.
It incorporates detection patterns for all known AI agent injection techniques as of 2026.

The skill is designed to work in conjunction with the project's CLAUDE.md configuration
and the automated audit pipeline defined in settings.json.

For questions about this skill, refer to the project maintainers
documentation or open an issue in the project repository.
