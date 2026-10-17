# SAST and SCA Scan Summary

## 1. Static Application Security Testing

- Tool: Semgrep OSS
- Command: `semgrep scan --config auto api/`
- Files scanned: 3 tracked API files
- Rules executed: 296
- Findings: 0
- Result: Scan completed successfully.

**Interpretation:** No findings were reported by the rules applied to the scanned files. This does not prove the application is vulnerability-free or that business-logic flaws are absent.

## 2. Software Composition Analysis

- Tool: `pip-audit`
- Target: `api/requirements.txt`
- Observed result: No known vulnerabilities reported in the audited dependencies.

**Interpretation:** This result applies to the dependency set and vulnerability data checked at scan time. It does not establish that every package is trustworthy, correctly pinned, or free from undisclosed vulnerabilities.

## 3. Secure AI-assisted development recommendations

1. Run SAST and dependency checks on every pull request and in CI.
2. Review AI-generated code for missing authorization, unsafe defaults, data leakage and incorrect business rules.
3. Verify AI-suggested package names, maintainers, source repositories and release history before installation.
4. Pin approved dependency versions and maintain lockfiles and a software bill of materials.
5. Require human review and regression tests for security-sensitive changes.

## 4. Limitations

The recorded scans do not demonstrate a complete CI/CD pipeline or prove that a secret-scanning hook blocks commits. Those controls require separate verification. No scanner can replace manual review and application-specific security tests.
