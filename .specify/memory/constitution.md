<!--
SYNC IMPACT REPORT
Version change: INITIAL → 1.0.0
Modified principles: N/A (initial creation)
Added sections: All core principles and governance
Removed sections: None
Templates requiring updates:
  ✅ .specify/templates/plan-template.md - constitution check section
  ✅ .specify/templates/spec-template.md - scope alignment verified  
  ✅ .specify/templates/tasks-template.md - task categorization verified
Follow-up TODOs: None
-->

# TicTacTocToe-Engine Constitution

## Core Principles

### I. Engine Isolation (NON-NEGOTIABLE)

The game engine MUST remain isolated in the TTTTengine/ subdirectory with no external dependencies. All source files (TTTT.c, TTTT.h, TTTTapi.c, TTTTapi.h, TTTTcommon.h, main.c) MUST be pure C code with no third-party libraries. The engine operates independently of build files, test scripts, and utilities outside the source folder.

**Rationale**: Maintains portability, predictability, and ensures the engine can be embedded in any C-compatible environment without dependency conflicts.

### II. API Stability

Existing API functions in TTTTapi.h MUST NOT be modified or removed. New API additions MUST follow current naming conventions (TTTT_prefix, CamelCase for types, snake_case where established). All API changes MUST maintain backward compatibility.

**Rationale**: Preserves integration stability for existing clients and ensures consistent developer experience.

### III. Test-Driven Validation

All engine modifications MUST pass existing test suites (functional.py, tournament.py). New features MUST include corresponding test cases. Tests MUST run against the compiled tttt executable using subprocess communication, not direct library linking.

**Rationale**: Ensures behavioral consistency and prevents regressions in the game logic and CLI interface.

### IV. Heuristic Weight Flexibility

The engine MUST support dynamic heuristic weight adjustment through the existing weight matrix system. Tournament mode MUST facilitate weight comparison experiments. Weight modifications MUST be runtime-configurable without requiring recompilation.

**Rationale**: Enables the primary goal of creating varied gameplay through weight experimentation and competitive analysis.

### V. Cross-Platform Build Compatibility

Code MUST compile successfully on both macOS (Xcode) and Linux/Unix (make). No platform-specific dependencies or compiler extensions are permitted. Build outputs MUST be functionally equivalent across platforms.

**Rationale**: Maintains the project's established multi-platform support and ensures consistent behavior regardless of development environment.

## Development Constraints

### Technology Stack Requirements

- **Language**: Pure C (C99 standard minimum)
- **Build System**: Unix make + Xcode project compatibility
- **Dependencies**: None permitted in engine code
- **Testing**: Python scripts external to engine
- **Platform**: macOS and Linux/Unix support mandatory

### Performance Standards

- Game state evaluation MUST complete within reasonable interactive timeframes
- Memory usage MUST remain bounded (no memory leaks in engine functions)
- Tournament mode MUST handle extended gameplay sessions without degradation

## Quality Gates

### Code Review Requirements

- All changes MUST maintain existing API contracts
- Engine isolation MUST be verified (no new external dependencies)
- Cross-platform compilation MUST be tested
- Existing test suites MUST pass without modification

### Release Criteria

- Successful compilation on both supported platforms
- All functional tests passing
- Tournament mode operational for weight experimentation
- No API breaking changes without explicit versioning

## Governance

This constitution supersedes all other development practices. The engine isolation principle is non-negotiable - any violation requires constitutional amendment. API changes require impact assessment and backward compatibility verification.

All modifications MUST be validated against existing test infrastructure before integration. Weight system changes MUST maintain the goal of enabling dynamic gameplay experimentation.

Complexity additions MUST be justified in terms of gameplay enhancement or weight system flexibility. Use `.github/copilot-instructions.md` for runtime development guidance and architectural context.

**Version**: 1.0.0 | **Ratified**: 2025-09-28 | **Last Amended**: 2025-09-28
