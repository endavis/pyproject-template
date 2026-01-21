# ADR-0013: Python version support policy with bookend CI strategy

## Status

Accepted

## Decision

Adopt a tiered Python version support policy:

1. **Active support**: Last 3 major Python versions, tested on every PR using bookend strategy (oldest + newest)
2. **Passive compatibility**: Older versions that still pass CI, tested on-demand via `full-matrix` label
3. **Deprecation**: Versions removed from CI when tests fail, with final compatible release tagged

CI matrix strategy:
- **Default (6 jobs)**: Bookend versions (oldest + newest active) × 3 OSes
- **Full matrix (9-15 jobs)**: All supported versions × 3 OSes, triggered by `full-matrix` label

## Rationale

Testing every Python version on every PR creates excessive CI load without proportional benefit. The bookend strategy (testing oldest and newest supported versions) catches most compatibility issues:
- If code works on 3.12 and 3.14, it almost certainly works on 3.13
- Full matrix testing is available when needed (releases, compatibility-sensitive changes)
- Passive compatibility allows supporting older versions without maintenance burden
- Clear deprecation process with tagged releases protects users on older Python versions

## Related Issues

- Issue #168: Add Python 3.14 to CI testing matrix

## Related Documentation

- [CI/CD Testing Guide - Python Version Support Policy](../development/ci-cd-testing.md#python-version-support-policy)
