"""
Component Module
================

This module defines the Component class which represents a chemical compound
with its thermodynamic and physical properties.

Author: Plant Simulation Software Project
Date: November 2025
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
import json


@dataclass
class Component:
    """
    Represents a chemical component with its properties.
    
    This class stores all relevant thermodynamic and physical properties
    needed for process simulation calculations.
    
    Attributes:
        name (str): Common name of the component (e.g., "Water", "Methane")
        formula (str): Chemical formula (e.g., "H2O", "CH4")
        cas_number (str): CAS Registry Number for unique identification
        molecular_weight (float): Molecular weight in kg/kmol
        
        # Critical Properties
        critical_temperature (float): Critical temperature in K
        critical_pressure (float): Critical pressure in Pa
        critical_volume (float): Critical molar volume in m³/kmol
        acentric_factor (float): Pitzer acentric factor (dimensionless)
        
        # Normal Properties
        normal_boiling_point (Optional[float]): Normal boiling point in K
        normal_melting_point (Optional[float]): Normal melting point in K
        
        # Ideal Gas Heat Capacity Coefficients (Cp = A + B*T + C*T² + D*T³)
        # Where Cp is in J/(kmol·K) and T is in K
        cp_ideal_gas_a (Optional[float]): Coefficient A
        cp_ideal_gas_b (Optional[float]): Coefficient B
        cp_ideal_gas_c (Optional[float]): Coefficient C
        cp_ideal_gas_d (Optional[float]): Coefficient D
        
        # Antoine Equation for Vapor Pressure (log10(P) = A - B/(T+C))
        # Where P is in Pa and T is in K
        antoine_a (Optional[float]): Antoine coefficient A
        antoine_b (Optional[float]): Antoine coefficient B
        antoine_c (Optional[float]): Antoine coefficient C
        antoine_tmin (Optional[float]): Valid temperature range minimum in K
        antoine_tmax (Optional[float]): Valid temperature range maximum in K
        
        # Heat of Vaporization
        heat_of_vaporization (Optional[float]): Heat of vaporization at Tb in J/kmol
        
        # Additional metadata
        phase_at_stp (str): Phase at STP ('gas', 'liquid', 'solid')
        description (Optional[str]): Additional notes or description
        
    Example:
        >>> water = Component(
        ...     name="Water",
        ...     formula="H2O",
        ...     cas_number="7732-18-5",
        ...     molecular_weight=18.015,
        ...     critical_temperature=647.1,
        ...     critical_pressure=22.064e6,
        ...     acentric_factor=0.345
        ... )
        >>> print(water.name)
        Water
    """
    
    # Basic identification
    name: str
    formula: str
    cas_number: str = ""
    molecular_weight: float = 0.0  # kg/kmol
    
    # Critical properties
    critical_temperature: float = 0.0  # K
    critical_pressure: float = 0.0  # Pa
    critical_volume: float = 0.0  # m³/kmol
    acentric_factor: float = 0.0  # dimensionless
    
    # Normal properties
    normal_boiling_point: Optional[float] = None  # K
    normal_melting_point: Optional[float] = None  # K
    
    # Ideal gas heat capacity coefficients
    cp_ideal_gas_a: Optional[float] = None
    cp_ideal_gas_b: Optional[float] = None
    cp_ideal_gas_c: Optional[float] = None
    cp_ideal_gas_d: Optional[float] = None
    
    # Antoine equation coefficients for vapor pressure
    antoine_a: Optional[float] = None
    antoine_b: Optional[float] = None
    antoine_c: Optional[float] = None
    antoine_tmin: Optional[float] = None
    antoine_tmax: Optional[float] = None
    
    # Heat of vaporization
    heat_of_vaporization: Optional[float] = None  # J/kmol
    
    # Additional properties
    phase_at_stp: str = "unknown"  # 'gas', 'liquid', 'solid', 'unknown'
    description: str = ""
    
    def __post_init__(self):
        """Validate component data after initialization."""
        if not self.name:
            raise ValueError("Component name cannot be empty")
        if not self.formula:
            raise ValueError("Component formula cannot be empty")
        if self.molecular_weight <= 0:
            raise ValueError("Molecular weight must be positive")
    
    def vapor_pressure(self, temperature: float) -> float:
        """
        Calculate vapor pressure using Antoine equation.
        
        Args:
            temperature (float): Temperature in K
            
        Returns:
            float: Vapor pressure in Pa
            
        Raises:
            ValueError: If Antoine coefficients are not defined
            Warning: If temperature is outside valid range
        """
        if None in (self.antoine_a, self.antoine_b, self.antoine_c):
            raise ValueError(f"Antoine coefficients not defined for {self.name}")
        
        # Check temperature range
        if self.antoine_tmin and temperature < self.antoine_tmin:
            print(f"Warning: Temperature {temperature}K below valid range "
                  f"({self.antoine_tmin}K) for {self.name}")
        if self.antoine_tmax and temperature > self.antoine_tmax:
            print(f"Warning: Temperature {temperature}K above valid range "
                  f"({self.antoine_tmax}K) for {self.name}")
        
        # Antoine equation: log10(P) = A - B/(T+C)
        # Result in Pa (assuming Antoine A is adjusted for Pa)
        import math
        log_p = self.antoine_a - self.antoine_b / (temperature + self.antoine_c)
        return 10 ** log_p
    
    def cp_ideal_gas(self, temperature: float) -> float:
        """
        Calculate ideal gas heat capacity at given temperature.
        
        Uses polynomial correlation: Cp = A + B*T + C*T² + D*T³
        
        Args:
            temperature (float): Temperature in K
            
        Returns:
            float: Heat capacity in J/(kmol·K)
            
        Raises:
            ValueError: If heat capacity coefficients are not defined
        """
        if None in (self.cp_ideal_gas_a, self.cp_ideal_gas_b, 
                    self.cp_ideal_gas_c, self.cp_ideal_gas_d):
            raise ValueError(f"Heat capacity coefficients not defined for {self.name}")
        
        cp = (self.cp_ideal_gas_a + 
              self.cp_ideal_gas_b * temperature +
              self.cp_ideal_gas_c * temperature**2 +
              self.cp_ideal_gas_d * temperature**3)
        
        return cp
    
    def reduced_temperature(self, temperature: float) -> float:
        """
        Calculate reduced temperature (T/Tc).
        
        Args:
            temperature (float): Temperature in K
            
        Returns:
            float: Reduced temperature (dimensionless)
        """
        if self.critical_temperature <= 0:
            raise ValueError(f"Critical temperature not defined for {self.name}")
        return temperature / self.critical_temperature
    
    def reduced_pressure(self, pressure: float) -> float:
        """
        Calculate reduced pressure (P/Pc).
        
        Args:
            pressure (float): Pressure in Pa
            
        Returns:
            float: Reduced pressure (dimensionless)
        """
        if self.critical_pressure <= 0:
            raise ValueError(f"Critical pressure not defined for {self.name}")
        return pressure / self.critical_pressure
    
    def to_dict(self) -> Dict:
        """
        Convert component to dictionary for serialization.
        
        Returns:
            Dict: Component properties as dictionary
        """
        return {
            'name': self.name,
            'formula': self.formula,
            'cas_number': self.cas_number,
            'molecular_weight': self.molecular_weight,
            'critical_temperature': self.critical_temperature,
            'critical_pressure': self.critical_pressure,
            'critical_volume': self.critical_volume,
            'acentric_factor': self.acentric_factor,
            'normal_boiling_point': self.normal_boiling_point,
            'normal_melting_point': self.normal_melting_point,
            'cp_ideal_gas_a': self.cp_ideal_gas_a,
            'cp_ideal_gas_b': self.cp_ideal_gas_b,
            'cp_ideal_gas_c': self.cp_ideal_gas_c,
            'cp_ideal_gas_d': self.cp_ideal_gas_d,
            'antoine_a': self.antoine_a,
            'antoine_b': self.antoine_b,
            'antoine_c': self.antoine_c,
            'antoine_tmin': self.antoine_tmin,
            'antoine_tmax': self.antoine_tmax,
            'heat_of_vaporization': self.heat_of_vaporization,
            'phase_at_stp': self.phase_at_stp,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Component':
        """
        Create component from dictionary.
        
        Args:
            data (Dict): Component properties as dictionary
            
        Returns:
            Component: New component instance
        """
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation of component."""
        return (f"Component(name='{self.name}', formula='{self.formula}', "
                f"MW={self.molecular_weight:.3f} kg/kmol)")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name} ({self.formula})"


