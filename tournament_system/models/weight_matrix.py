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
            ValueError: If label contains invalid characters
        """
        # Validate label
        self._validate_label(label)
        
        # Validate weights
        self._validate_weights(weights)
            
        self.label = label.strip()
        self.weights = weights.copy()
        self.description = description.strip() if description else None
        
    def _validate_label(self, label: str) -> None:
        """Validate label format and content."""
        if not isinstance(label, str):
            raise ValueError(f"Label must be a string, got {type(label).__name__}: {label}")
            
        if not label or not label.strip():
            raise ValueError("Label cannot be empty or whitespace-only")
            
        label = label.strip()
        
        # Check for problematic characters
        invalid_chars = [',', '"', '\n', '\r', '\t']
        found_chars = [char for char in invalid_chars if char in label]
        if found_chars:
            char_names = {'\\n': 'newline', '\\r': 'carriage return', '\\t': 'tab', ',': 'comma', '"': 'quote'}
            found_names = [char_names.get(char, f"'{char}'") for char in found_chars]
            raise ValueError(f"Label contains invalid characters: {', '.join(found_names)}. "
                           f"Label: '{label}'")
        
        # Check length
        if len(label) > 50:
            raise ValueError(f"Label too long ({len(label)} chars), maximum 50 characters: '{label[:20]}...'")
            
        # Check for reasonable content
        if label.isspace():
            raise ValueError("Label cannot contain only whitespace characters")
            
    def _validate_weights(self, weights: List) -> None:
        """Validate weight list format and values."""
        if not isinstance(weights, (list, tuple)):
            raise ValueError(f"Weights must be a list or tuple, got {type(weights).__name__}")
            
        if len(weights) != 25:
            raise ValueError(f"Weights must contain exactly 25 values (5x5 matrix), got {len(weights)}. "
                           f"Expected: 25, Received: {len(weights)}")
        
        # Check types and ranges
        non_numeric = []
        out_of_range = []
        
        for i, weight in enumerate(weights):
            if not isinstance(weight, (int, float)):
                non_numeric.append(f"position {i}: {type(weight).__name__} '{weight}'")
            else:
                # Convert float to int if it's a whole number
                if isinstance(weight, float):
                    if weight.is_integer():
                        weights[i] = int(weight)
                    else:
                        raise ValueError(f"Weight at position {i} is not an integer: {weight}")
                        
                # Check reasonable range
                if not -1000 <= weight <= 1000:
                    out_of_range.append(f"position {i}: {weight}")
        
        if non_numeric:
            raise ValueError(f"All weights must be numeric. Non-numeric values found at: {', '.join(non_numeric[:3])}"
                           + ("..." if len(non_numeric) > 3 else ""))
                           
        if out_of_range:
            raise ValueError(f"Weights should be in range [-1000, 1000]. Out of range values: {', '.join(out_of_range[:3])}"
                           + ("..." if len(out_of_range) > 3 else ""))
        
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
        if len(weight_values) != 25:
            raise ValueError(f"Expected 25 weight values, got {len(weight_values)}")
        
        weights = []
        conversion_errors = []
        
        for i, weight_str in enumerate(weight_values):
            weight_str = weight_str.strip()
            
            if not weight_str:
                conversion_errors.append(f"position {i}: empty value")
                continue
                
            try:
                # Try to convert to float first, then to int if it's a whole number
                weight_float = float(weight_str)
                if weight_float.is_integer():
                    weights.append(int(weight_float))
                else:
                    # Allow floats but warn about precision loss
                    weights.append(int(round(weight_float)))
            except ValueError:
                conversion_errors.append(f"position {i}: '{weight_str}' is not a valid number")
        
        if conversion_errors:
            error_summary = ', '.join(conversion_errors[:3])
            if len(conversion_errors) > 3:
                error_summary += f" (and {len(conversion_errors) - 3} more)"
            raise ValueError(f"Weight conversion errors: {error_summary}")
            
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