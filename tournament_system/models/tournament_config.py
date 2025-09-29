"""
TournamentConfiguration model for tournament system.

Contains complete tournament setup including all weight matrices and parameters.
"""

import csv
from typing import List, Dict
from .weight_matrix import WeightMatrix


class TournamentConfiguration:
    """
    Complete tournament setup including all weight matrices and parameters.
    
    Manages loading from CSV files and validation of tournament parameters.
    """
    
    VALID_OUTPUT_FORMATS = {"json", "csv", "text"}
    
    def __init__(self, 
                 matrices: List[WeightMatrix],
                 iterations_per_matchup: int = 100,
                 randomization_enabled: bool = False,
                 output_formats: List[str] = None,
                 config_file_path: str = None):
        """
        Initialize tournament configuration.
        
        Args:
            matrices: List of WeightMatrix objects for tournament
            iterations_per_matchup: Number of games per matrix pair (default: 100)
            randomization_enabled: Enable engine randomization flag (default: False)
            output_formats: List of output format strings (default: ["json", "csv", "text"])
            config_file_path: Path to source CSV file (optional)
            
        Raises:
            ValueError: If invalid parameters provided
        """
        if len(matrices) < 2:
            raise ValueError("Tournament requires at least 2 weight matrices")
            
        if iterations_per_matchup <= 0:
            raise ValueError("Iterations per matchup must be positive")
            
        # Comprehensive validation
        self._validate_matrices(matrices)
        self._validate_iterations(iterations_per_matchup)
        self._validate_output_formats(output_formats or ["json", "csv", "text"])
            
        # Validate output formats
        if output_formats is None:
            output_formats = ["json", "csv", "text"]
        invalid_formats = set(output_formats) - self.VALID_OUTPUT_FORMATS
        if invalid_formats:
            raise ValueError(f"Invalid output formats: {invalid_formats}")
            
        self.matrices = matrices
        self.iterations_per_matchup = iterations_per_matchup
        self.randomization_enabled = randomization_enabled
        self.output_formats = output_formats
        self.config_file_path = config_file_path
        
    def _validate_matrices(self, matrices: List[WeightMatrix]) -> None:
        """Validate matrix list and detect common issues."""
        if not matrices:
            raise ValueError("No weight matrices provided")
            
        if len(matrices) < 2:
            raise ValueError(f"Tournament requires at least 2 matrices, got {len(matrices)}")
            
        if len(matrices) > 50:
            raise ValueError(f"Too many matrices ({len(matrices)}), maximum recommended is 50")
            
        # Check for duplicate labels
        labels = [m.label for m in matrices]
        label_counts = {}
        for label in labels:
            label_counts[label] = label_counts.get(label, 0) + 1
            
        duplicates = [label for label, count in label_counts.items() if count > 1]
        if duplicates:
            raise ValueError(f"Duplicate matrix labels found: {duplicates}. Each matrix must have a unique label.")
            
        # Check for empty or invalid labels
        invalid_labels = [m.label for m in matrices if not m.label or not m.label.strip()]
        if invalid_labels:
            raise ValueError(f"Empty or whitespace-only labels found: {invalid_labels}")
            
        # Check for problematic label characters
        problematic_labels = []
        for m in matrices:
            if any(char in m.label for char in [',', '"', '\n', '\r']):
                problematic_labels.append(m.label)
        if problematic_labels:
            raise ValueError(f"Labels contain problematic characters (comma, quote, newline): {problematic_labels}")
            
    def _validate_iterations(self, iterations: int) -> None:
        """Validate iterations per matchup parameter."""
        if not isinstance(iterations, int):
            raise ValueError(f"Iterations must be an integer, got {type(iterations).__name__}: {iterations}")
            
        if iterations <= 0:
            raise ValueError(f"Iterations per matchup must be positive, got: {iterations}")
            
        if iterations > 10000:
            raise ValueError(f"Iterations per matchup too large ({iterations}), maximum recommended is 10000")
            
    def _validate_output_formats(self, formats: List[str]) -> None:
        """Validate output format list."""
        if not formats:
            raise ValueError("At least one output format must be specified")
            
        invalid_formats = [fmt for fmt in formats if fmt not in self.VALID_OUTPUT_FORMATS]
        if invalid_formats:
            valid_list = ", ".join(sorted(self.VALID_OUTPUT_FORMATS))
            raise ValueError(f"Invalid output formats: {invalid_formats}. Valid formats: {valid_list}")
            
        # Check for duplicates
        if len(set(formats)) != len(formats):
            duplicates = [fmt for fmt in formats if formats.count(fmt) > 1]
            raise ValueError(f"Duplicate output formats: {duplicates}")
        
    def get_matrix_by_label(self, label: str) -> WeightMatrix:
        """
        Get matrix by label.
        
        Args:
            label: Matrix label to find
            
        Returns:
            WeightMatrix with matching label
            
        Raises:
            ValueError: If label not found
        """
        for matrix in self.matrices:
            if matrix.label == label:
                return matrix
        raise ValueError(f"Matrix with label '{label}' not found")
        
    def get_all_matchups(self) -> List[tuple]:
        """
        Generate all unique matrix pairs for round-robin tournament.
        
        Returns:
            List of (matrix1, matrix2) tuples for all matchups
        """
        matchups = []
        for i in range(len(self.matrices)):
            for j in range(i + 1, len(self.matrices)):
                matchups.append((self.matrices[i], self.matrices[j]))
        return matchups
        
    @property
    def total_games_count(self) -> int:
        """Calculate total number of games in tournament."""
        matchups = len(self.get_all_matchups())
        # Each matchup plays with both matrices as first/second player
        return matchups * 2 * self.iterations_per_matchup
        
    @property
    def matrix_labels(self) -> List[str]:
        """Get list of all matrix labels."""
        return [m.label for m in self.matrices]
        
    @classmethod
    def from_csv_file(cls, 
                      config_path: str,
                      iterations_per_matchup: int = 100,
                      randomization_enabled: bool = False,
                      output_formats: List[str] = None) -> "TournamentConfiguration":
        """
        Load tournament configuration from CSV file.
        
        Expected CSV format:
        - Header: label,w0_0,w0_1,...,w4_4 (26 columns total)
        - Data rows: matrix_label,weight1,weight2,...,weight25
        
        Args:
            config_path: Path to CSV configuration file
            iterations_per_matchup: Games per matchup (default: 100)
            randomization_enabled: Enable randomization (default: False)
            output_formats: Output formats (default: ["json", "csv", "text"])
            
        Returns:
            TournamentConfiguration instance
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        matrices = []
        
        # Validate file exists and is readable
        try:
            with open(config_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                try:
                    # Read and validate header
                    header = next(reader)
                except StopIteration:
                    raise ValueError("CSV file is empty")
                
                expected_columns = 26  # label + 25 weights
                if len(header) != expected_columns:
                    raise ValueError(f"Invalid CSV header: expected {expected_columns} columns (label + 25 weights), got {len(header)}. "
                                   f"Header: {header[:5]}...")
                    
                if header[0].lower() != 'label':
                    raise ValueError(f"First column must be 'label', got '{header[0]}'")
                    
                # Validate weight column headers (optional but helpful)
                weight_headers = header[1:]
                non_numeric_headers = [h for h in weight_headers if h and not h.replace('w', '').replace('_', '').replace('.', '').isdigit()]
                if len(non_numeric_headers) > 5:  # Allow some flexibility
                    raise ValueError(f"Weight column headers should be numeric (e.g., 'w00', 'w01'), found many non-numeric: {non_numeric_headers[:3]}...")
                
                # Track labels for duplicate detection
                seen_labels = set()
                
                # Read data rows
                for row_num, row in enumerate(reader, start=2):
                    if not row or all(cell.strip() == '' for cell in row):
                        continue  # Skip empty rows
                        
                    if len(row) != expected_columns:
                        raise ValueError(f"Row {row_num}: Expected {expected_columns} columns, got {len(row)}. "
                                       f"Data: {row[:3]}...")
                        
                    label = row[0].strip()
                    if not label:
                        raise ValueError(f"Row {row_num}: Empty or whitespace-only label")
                        
                    # Check for duplicate labels during parsing
                    if label in seen_labels:
                        raise ValueError(f"Row {row_num}: Duplicate label '{label}' found")
                    seen_labels.add(label)
                    
                    # Validate label characters
                    if any(char in label for char in [',', '"', '\n', '\r']):
                        raise ValueError(f"Row {row_num}: Label '{label}' contains invalid characters (comma, quote, newline)")
                        
                    weight_values = row[1:]
                    
                    # Check for empty weights
                    empty_weights = [i for i, w in enumerate(weight_values) if not w.strip()]
                    if empty_weights:
                        raise ValueError(f"Row {row_num}: Empty weight values at positions: {empty_weights}")
                    
                    try:
                        matrix = WeightMatrix.from_csv_row(label, weight_values)
                        matrices.append(matrix)
                    except ValueError as e:
                        raise ValueError(f"Row {row_num} (label: '{label}'): {e}")
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: '{config_path}'. Please check the file path and permissions.")
        except PermissionError:
            raise PermissionError(f"Permission denied reading file: '{config_path}'. Please check file permissions.")
        except UnicodeDecodeError as e:
            raise ValueError(f"File encoding error: {e}. Please save CSV file with UTF-8 encoding.")
        except csv.Error as e:
            raise ValueError(f"CSV parsing error: {e}. Please check CSV format and special characters.")
            
        if not matrices:
            raise ValueError("No valid matrices found in CSV file")
            
        return cls(matrices, iterations_per_matchup, randomization_enabled, 
                  output_formats, config_path)
        
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "matrices": [m.to_dict() for m in self.matrices],
            "iterations_per_matchup": self.iterations_per_matchup,
            "randomization_enabled": self.randomization_enabled,
            "output_formats": self.output_formats,
            "config_file_path": self.config_file_path,
            "total_games_count": self.total_games_count,
            "matrix_count": len(self.matrices)
        }
        
    def __str__(self) -> str:
        """String representation."""
        return (f"TournamentConfig({len(self.matrices)} matrices, "
                f"{self.iterations_per_matchup} iterations, "
                f"{self.total_games_count} total games)")
                
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"TournamentConfiguration(matrices={len(self.matrices)}, "
                f"iterations={self.iterations_per_matchup}, "
                f"randomization={self.randomization_enabled}, "
                f"formats={self.output_formats})")