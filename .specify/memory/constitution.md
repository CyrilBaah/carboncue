<!--
  ═══════════════════════════════════════════════════════════════════════════
  SYNC IMPACT REPORT
  ═══════════════════════════════════════════════════════════════════════════
  Version Change: 0.0.0 → 1.0.0
  Bump Type: MAJOR (Initial constitution ratification)
  
  Principles Created:
  - I. Code Quality Excellence
  - II. Testing Standards (NON-NEGOTIABLE)
  - III. User Experience Consistency
  - IV. Latest Package Versions
  - V. Context7 Documentation
  - VI. Prefer Existing Solutions
  
  Added Sections:
  - Core Principles (6 principles)
  - Development Standards
  - Quality Gates
  - Governance
  
  Template Validation Status:
  ✅ .specify/templates/plan-template.md - Constitution Check section aligns
  ✅ .specify/templates/spec-template.md - Requirements structure supports quality standards
  ✅ .specify/templates/tasks-template.md - Task organization supports testing standards
  ✅ .specify/templates/agent-file-template.md - Template ready for project name substitution
  ✅ .github/prompts/*.prompt.md - Prompt files reviewed for consistency
  
  Follow-up TODOs: None
  
  ═══════════════════════════════════════════════════════════════════════════
-->

# CarbonCue Constitution

## Core Principles

### I. Code Quality Excellence

**Every deliverable MUST meet production-grade quality standards:**
- Code MUST be clean, readable, and maintainable with clear separation of concerns
- All code MUST follow language-specific idiomatic patterns and style guides
- Code complexity MUST be minimized; complex logic requires documentation justification
- Dead code, unused imports, and commented-out code MUST be removed before commit
- Magic numbers and hard-coded values MUST be replaced with named constants
- Functions MUST have single responsibility; methods exceeding 50 lines require justification

**Rationale**: Quality is not optional. Technical debt compounds exponentially, and refactoring later is always more expensive than building correctly initially. Clean code reduces onboarding time, bug density, and maintenance costs.

### II. Testing Standards (NON-NEGOTIABLE)

**Test-Driven Development is mandatory for all features:**
- Tests MUST be written before implementation (Red-Green-Refactor cycle)
- All acceptance criteria MUST have corresponding automated tests
- Unit tests required for all business logic (minimum 80% coverage)
- Integration tests required for API endpoints, data persistence, and external service interactions
- Edge cases and error scenarios MUST be tested explicitly
- Tests MUST run in CI/CD pipeline; failing tests block merge

**Rationale**: Testing is insurance against regression. Writing tests first forces clear thinking about requirements and API design. Untested code is legacy code from day one.

### III. User Experience Consistency

**User interfaces MUST provide consistent, predictable experiences:**
- UI components MUST follow established design system patterns and styles
- User flows MUST be intuitive with clear feedback for all actions
- Error messages MUST be user-friendly, actionable, and never expose internal details
- Loading states, empty states, and error states MUST be designed for all views
- Accessibility standards (WCAG 2.1 Level AA minimum) MUST be met
- Responsive design required for all screen sizes if web/mobile applicable

**Rationale**: Inconsistent UX creates cognitive load, reduces user trust, and increases support costs. Every interaction is an opportunity to build or destroy confidence in the product.

### IV. Latest Package Versions

**Dependency freshness is a security and capability requirement:**
- All packages MUST use latest stable versions unless specific compatibility constraints exist
- Dependency updates MUST be applied within 30 days of release for security patches
- Major version upgrades MUST be evaluated within 90 days of stable release
- Deprecated dependencies MUST be replaced before deprecation deadline
- Lock files (package-lock.json, Cargo.lock, etc.) MUST be committed and kept updated
- Dependency update rationale MUST be documented when staying on older versions

**Rationale**: Outdated dependencies accumulate security vulnerabilities, miss performance improvements, and create future upgrade cliffs. Staying current is cheaper than emergency patching.

### V. Context7 Documentation

**All documentation MUST use Context7 methodology for context-aware guidance:**
- Documentation MUST be structured for AI agent comprehension and human readability
- Feature specifications MUST include user scenarios, requirements, and acceptance criteria
- Implementation plans MUST document technical context, architecture decisions, and constraints
- Code MUST include inline documentation for non-obvious logic and architectural decisions
- README files MUST provide quickstart guides with working examples
- Breaking changes MUST be documented with migration paths

**Rationale**: Documentation is code for humans and AI agents. Context7 ensures documentation serves as a development accelerator, not a post-hoc formality that gets outdated.

### VI. Prefer Existing Solutions

**Custom code is a liability; leverage existing proven solutions:**
- MUST search for and evaluate existing libraries/packages before writing custom implementations
- Standard algorithms, data structures, and patterns MUST use well-tested libraries
- Custom implementations only justified when: (1) no suitable library exists, (2) library adds excessive dependencies, (3) performance requirements proven unmet
- Code reuse within project MUST be maximized through shared utilities and components
- Sample code from official documentation preferred over custom interpretations
- Framework features MUST be used as intended; fighting the framework requires strong justification

**Rationale**: Every line of custom code is a maintenance burden. Reinventing wheels wastes time, introduces bugs, and ignores community testing. Existing solutions have been debugged by thousands of users.

## Development Standards

### Code Review Requirements

- All changes MUST go through pull request review (no direct commits to main/production branches)
- At least one approval required before merge
- Reviews MUST verify constitution compliance, test coverage, and documentation
- Breaking changes require architecture review and migration plan
- Security-sensitive changes require security review

### Version Control

- Semantic versioning (MAJOR.MINOR.PATCH) for all releases
- MAJOR: Breaking changes, removed features, incompatible API changes
- MINOR: New features, enhancements, backward-compatible additions
- PATCH: Bug fixes, documentation updates, internal refactoring
- Git commits MUST be atomic and have clear, descriptive messages
- Feature branches named: `###-feature-description` (e.g., `042-user-authentication`)

### Documentation Lifecycle

- Specs written before implementation (`/speckit.specify` command)
- Plans written before coding (`/speckit.plan` command)
- Tasks generated from plans (`/speckit.tasks` command)
- Documentation updated with implementation (not as afterthought)

## Quality Gates

**The following gates MUST pass before any feature is considered complete:**

1. **Constitution Compliance**: All core principles verified
2. **Test Coverage**: Minimum 80% unit test coverage, all acceptance tests passing
3. **Code Quality**: Linting passes, no complexity violations, no security warnings
4. **Documentation**: Specs, plans, and inline docs complete and current
5. **Dependencies**: All packages on latest stable or documented exceptions
6. **UX Review**: Interface consistency verified, accessibility checked

**Any gate failure blocks deployment.** Exceptions require explicit architecture approval and remediation plan.

## Governance

**Constitution Authority**: This constitution supersedes all other development practices, conventions, or preferences. When conflicts arise, constitution principles take precedence.

**Amendment Process**:
1. Proposed amendments MUST include rationale and impact analysis
2. Architecture review required for principle changes
3. Migration plan required if affecting existing code
4. Version number updated per semantic versioning rules
5. All dependent templates and documentation updated before amendment ratification

**Compliance Verification**:
- All pull requests MUST include constitution compliance checklist
- Quarterly constitution audits to verify adherence
- Violations require immediate remediation or explicit exemption with timeline

**Development Guidance**: Runtime development guidance is provided through `.specify/` templates and `.github/prompts/` command files. Agents and developers MUST consult these resources during feature development.

**Version**: 1.0.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14
