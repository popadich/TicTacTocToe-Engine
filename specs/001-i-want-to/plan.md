
# Implementation Plan: Tournament System Enhancement

**Branch**: `001-i-want-to` | **Date**: 2025-09-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-i-want-to/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Enhanced tournament system for the 3D tic-tac-toe engine that allows automated testing of different heuristic weight matrices against each other. The system uses a CSV configuration file to define labeled weight matrices and generates comprehensive statistical reports on game outcomes. Technical approach builds upon existing tournament.py script using Python with subprocess communication to the C engine executable.

## Technical Context
**Language/Version**: Python 3.8+  
**Primary Dependencies**: Standard library (subprocess, csv, json), existing tttt executable  
**Storage**: CSV configuration files, JSON/text report outputs, no database required  
**Target Platform**: macOS and Linux/Unix (matching existing engine compatibility)
**Project Type**: single - extension to existing game engine project  
**Performance Goals**: Handle tournaments with 10+ weight matrices, 1000+ games per session  
**Constraints**: No modifications to TTTTengine/ directory, must use subprocess communication only  
**Scale/Scope**: Support 5-20 weight matrices, generate reports for up to 10K game results

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Pre-Research)
- **Engine Isolation**: ✅ No external dependencies introduced to TTTTengine/ directory - Python scripts run externally
- **API Stability**: ✅ Existing TTTT API functions unchanged, using existing tournament mode (-t) and weight flags (-w)
- **Weight System**: ✅ Enhances heuristic weight flexibility through systematic tournament testing
- **Cross-Platform**: ✅ Python scripts compatible with both macOS and Linux/Unix platforms

### Post-Design Re-Check
- **Engine Isolation**: ✅ CONFIRMED - All components (TournamentManager, GameRunner) use subprocess communication only
- **API Stability**: ✅ CONFIRMED - Design uses existing -t, -w, -r flags without modification
- **Weight System**: ✅ CONFIRMED - CSV configuration and statistical analysis enhance weight experimentation
- **Cross-Platform**: ✅ CONFIRMED - Python standard library dependencies ensure cross-platform compatibility

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
tournament_system/ 
├── init.py 
├── models/ 
│ ├── init.py 
│ ├── weight_matrix.py 
│ ├── game_result.py 
│ ├── matchup_result.py 
│ ├── tournament_config.py 
│ └── tournament_report.py 
├── reports/ 
│ ├── init.py 
│ ├── json_formatter.py 
│ ├── text_formatter.py 
│ └── csv_formatter.py 
├── game_runner.py 
├── tournament_manager.py 
└── randomization_validator.py
tournament_runner.py
sample_tournament_config.csv


**Structure Decision**: Single project structure with tournament_system package containing all Python components, maintaining separation from TTTTengine/ directory per constitutional requirements.


## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → define interface
   - Use standard patterns for method signatures
   - Output interface definitions to `/contracts/`

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh copilot`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Component Breakdown**:
- Load `.specify/templates/tasks-template.md` as base
- Apply research decisions to task generation approach
- From data-model.md:
  - WeightMatrix class implementation task
  - GameResult class implementation task [P]
  - TournamentConfiguration loader task
  - TournamentReport generator task
- From contracts/:
  - TournamentManager implementation tasks
  - GameRunner implementation tasks [P]
  - Engine communication protocol implementation
- From quickstart.md:  
  - CSV configuration file creation task
  - Command-line interface setup task
  - Sample weight matrices creation task
  - Integration with existing tournament.py

**Ordering Strategy**:
- Foundation first: Data models before service classes
- Engine integration: GameRunner before TournamentManager
- Mark [P] for parallel execution on independent components

**Estimated Output**: 15-20 numbered, ordered tasks focusing on Python components only

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command) - research.md created
- [x] Phase 1: Design complete (/plan command) - data-model.md, contracts/, quickstart.md created
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS - No engine modifications, external Python tools only
- [x] Post-Design Constitution Check: PASS - All constitutional requirements maintained
- [x] All NEEDS CLARIFICATION resolved - CSV format clarified during specification
- [x] Complexity deviations documented - No violations detected

---
*Based on Constitution v1.0.0 - See `/memory/constitution.md`*
