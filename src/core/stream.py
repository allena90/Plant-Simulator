"""
Stream Module
=============

This module defines the Stream class which represents material flows
between unit operations in a process flowsheet.

Author: Plant Simulation Software Project
Date: November 2025
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
from src.core.component import Component


@dataclass
class Stream:
    """
    Represents a process stream with temperature, pressure, composition, and flow rate.
    
    A stream contains a mixture of components flowing at specified conditions.
    It handles mass and energy balances, phase calculations, and property calculations.
    
    Attributes:
        name (str): Stream identifier
        temperature (float): Temperature in K
        pressure (float): Pressure in Pa
        components (Dict[str, Component]): Dictionary of components by name
        mole_fractions (Dict[str, float]): Mole fractions of each component (sum = 1.0)
        molar_flow (float): Total molar flow rate in kmol/s
        phase (str): Phase state ('vapor', 'liquid', 'mixed', 'unknown')
        
    Example:
        >>> from src.core.component import create_water, create_methane
        >>> water = create_water()
        >>> methane = create_methane()
        >>> 
        >>> stream = Stream(
        ...     name="Feed",
        ...     temperature=298.15,
        ...     pressure=101325,
        ...     components={'Water': water, 'Methane': methane},
        ...     mole_fractions={'Water': 0.5, 'Methane': 0.5},
        ...     molar_flow=100.0
        ... )
        >>> print(stream.mass_flow())
        1701.45 kg/s
    """
    
    name: str
    temperature: float  # K
    pressure: float  # Pa
    components: Dict[str, Component] = field(default_factory=dict)
    mole_fractions: Dict[str, float] = field(default_factory=dict)
    molar_flow: float = 0.0  # kmol/s
    phase: str = "unknown"  # 'vapor', 'liquid', 'mixed', 'unknown'
    
    def __post_init__(self):
        """Validate stream data after initialization."""
        if not self.name:
            raise ValueError("Stream name cannot be empty")
        if self.temperature <= 0:
            raise ValueError("Temperature must be positive (in Kelvin)")
        if self.pressure <= 0:
            raise ValueError("Pressure must be positive")
        if self.molar_flow < 0:
            raise ValueError("Molar flow cannot be negative")
        
        # Validate mole fractions
        if self.mole_fractions:
            total = sum(self.mole_fractions.values())
            if abs(total - 1.0) > 1e-6 and total > 0:
                raise ValueError(f"Mole fractions must sum to 1.0, got {total}")
            
            # Check that all components in mole_fractions exist in components dict
            for comp_name in self.mole_fractions.keys():
                if comp_name not in self.components:
                    raise ValueError(f"Component '{comp_name}' in mole_fractions not found in components dict")
    
    def molecular_weight(self) -> float:
        """
        Calculate average molecular weight of the mixture.
        
        MW_avg = Σ(xi * MWi)
        
        Returns:
            float: Average molecular weight in kg/kmol
        """
        if not self.mole_fractions or not self.components:
            return 0.0
        
        mw = sum(self.mole_fractions[name] * comp.molecular_weight 
                 for name, comp in self.components.items()
                 if name in self.mole_fractions)
        return mw
    
    def mass_flow(self) -> float:
        """
        Calculate total mass flow rate.
        
        m_dot = n_dot * MW_avg
        
        Returns:
            float: Mass flow rate in kg/s
        """
        return self.molar_flow * self.molecular_weight()
    
    def component_molar_flows(self) -> Dict[str, float]:
        """
        Calculate individual component molar flow rates.
        
        Returns:
            Dict[str, float]: Molar flow rates in kmol/s for each component
        """
        return {name: self.molar_flow * self.mole_fractions.get(name, 0.0)
                for name in self.components.keys()}
    
    def component_mass_flows(self) -> Dict[str, float]:
        """
        Calculate individual component mass flow rates.
        
        Returns:
            Dict[str, float]: Mass flow rates in kg/s for each component
        """
        comp_flows = self.component_molar_flows()
        return {name: comp_flows[name] * self.components[name].molecular_weight
                for name in self.components.keys()}
    
    def mass_fractions(self) -> Dict[str, float]:
        """
        Calculate mass fractions from mole fractions.
        
        wi = (xi * MWi) / MW_avg
        
        Returns:
            Dict[str, float]: Mass fractions for each component
        """
        if not self.mole_fractions or not self.components:
            return {}
        
        mw_avg = self.molecular_weight()
        if mw_avg == 0:
            return {}
        
        return {name: (self.mole_fractions[name] * self.components[name].molecular_weight) / mw_avg
                for name in self.components.keys()
                if name in self.mole_fractions}
    
    def volumetric_flow(self, density: float) -> float:
        """
        Calculate volumetric flow rate.
        
        Q = m_dot / ρ
        
        Args:
            density (float): Density in kg/m³
            
        Returns:
            float: Volumetric flow rate in m³/s
        """
        if density <= 0:
            raise ValueError("Density must be positive")
        return self.mass_flow() / density
    
    def ideal_gas_density(self) -> float:
        """
        Calculate density assuming ideal gas behavior.
        
        ρ = P * MW / (R * T)
        
        Returns:
            float: Density in kg/m³
        """
        R = 8314.46  # J/(kmol·K)
        return (self.pressure * self.molecular_weight()) / (R * self.temperature)
    
    def molar_volume_ideal_gas(self) -> float:
        """
        Calculate molar volume assuming ideal gas.
        
        V_m = R * T / P
        
        Returns:
            float: Molar volume in m³/kmol
        """
        R = 8314.46  # J/(kmol·K)
        return (R * self.temperature) / self.pressure
    
    def enthalpy_ideal_gas(self, reference_temp: float = 298.15) -> float:
        """
        Calculate enthalpy assuming ideal gas behavior.
        
        Uses constant Cp approximation: H = Cp * (T - T_ref)
        This is simplified - real implementation would integrate Cp(T)
        
        Args:
            reference_temp (float): Reference temperature in K (default 298.15K)
            
        Returns:
            float: Specific enthalpy in J/kg
        """
        # Simplified: use Cp at average temperature
        T_avg = (self.temperature + reference_temp) / 2
        
        # Calculate mixture Cp (molar basis)
        cp_mix = 0.0
        for name, comp in self.components.items():
            if name in self.mole_fractions:
                try:
                    cp_comp = comp.cp_ideal_gas(T_avg)
                    cp_mix += self.mole_fractions[name] * cp_comp
                except ValueError:
                    # Component doesn't have Cp data
                    continue
        
        # Convert to mass basis
        mw = self.molecular_weight()
        if mw == 0:
            return 0.0
        
        cp_mass = cp_mix / mw  # J/(kg·K)
        h = cp_mass * (self.temperature - reference_temp)
        
        return h
    
    def copy(self) -> 'Stream':
        """
        Create a deep copy of the stream.
        
        Returns:
            Stream: New stream instance with same properties
        """
        return Stream(
            name=self.name + "_copy",
            temperature=self.temperature,
            pressure=self.pressure,
            components=self.components.copy(),
            mole_fractions=self.mole_fractions.copy(),
            molar_flow=self.molar_flow,
            phase=self.phase
        )
    
    def mix_with(self, other: 'Stream') -> 'Stream':
        """
        Mix this stream with another stream (adiabatic mixing at lower pressure).
        
        Conservation laws:
        - Mass: n_out = n_1 + n_2
        - Component: n_i,out = n_i,1 + n_i,2
        - Energy: H_out = H_1 + H_2 (adiabatic)
        
        Pressure: Takes minimum of the two pressures
        
        Args:
            other (Stream): Stream to mix with
            
        Returns:
            Stream: New mixed stream
        """
        if not self.components or not other.components:
            raise ValueError("Cannot mix streams with no components")
        
        # Combine components
        all_components = {}
        all_components.update(self.components)
        all_components.update(other.components)
        
        # Calculate output molar flow
        n_out = self.molar_flow + other.molar_flow
        
        if n_out == 0:
            raise ValueError("Cannot mix streams with zero total flow")
        
        # Calculate output composition
        comp_flows_1 = self.component_molar_flows()
        comp_flows_2 = other.component_molar_flows()
        
        comp_flows_out = {}
        for name in all_components.keys():
            flow_1 = comp_flows_1.get(name, 0.0)
            flow_2 = comp_flows_2.get(name, 0.0)
            comp_flows_out[name] = flow_1 + flow_2
        
        # Convert to mole fractions
        mole_fractions_out = {name: flow / n_out 
                              for name, flow in comp_flows_out.items()}
        
        # Output pressure is minimum (pressure drop)
        p_out = min(self.pressure, other.pressure)
        
        # For adiabatic mixing, solve energy balance for outlet temperature
        # Simplified: mass-weighted average (assumes similar Cp)
        # More rigorous would solve: H_out = H_1 + H_2
        m1 = self.mass_flow()
        m2 = other.mass_flow()
        m_total = m1 + m2
        
        if m_total > 0:
            T_out = (m1 * self.temperature + m2 * other.temperature) / m_total
        else:
            T_out = (self.temperature + other.temperature) / 2
        
        return Stream(
            name=f"{self.name}+{other.name}",
            temperature=T_out,
            pressure=p_out,
            components=all_components,
            mole_fractions=mole_fractions_out,
            molar_flow=n_out,
            phase="mixed"
        )
    
    def split(self, fraction: float, name_suffix: str = "_split") -> 'Stream':
        """
        Split stream into two streams with same composition.
        
        Args:
            fraction (float): Fraction going to output stream (0 to 1)
            name_suffix (str): Suffix to add to stream name
            
        Returns:
            Stream: New stream with flow = fraction * original flow
        """
        if not 0 <= fraction <= 1:
            raise ValueError("Split fraction must be between 0 and 1")
        
        return Stream(
            name=self.name + name_suffix,
            temperature=self.temperature,
            pressure=self.pressure,
            components=self.components.copy(),
            mole_fractions=self.mole_fractions.copy(),
            molar_flow=self.molar_flow * fraction,
            phase=self.phase
        )
    
    def __repr__(self) -> str:
        """String representation of stream."""
        return (f"Stream(name='{self.name}', T={self.temperature:.2f}K, "
                f"P={self.pressure/1e5:.2f}bar, n={self.molar_flow:.2f}kmol/s)")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Stream '{self.name}': {self.temperature:.1f}K, {self.pressure/1e5:.2f}bar, {self.molar_flow:.2f}kmol/s"
    
    def summary(self) -> str:
        """
        Generate detailed summary of stream properties.
        
        Returns:
            str: Multi-line summary of stream
        """
        lines = [
            f"Stream: {self.name}",
            f"{'='*50}",
            f"Temperature: {self.temperature:.2f} K ({self.temperature-273.15:.2f} °C)",
            f"Pressure: {self.pressure/1e5:.4f} bar ({self.pressure/1e6:.4f} MPa)",
            f"Phase: {self.phase}",
            f"",
            f"Flow Rates:",
            f"  Molar flow: {self.molar_flow:.4f} kmol/s ({self.molar_flow*3600:.2f} kmol/h)",
            f"  Mass flow: {self.mass_flow():.4f} kg/s ({self.mass_flow()*3600:.2f} kg/h)",
            f"  Molecular weight: {self.molecular_weight():.4f} kg/kmol",
            f"",
            f"Composition (Mole Basis):",
        ]
        
        for name in sorted(self.components.keys()):
            if name in self.mole_fractions:
                x = self.mole_fractions[name]
                comp_flow = self.molar_flow * x
                lines.append(f"  {name:20s}: {x:8.4f} ({comp_flow:10.4f} kmol/s)")
        
        lines.append("")
        lines.append("Composition (Mass Basis):")
        mass_fracs = self.mass_fractions()
        for name in sorted(self.components.keys()):
            if name in mass_fracs:
                w = mass_fracs[name]
                comp_mass_flow = self.mass_flow() * w
                lines.append(f"  {name:20s}: {w:8.4f} ({comp_mass_flow:10.4f} kg/s)")
        
        return "\n".join(lines)


# Utility functions for unit conversions
class UnitConversion:
    """Unit conversion utilities for common process engineering units."""
    
    @staticmethod
    def celsius_to_kelvin(temp_c: float) -> float:
        """Convert Celsius to Kelvin."""
        return temp_c + 273.15
    
    @staticmethod
    def kelvin_to_celsius(temp_k: float) -> float:
        """Convert Kelvin to Celsius."""
        return temp_k - 273.15
    
    @staticmethod
    def fahrenheit_to_kelvin(temp_f: float) -> float:
        """Convert Fahrenheit to Kelvin."""
        return (temp_f - 32) * 5/9 + 273.15
    
    @staticmethod
    def kelvin_to_fahrenheit(temp_k: float) -> float:
        """Convert Kelvin to Fahrenheit."""
        return (temp_k - 273.15) * 9/5 + 32
    
    @staticmethod
    def bar_to_pascal(pressure_bar: float) -> float:
        """Convert bar to Pascal."""
        return pressure_bar * 1e5
    
    @staticmethod
    def pascal_to_bar(pressure_pa: float) -> float:
        """Convert Pascal to bar."""
        return pressure_pa / 1e5
    
    @staticmethod
    def psi_to_pascal(pressure_psi: float) -> float:
        """Convert psi to Pascal."""
        return pressure_psi * 6894.76
    
    @staticmethod
    def pascal_to_psi(pressure_pa: float) -> float:
        """Convert Pascal to psi."""
        return pressure_pa / 6894.76
    
    @staticmethod
    def atm_to_pascal(pressure_atm: float) -> float:
        """Convert atm to Pascal."""
        return pressure_atm * 101325
    
    @staticmethod
    def pascal_to_atm(pressure_pa: float) -> float:
        """Convert Pascal to atm."""
        return pressure_pa / 101325
    
    @staticmethod
    def kmol_s_to_kmol_h(flow_kmol_s: float) -> float:
        """Convert kmol/s to kmol/h."""
        return flow_kmol_s * 3600
    
    @staticmethod
    def kmol_h_to_kmol_s(flow_kmol_h: float) -> float:
        """Convert kmol/h to kmol/s."""
        return flow_kmol_h / 3600


if __name__ == "__main__":
    # Example usage
    from src.core.component import create_water, create_methane
    
    print("=== Stream Module Demo ===\n")
    
    # Create components
    water = create_water()
    methane = create_methane()
    
    # Create a stream
    stream1 = Stream(
        name="Feed-1",
        temperature=UnitConversion.celsius_to_kelvin(25),  # 25°C
        pressure=UnitConversion.bar_to_pascal(10),  # 10 bar
        components={'Water': water, 'Methane': methane},
        mole_fractions={'Water': 0.6, 'Methane': 0.4},
        molar_flow=100.0,  # kmol/s
        phase="liquid"
    )
    
    print(stream1.summary())
    print("\n" + "="*50 + "\n")
    
    # Create another stream
    stream2 = Stream(
        name="Feed-2",
        temperature=UnitConversion.celsius_to_kelvin(50),  # 50°C
        pressure=UnitConversion.bar_to_pascal(10),  # 10 bar
        components={'Water': water, 'Methane': methane},
        mole_fractions={'Water': 0.3, 'Methane': 0.7},
        molar_flow=50.0,  # kmol/s
        phase="vapor"
    )
    
    print(stream2.summary())
    print("\n" + "="*50 + "\n")
    
    # Mix the streams
    mixed = stream1.mix_with(stream2)
    print("Mixed Stream:")
    print(mixed.summary())
    print("\n" + "="*50 + "\n")
    
    # Split a stream
    split1 = stream1.split(0.7, "_A")
    split2 = stream1.split(0.3, "_B")
    print(f"Original: {stream1}")
    print(f"Split A (70%): {split1}")
    print(f"Split B (30%): {split2}")
