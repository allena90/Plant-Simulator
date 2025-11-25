"""
Dimensional Analysis Module.
==============================

This module provides tools for performing dimensional analysis on physical quantities and unit
covnersions.

Authors: Plant Simulation Software Project
Date: November 2025
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import json


@dataclass
class Dimension:
    """
    Represents a physical dimension (e.g., Length, Mass, Time).

    This class encapsulates the properties of a physical dimension, including its name, symbol,
    and base units, as well as methods for dimensional analysis.

    Attributes:
        name (str): The name of the dimension (e.g., "Length").
        symbol (str): The symbol representing the dimension (e.g., "L").
       
        # Unit properties
        base_units (Dict[str, int]): A dictionary mapping base unit names to their exponents
            in this dimension (e.g., {"meter": 1} for Length).
        unit_conversions (Dict[str, float]): A dictionary mapping unit names to their conversion
            factors relative to the base unit.
            
        # Additional metadata
        description (Optional[str]): A brief description of the dimension.
    
    Example:
        >>> length = Dimension(
        ...     name="Length",
        ...     symbol="L",
        ...     base_units={"meter": 1},
        ...     unit_conversions={"kilometer": 1000.0, "centimeter": 0.01},
        ...     description="Dimension representing length."
        ... )
        >>> print(length.name)
        Length
    """

    #Basic identification
    name: str
    symbol: str

    # Unit properties
    base_units: Dict[str, int] = field(default_factory=dict)
    unit_conversions: Dict[str, float] = field(default_factory=dict)

    # Additional properties
    description: str =""

    def __post_init__(self):
        # Validate base_units and unit_conversions
        if not self.base_units:
            raise ValueError("base_units must contain at least one unit.")
        if not self.unit_conversions:
            raise ValueError("unit_conversions must contain at least one conversion factor.")

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one unit to another within this dimension.

        Args:
            value (float): The numerical value to convert.
            from_unit (str): The unit of the input value.
            to_unit (str): The unit to convert the value to

        Returns:
            float: The converted value in the target unit.
        
        Raises:
            ValueError: If either the from_unit or to_unit is not recognized.
            Warning: If conversion between the specified units is not possible.
        """

        if from_unit not in self.unit_conversions:
            raise ValueError(f"Unrecognized from_unit: {from_unit}")
        if to_unit not in self.unit_conversions:
            raise ValueError(f"Unrecognized to_unit: {to_unit}")

        # Convert value to base unit
        base_value = value * self.unit_conversions[from_unit]

        # Convert base unit to target unit
        converted_value = base_value / self.unit_conversions[to_unit]

        return converted_value
    
    def to_dict(self) -> Dict:
        """
        Convert dimension to dictionary for serialization.

        Returns:
            Dict: A dictionary representation of the Dimension instance.
        """
        return {
            "name": self.name,
            "symbol": self.symbol,
            "base_units": self.base_units,
            "unit_conversions": self.unit_conversions,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Dimension":
        """
        Create a Dimension from a dictionary.

        Args:
            data (Dict): Diminension properties as a dictionary.
        Returns:
            Dimension: New dimension instance.
        """
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation of the dimeminsion."""
        return (f"Dimension(name='{self.name}', symbol='{self.symbol}', "
                f"base_units='{self.base_units})")
    def __str__(self) -> str:
        """Humnan-readable string representation"""
        return f"{self.name} ({self.symbol}): {self.description}"
    


# Predefined common dimensions for quick access
def create_length() -> Dimension:
    return Dimension(
        name="Length",
        symbol="L",
        base_units={"meter": 1},
        unit_conversions={"kilometer": 1000.0, "centimeter": 0.01, "meter": 1.0},
        description="Dimension representing length."
    )

@dataclass
class Unit:
    """
    Represents a physical unit associated with a dimension.

    This class encapsulates the properties of a physical unit, including its name, symbol,
    conversion factor to the base unit, and associated dimension.

    Attributes:
        name (str): The name of the unit (e.g., "meter").
        symbol (str): The symbol representing the unit (e.g., "m").
        conversion_factor (float): The factor to convert this unit to the base unit of its
            dimension.
        dimension (Dimension): The dimension this unit belongs to.
        base_unit (bool): Indicates if this unit is the base unit of its dimension.
        base_units (Dict[str, int]): A dictionary mapping base unit names to their exponents
            in this dimension (e.g., {"meter": 1} for Length).

        #Additional metadata
        description (Optional[str]): A brief description of the unit.
        unit_system (Optional[str]): The system of units this unit belongs to (e.g., "SI", "US Customary", "Natur").

    Example:
        >>> meter = Unit(
        ...     name="meter",
        ...     symbol="m",
        ...     conversion_factor=1.0,
        ...     dimension=create_length(),
        ...     base_unit=True,
        ...     base_units={"meter": 1},
        ...     description="Base unit of length in the SI system.",
        ...     unit_system="SI"
        ... )
        >>> print(meter.name)
        meter
    """
    # Basic identification
    name: str
    symbol: str

    # Conversion properties
    conversion_factor: float
    dimension: Dimension
    base_unit: bool = False

    # Additional properties
    description: str = ""
    unit_system: str = "SI"

    def __post_init__(self):
        '''Validate unit data after initialization.'''
        if self.conversion_factor <= 0:
            raise ValueError("conversion_factor must be a positive number.")
        if not isinstance(self.dimension, Dimension):
            raise ValueError("dimension must be an instance of Dimension class.")
        if self.base_unit:
            # Ensure conversion factor is 1 for base units
            self.conversion_factor = 1.0


    @property
    def metric_prefixes(self) -> Dict[str, float]:
        """
        Get common metric prefixes for this unit.

        Returns:
            Dict[str, int]: A dictionary mapping metric prefixes to their factors (power of 10).
        """
        return {
            "quetta": 30,
            "ronna": 27,
            "yotta": 24,
            "zetta": 21,
            "exa": 18,
            "peta": 15,
            "tera": 12,
            "giga": 9,
            "mega": 6,
            "kilo": 3,
            "hecto": 2,
            "deca": 1,
            "deci": -1,
            "centi": -2,
            "milli": -3,
            "micro": -6,
            "nano": -9,
            "pico": -12,
            "femto": -15,
            "atto": -18,
            "zepto": -21,
            "yocto": -24,
            "ronto": -27,
            "quecto": -30,
        }
    
    def convert_to_base(self, value: float) -> float:
        """
        Convert a value from this unit to its base unit.

        Args:
            value (float): The numerical value in this unit.    
        Returns:
            float: The value converted to the base unit
        """
        return value * self.conversion_factor
    

    def get_prefixed_unit(self, unit: str) -> Optional[float]:
        """
        Checks to see if the given unit has a metric prefix and if it does, returns the conversion factor.

        Args:
            unit (str): The unit name with potential metric prefix.

        Returns:
            Optional[float]: The conversion factor if a prefixed unit is found, else 1
        
        """

        for prefix, factor in self.metric_prefixes.items():
            if unit.startswith(prefix) and unit[len(prefix):] == self.name:
                return 10 ** factor
        return 1

    def to_dict(self) -> Dict:
        """
        Convert unit to dictionary for serialization.

        Returns:
            Dict: Unit properties as a dictionary.
        """
        return {
            "name": self.name,
            "symbol": self.symbol,
            "conversion_factor": self.conversion_factor,
            "dimension": self.dimension.to_dict(),
            "base_unit": self.base_unit,
            "description": self.description,
            "unit_system": self.unit_system,
        }    

    @classmethod
    def from_dict(cls, data: Dict) -> "Unit":
        """
        Create a Unit from a dictionary.

        Args:
            data (Dict): Unit properties as a dictionary.
        
        Returns:
            Unit: New unit instance.
        """
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation of the unit."""
        return (f"Unit(name='{self.name}', symbol='{self.symbol}', "
                f"conversion_factor={self.conversion_factor}, "
                f"dimension={self.dimension.name})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name} ({self.symbol}): {self.description}"
    
# Predefined common units for quick access
def create_meter() -> Unit:
    return Unit(
        name="meter",
        symbol="m",
        conversion_factor=1.0,
        dimension=create_length(),
        base_unit=True,
        description="Base unit of length in the SI system.",
        unit_system="SI"
    )   

def create_kilometer() -> Unit:
    return Unit(
        name="kilometer",
        symbol="km",
        conversion_factor=1000.0,
        dimension=create_length(),
        base_unit=False,
        description="Kilometer unit of length in the SI system.",
        unit_system="SI"
    )
