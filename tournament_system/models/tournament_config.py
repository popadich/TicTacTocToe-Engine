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
            
        # Validate unique matrix labels
        labels = [m.label for m in matrices]
        if len(set(labels)) != len(labels):
            duplicates = [label for label in labels if labels.count(label) > 1]
            raise ValueError(f"Duplicate matrix labels found: {duplicates}")
            
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
        
        try:
            with open(config_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                
                # Read and validate header
                header = next(reader)
                expected_columns = 26  # label + 25 weights
                if len(header) != expected_columns:
                    raise ValueError(f"CSV must have {expected_columns} columns, got {len(header)}")
                    
                if header[0].lower() != 'label':
                    raise ValueError("First column must be 'label'")
                    
                # Read data rows
                for row_num, row in enumerate(reader, start=2):
                    if len(row) != expected_columns:
                        raise ValueError(f"Row {row_num}: Expected {expected_columns} columns, got {len(row)}")
                        
                    label = row[0].strip()
                    if not label:
                        raise ValueError(f"Row {row_num}: Empty label")
                        
                    weight_values = row[1:]
                    
                    try:
                        matrix = WeightMatrix.from_csv_row(label, weight_values)
                        matrices.append(matrix)
                    except ValueError as e:
                        raise ValueError(f"Row {row_num}: {e}")
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except csv.Error as e:
            raise ValueError(f"CSV parsing error: {e}")
            
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