# Predefined common components for quick access
def create_water() -> Component:
    """Create water component with standard properties."""
    return Component(
        name="Water",
        formula="H2O",
        cas_number="7732-18-5",
        molecular_weight=18.015,
        critical_temperature=647.1,
        critical_pressure=22.064e6,
        critical_volume=0.0559,
        acentric_factor=0.345,
        normal_boiling_point=373.15,
        normal_melting_point=273.15,
        # Ideal gas Cp coefficients (J/kmol·K)
        cp_ideal_gas_a=33363.0,
        cp_ideal_gas_b=26.79,
        cp_ideal_gas_c=0.008687,
        cp_ideal_gas_d=-8.8e-6,
        # Antoine coefficients (for P in Pa, T in K)
        antoine_a=10.196,
        antoine_b=1730.63,
        antoine_c=-39.724,
        antoine_tmin=273.15,
        antoine_tmax=373.15,
        heat_of_vaporization=40660e3,  # J/kmol
        phase_at_stp="liquid",
        description="Water (steam, H2O)"
    )


def create_methane() -> Component:
    """Create methane component with standard properties."""
    return Component(
        name="Methane",
        formula="CH4",
        cas_number="74-82-8",
        molecular_weight=16.043,
        critical_temperature=190.6,
        critical_pressure=4.599e6,
        critical_volume=0.0986,
        acentric_factor=0.011,
        normal_boiling_point=111.65,
        normal_melting_point=90.7,
        # Ideal gas Cp coefficients
        cp_ideal_gas_a=19252.0,
        cp_ideal_gas_b=52.1,
        cp_ideal_gas_c=0.0,
        cp_ideal_gas_d=0.0,
        # Antoine coefficients
        antoine_a=8.968,
        antoine_b=897.84,
        antoine_c=-7.16,
        antoine_tmin=91.0,
        antoine_tmax=190.0,
        heat_of_vaporization=8180e3,
        phase_at_stp="gas",
        description="Methane (natural gas main component)"
    )


if __name__ == "__main__":
    # Example usage
    print("=== Component Module Demo ===\n")
    
    # Create water component
    water = create_water()
    print(water)
    print(f"Molecular Weight: {water.molecular_weight} kg/kmol")
    print(f"Critical Temperature: {water.critical_temperature} K")
    print(f"Critical Pressure: {water.critical_pressure/1e6:.3f} MPa")
    
    # Calculate vapor pressure at 100°C
    temp = 373.15  # K
    p_sat = water.vapor_pressure(temp)
    print(f"\nVapor pressure at {temp}K: {p_sat/1e5:.3f} bar")
    
    # Calculate heat capacity
    cp = water.cp_ideal_gas(temp)
    print(f"Ideal gas Cp at {temp}K: {cp:.1f} J/(kmol·K)")
    
    print("\n" + "="*50 + "\n")
    
    # Create methane component
    methane = create_methane()
    print(methane)
    print(f"Phase at STP: {methane.phase_at_stp}")
