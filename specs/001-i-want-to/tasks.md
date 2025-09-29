# Tasks: Tournament System Enhancement

**Input**: Design documents from `/specs/001-i-want-to/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory ✅
   → Tech stack: Python 3.8+, subprocess communication with tttt executable
   → Structure: Single project with tournament system components
2. Load optional design documents ✅:
   → data-model.md: 5 entities (WeightMatrix, GameResult, MatchupResult, TournamentConfiguration, TournamentReport)
   → contracts/: 2 interface files (GameRunner, TournamentManager)
   → research.md: Engine capabilities and CSV format decisions
3. Generate tasks by category:
   → Setup: project structure, CSV samples
   → Core: data models, engine communication, tournament orchestration
   → Integration: CLI interface, report generation
   → Polish: performance validation, documentation
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Foundation before services
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness ✅:
   → All entities have model implementations
   → All contracts have implementations
   → CLI and reporting covered
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: Files created directly in repository root
- Tournament system components in separate modules
- Configuration and sample files in project root

## Phase 3.1: Setup
- [x] T001 Create project structure: `tournament_system/` directory with `__init__.py`
- [x] T002 [P] Create sample CSV configuration file `sample_tournament_config.csv` with 4 weight matrices
- [x] T003 [P] Create tournament results output directory structure

## Phase 3.2: Core Data Models
- [x] T004 [P] WeightMatrix model in `tournament_system/models/weight_matrix.py`
- [x] T005 [P] GameResult model in `tournament_system/models/game_result.py`
- [x] T006 [P] MatchupResult model in `tournament_system/models/matchup_result.py`
- [x] T007 [P] TournamentConfiguration model in `tournament_system/models/tournament_config.py`
- [x] T008 [P] TournamentReport model in `tournament_system/models/tournament_report.py`
- [x] T009 Create models `__init__.py` to export all model classes

## Phase 3.3: Engine Communication
- [x] T010 GameRunner implementation in `tournament_system/game_runner.py`
- [x] T011 Engine validation and error handling in GameRunner
- [x] T012 Weight matrix formatting for subprocess communication

## Phase 3.4: Tournament Orchestration
- [x] T013 TournamentManager implementation in `tournament_system/tournament_manager.py`
- [x] T014 CSV configuration loading and validation
- [x] T015 Round-robin tournament scheduling logic
- [x] T016 Game execution coordination with GameRunner

## Phase 3.5: Report Generation
- [x] T017 [P] JSON report formatter in `tournament_system/reports/json_formatter.py`
- [x] T018 [P] Text report formatter in `tournament_system/reports/text_formatter.py`
- [x] T019 [P] CSV report formatter in `tournament_system/reports/csv_formatter.py`
- [x] T020 Report generation orchestration in TournamentManager

## Phase 3.6: CLI Interface
- [ ] T021 Main CLI script `tournament_runner.py` in project root
- [ ] T022 Command-line argument parsing and validation
- [ ] T023 Progress reporting and user feedback during tournament execution

## Phase 3.7: Integration & Polish
- [ ] T024 Configuration file validation and error messaging
- [ ] T025 [P] Performance optimization for large tournaments (batch processing)
- [ ] T026 [P] Update `README.md` with tournament system documentation
- [ ] T027 Create comprehensive example in quickstart validation
- [ ] T028 [P] Validate randomization functionality with identical board positions

## Dependencies
- Setup (T001-T003) before all implementation
- Data models (T004-T009) before services (T010-T016)
- T010-T012 (GameRunner) blocks T013-T016 (TournamentManager)
- T013-T016 (TournamentManager) blocks T017-T020 (Report Generation)
- Core implementation (T004-T020) before CLI (T021-T023)
- All implementation before polish (T024-T028)

## Parallel Execution Examples

### Phase 3.2: Data Models (all parallel)
```bash
# Launch T004-T008 together:
Task: "WeightMatrix model in tournament_system/models/weight_matrix.py"
Task: "GameResult model in tournament_system/models/game_result.py"  
Task: "MatchupResult model in tournament_system/models/matchup_result.py"
Task: "TournamentConfiguration model in tournament_system/models/tournament_config.py"
Task: "TournamentReport model in tournament_system/models/tournament_report.py"
```

### Phase 3.5: Report Formatters (all parallel)
```bash
# Launch T017-T019 together:
Task: "JSON report formatter in tournament_system/reports/json_formatter.py"
Task: "Text report formatter in tournament_system/reports/text_formatter.py"
Task: "CSV report formatter in tournament_system/reports/csv_formatter.py"
```

### Phase 3.7: Polish Tasks (selected parallel)
```bash
# Launch T025-T026 together:
Task: "Performance optimization for large tournaments (batch processing)"
Task: "Update README.md with tournament system documentation"
```

## Task Details

### T001: Create project structure
**Files**: `tournament_system/__init__.py`, `tournament_system/models/__init__.py`, `tournament_system/reports/__init__.py`
**Description**: Create Python package structure with proper module organization

### T004: WeightMatrix model
**File**: `tournament_system/models/weight_matrix.py`
**Requirements**: 
- Class with label, weights (25 integers), description attributes
- Validation for unique labels and exact weight count
- Method to format weights for subprocess command

### T010: GameRunner implementation  
**File**: `tournament_system/game_runner.py`
**Requirements**:
- Constructor with engine_path parameter
- play_game() method executing subprocess calls
- validate_engine() method for executable verification
- Error handling for EngineError and TimeoutError

### T013: TournamentManager implementation
**File**: `tournament_system/tournament_manager.py`  
**Requirements**:
- Constructor with config_path and output_dir parameters
- run_tournament() method orchestrating complete tournament
- get_progress() method for execution status
- Integration with GameRunner for individual games

### T021: Main CLI script
**File**: `tournament_runner.py`
**Requirements**:
- Argument parsing for --config, --iterations, --output-dir, --randomization
- Integration with TournamentManager
- Progress display and error handling
- Output format selection (json, csv, text)

### T028: Validate randomization functionality  
**File**: `tournament_system/randomization_validator.py` (or integrate into existing tests)
**Requirements**:
- Create identical board positions with tied evaluation scores
- Verify -r flag produces different move selections across multiple runs
- Validate randomization distribution meets expected patterns
- Document randomization behavior for tournament configuration


## Notes
- [P] tasks = different files, no dependencies
- All subprocess communication uses existing tttt executable flags (-t, -w, -r)
- CSV configuration format: label + 25 weight values per row
- No modifications to TTTTengine/ directory per constitutional requirements
- Focus on performance for 1000+ game tournaments
- Maintain cross-platform compatibility (macOS/Linux)

## Task Generation Rules Applied
- Each data model entity → separate implementation task marked [P]
- Each contract interface → implementation task (sequential due to dependencies)
- Each report format → separate formatter marked [P]  
- CLI components sequential due to shared main script
- Setup tasks before all implementation
- Foundation (models) before services (GameRunner, TournamentManager)
- Core functionality before polish and documentation