"""
WeightMatrix model for tournament system.

Represents a labeled heuristic weight configuration for the game engine.
"""

from typing import List, Optional


class WeightMatrix:
    """
    Represents a labeled heuristic weight configuration for the game engine.
    
    The weight matrix is a 5x5 configuration where:
    - Rows represent human piece count (0-4) in a winning path
    - Columns represent machine piece count (0-4) in the same path
    - Values are scoring weights (negative favors machine, positive favors human)
    """
    
    def __init__(self, label: str, weights: List[int], description: Optional[str] = None):
        """
        Initialize weight matrix.
        
        Args:
            label: Unique identifier for this weight configuration
            weights: List of 25 integers representing flattened 5x5 matrix
            description: Optional human-readable description
            
        Raises:
            ValueError: If weights list is not exactly 25 integers
            ValueError: If label contains commas (CSV incompatible)
        """
        if len(weights) != 25:
            raise ValueError(f"Weights must contain exactly 25 values, got {len(weights)}")
        
        if not all(isinstance(w, int) for w in weights):
            raise ValueError("All weights must be integers")
            
        if "," in label:
            raise ValueError("Label cannot contain commas (CSV compatibility)")
            
        if not label.strip():
            raise ValueError("Label cannot be empty")
            
        self.label = label.strip()
        self.weights = weights.copy()
        self.description = description.strip() if description else None
        
    def to_command_string(self) -> str:
        """
        Format weights for subprocess command line.
        
        Returns:
            Space-separated string of 25 weight values
        """
        return " ".join(str(w) for w in self.weights)
        
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "label": self.label,
            "weights": self.weights,
            "description": self.description
        }
        
    @classmethod
    def from_csv_row(cls, label: str, weight_values: List[str]) -> "WeightMatrix":
        """
        Create WeightMatrix from CSV row data.
        
        Args:
            label: Matrix label from CSV
            weight_values: List of 25 weight strings from CSV
            
        Returns:
            WeightMatrix instance
            
        Raises:
            ValueError: If weight conversion fails or count is wrong
        """
        try:
            weights = [int(w.strip()) for w in weight_values]
        except ValueError as e:
            raise ValueError(f"Invalid weight value in CSV: {e}")
            
        return cls(label, weights)
        
    def __str__(self) -> str:
        """String representation."""
        desc = f" - {self.description}" if self.description else ""
        return f"WeightMatrix('{self.label}'{desc})"
        
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"WeightMatrix(label='{self.label}', weights={self.weights}, description='{self.description}')"
        
    def __eq__(self, other) -> bool:
        """Equality comparison based on label."""
        if not isinstance(other, WeightMatrix):
            return False
        return self.label == other.label