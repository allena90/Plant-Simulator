"""
Thermodynamic Models Module
============================

This module implements basic thermodynamic models including:
- Ideal Gas Law
- Equations of State (van der Waals, Redlich-Kwong)
- Vapor-Liquid Equilibrium (Raoult's Law)
- Flash Calculations

Author: Plant Simulation Software Project
Date: November 2025
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from src.core.component import Component
from src.core.stream import Stream


# Universal gas constant
R = 8.314462  # J/(mol·K) or m³·Pa/(mol·K)
R_KMOL = 8314.462  # J/(kmol·K)


@dataclass
class FlashResult:
    """
    Result from a flash calculation.
    
    Attributes:
        temperature (float): Temperature in K
        pressure (float): Pressure in Pa
        vapor_fraction (float): Vapor mole fraction (0 = all liquid, 1 = all vapor)
        vapor_mole_fractions (Dict[str, float]): Composition of vapor phase
        liquid_mole_fractions (Dict[str, float]): Composition of liquid phase
        converged (bool): Whether the calculation converged
        iterations (int): Number of iterations required
    """
    temperature: float
    pressure: float
    vapor_fraction: float
    vapor_mole_fractions: Dict[str, float]
    liquid_mole_fractions: Dict[str, float]
    converged: bool
    iterations: int


class IdealGas:
    """
    Ideal gas law calculations.
    
    PV = nRT
    """
    
    @staticmethod
    def molar_volume(temperature: float, pressure: float) -> float:
        """
        Calculate molar volume of ideal gas.
        
        V = RT/P
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            
        Returns:
            float: Molar volume in m³/kmol
        """
        return R_KMOL * temperature / pressure
    
    @staticmethod
    def pressure(temperature: float, molar_volume: float) -> float:
        """
        Calculate pressure from temperature and molar volume.
        
        P = RT/V
        
        Args:
            temperature (float): Temperature in K
            molar_volume (float): Molar volume in m³/kmol
            
        Returns:
            float: Pressure in Pa
        """
        return R_KMOL * temperature / molar_volume
    
    @staticmethod
    def compressibility_factor() -> float:
        """Return compressibility factor for ideal gas (always 1.0)."""
        return 1.0


class VanDerWaalsEOS:
    """
    Van der Waals equation of state.
    
    (P + a/V²)(V - b) = RT
    
    where:
        a = 27R²Tc²/(64Pc)
        b = RTc/(8Pc)
    """
    
    @staticmethod
    def calculate_parameters(component: Component) -> Tuple[float, float]:
        """
        Calculate van der Waals parameters a and b.
        
        Args:
            component (Component): Component with critical properties
            
        Returns:
            Tuple[float, float]: Parameters (a, b)
                a in Pa·m⁶/kmol²
                b in m³/kmol
        """
        Tc = component.critical_temperature
        Pc = component.critical_pressure
        
        a = 27 * R_KMOL**2 * Tc**2 / (64 * Pc)
        b = R_KMOL * Tc / (8 * Pc)
        
        return a, b
    
    @staticmethod
    def molar_volume(temperature: float, pressure: float, component: Component,
                     phase: str = 'vapor') -> float:
        """
        Calculate molar volume using van der Waals EOS.
        
        Solves cubic equation: V³ - (b + RT/P)V² + (a/P)V - ab/P = 0
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            component (Component): Component
            phase (str): 'vapor' or 'liquid' (determines which root to use)
            
        Returns:
            float: Molar volume in m³/kmol
        """
        a, b = VanDerWaalsEOS.calculate_parameters(component)
        
        # Coefficients of cubic equation: V³ + c2·V² + c1·V + c0 = 0
        c2 = -(b + R_KMOL * temperature / pressure)
        c1 = a / pressure
        c0 = -a * b / pressure
        
        # Solve cubic equation
        coeffs = [1, c2, c1, c0]
        roots = np.roots(coeffs)
        
        # Filter for real, positive roots
        real_roots = []
        for root in roots:
            if np.isreal(root) and np.real(root) > b:
                real_roots.append(np.real(root))
        
        if not real_roots:
            raise ValueError("No valid roots found in van der Waals EOS")
        
        # Return largest root for vapor, smallest for liquid
        if phase == 'vapor':
            return max(real_roots)
        else:
            return min(real_roots)
    
    @staticmethod
    def compressibility_factor(temperature: float, pressure: float, 
                               component: Component, phase: str = 'vapor') -> float:
        """
        Calculate compressibility factor Z = PV/(RT).
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            component (Component): Component
            phase (str): 'vapor' or 'liquid'
            
        Returns:
            float: Compressibility factor (dimensionless)
        """
        V = VanDerWaalsEOS.molar_volume(temperature, pressure, component, phase)
        Z = pressure * V / (R_KMOL * temperature)
        return Z


class RedlichKwongEOS:
    """
    Redlich-Kwong equation of state.
    
    P = RT/(V-b) - a/(T^0.5·V(V+b))
    
    where:
        a = 0.42748·R²·Tc^2.5/Pc
        b = 0.08664·R·Tc/Pc
    """
    
    @staticmethod
    def calculate_parameters(component: Component) -> Tuple[float, float]:
        """
        Calculate Redlich-Kwong parameters a and b.
        
        Args:
            component (Component): Component with critical properties
            
        Returns:
            Tuple[float, float]: Parameters (a, b)
                a in Pa·m⁶·K^0.5/kmol²
                b in m³/kmol
        """
        Tc = component.critical_temperature
        Pc = component.critical_pressure
        
        a = 0.42748 * R_KMOL**2 * Tc**2.5 / Pc
        b = 0.08664 * R_KMOL * Tc / Pc
        
        return a, b
    
    @staticmethod
    def molar_volume(temperature: float, pressure: float, component: Component,
                     phase: str = 'vapor') -> float:
        """
        Calculate molar volume using Redlich-Kwong EOS.
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            component (Component): Component
            phase (str): 'vapor' or 'liquid'
            
        Returns:
            float: Molar volume in m³/kmol
        """
        a, b = RedlichKwongEOS.calculate_parameters(component)
        
        # RK equation rearranged to cubic form
        # V³ - (RT/P)V² - (b²·RT/P + b·a/(P·√T) - a/(P·√T))V - ab/(P·√T) = 0
        
        A = a / (pressure * np.sqrt(temperature))
        B = b
        
        c2 = -R_KMOL * temperature / pressure
        c1 = -(B**2 * R_KMOL * temperature / pressure + B * A - A)
        c0 = -A * B
        
        coeffs = [1, c2, c1, c0]
        roots = np.roots(coeffs)
        
        # Filter for real, positive roots
        real_roots = []
        for root in roots:
            if np.isreal(root) and np.real(root) > b:
                real_roots.append(np.real(root))
        
        if not real_roots:
            raise ValueError("No valid roots found in Redlich-Kwong EOS")
        
        # Return largest root for vapor, smallest for liquid
        if phase == 'vapor':
            return max(real_roots)
        else:
            return min(real_roots)
    
    @staticmethod
    def compressibility_factor(temperature: float, pressure: float,
                               component: Component, phase: str = 'vapor') -> float:
        """
        Calculate compressibility factor Z = PV/(RT).
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            component (Component): Component
            phase (str): 'vapor' or 'liquid'
            
        Returns:
            float: Compressibility factor (dimensionless)
        """
        V = RedlichKwongEOS.molar_volume(temperature, pressure, component, phase)
        Z = pressure * V / (R_KMOL * temperature)
        return Z


class VLE:
    """
    Vapor-Liquid Equilibrium calculations.
    
    Implements Raoult's Law for ideal mixtures:
    yi·P = xi·Pi_sat
    """
    
    @staticmethod
    def raoult_law_k_values(temperature: float, pressure: float,
                            components: Dict[str, Component]) -> Dict[str, float]:
        """
        Calculate K-values using Raoult's Law.
        
        K_i = P_i_sat / P
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            components (Dict[str, Component]): Components in mixture
            
        Returns:
            Dict[str, float]: K-values for each component
        """
        k_values = {}
        
        for name, comp in components.items():
            try:
                p_sat = comp.vapor_pressure(temperature)
                k_values[name] = p_sat / pressure
            except (ValueError, AttributeError):
                # Component doesn't have vapor pressure data
                # Assume K = 1 (no separation)
                k_values[name] = 1.0
        
        return k_values
    
    @staticmethod
    def bubble_point_pressure(temperature: float, liquid_mole_fractions: Dict[str, float],
                             components: Dict[str, Component]) -> float:
        """
        Calculate bubble point pressure at given temperature.
        
        P_bubble = Σ(xi·Pi_sat)
        
        Args:
            temperature (float): Temperature in K
            liquid_mole_fractions (Dict[str, float]): Liquid composition
            components (Dict[str, Component]): Components
            
        Returns:
            float: Bubble point pressure in Pa
        """
        p_bubble = 0.0
        
        for name, x_i in liquid_mole_fractions.items():
            if name in components:
                try:
                    p_sat = components[name].vapor_pressure(temperature)
                    p_bubble += x_i * p_sat
                except (ValueError, AttributeError):
                    pass
        
        return p_bubble
    
    @staticmethod
    def dew_point_pressure(temperature: float, vapor_mole_fractions: Dict[str, float],
                          components: Dict[str, Component]) -> float:
        """
        Calculate dew point pressure at given temperature.
        
        P_dew = 1 / Σ(yi/Pi_sat)
        
        Args:
            temperature (float): Temperature in K
            vapor_mole_fractions (Dict[str, float]): Vapor composition
            components (Dict[str, Component]): Components
            
        Returns:
            float: Dew point pressure in Pa
        """
        sum_inv = 0.0
        
        for name, y_i in vapor_mole_fractions.items():
            if name in components:
                try:
                    p_sat = components[name].vapor_pressure(temperature)
                    if p_sat > 0:
                        sum_inv += y_i / p_sat
                except (ValueError, AttributeError):
                    pass
        
        if sum_inv > 0:
            return 1.0 / sum_inv
        else:
            return 0.0


class Flash:
    """
    Flash calculations for vapor-liquid separation.
    
    Performs isothermal flash: given T, P, and feed composition,
    calculate vapor fraction and phase compositions.
    """
    
    @staticmethod
    def isothermal_flash(temperature: float, pressure: float,
                        feed_mole_fractions: Dict[str, float],
                        components: Dict[str, Component],
                        max_iterations: int = 100,
                        tolerance: float = 1e-6) -> FlashResult:
        """
        Perform isothermal flash calculation.
        
        Rachford-Rice equation:
        f(V) = Σ[zi(Ki-1)/(1+V(Ki-1))] = 0
        
        Args:
            temperature (float): Temperature in K
            pressure (float): Pressure in Pa
            feed_mole_fractions (Dict[str, float]): Feed composition
            components (Dict[str, Component]): Components
            max_iterations (int): Maximum iterations
            tolerance (float): Convergence tolerance
            
        Returns:
            FlashResult: Flash calculation results
        """
        # Get K-values
        k_values = VLE.raoult_law_k_values(temperature, pressure, components)
        
        # Check if single phase
        # All liquid if all K < 1, all vapor if all K > 1
        k_min = min(k_values.values())
        k_max = max(k_values.values())
        
        if k_max <= 1.0:
            # All liquid
            return FlashResult(
                temperature=temperature,
                pressure=pressure,
                vapor_fraction=0.0,
                vapor_mole_fractions={},
                liquid_mole_fractions=feed_mole_fractions.copy(),
                converged=True,
                iterations=0
            )
        
        if k_min >= 1.0:
            # All vapor
            return FlashResult(
                temperature=temperature,
                pressure=pressure,
                vapor_fraction=1.0,
                vapor_mole_fractions=feed_mole_fractions.copy(),
                liquid_mole_fractions={},
                converged=True,
                iterations=0
            )
        
        # Two-phase region - solve Rachford-Rice equation
        # Use Newton-Raphson method
        
        def rachford_rice(V: float) -> float:
            """Rachford-Rice objective function."""
            f = 0.0
            for name, z_i in feed_mole_fractions.items():
                K_i = k_values[name]
                f += z_i * (K_i - 1) / (1 + V * (K_i - 1))
            return f
        
        def rachford_rice_derivative(V: float) -> float:
            """Derivative of Rachford-Rice function."""
            df = 0.0
            for name, z_i in feed_mole_fractions.items():
                K_i = k_values[name]
                denominator = 1 + V * (K_i - 1)
                df -= z_i * (K_i - 1)**2 / denominator**2
            return df
        
        # Initial guess for vapor fraction
        V = 0.5
        
        # Newton-Raphson iteration
        converged = False
        for iteration in range(max_iterations):
            f = rachford_rice(V)
            df = rachford_rice_derivative(V)
            
            if abs(f) < tolerance:
                converged = True
                break
            
            if abs(df) < 1e-10:
                # Derivative too small, use bisection backup
                break
            
            # Newton step
            V_new = V - f / df
            
            # Keep V in bounds [0, 1]
            V_new = max(0.0, min(1.0, V_new))
            
            V = V_new
        
        # Calculate phase compositions
        vapor_comp = {}
        liquid_comp = {}
        
        for name, z_i in feed_mole_fractions.items():
            K_i = k_values[name]
            
            # xi = zi / [1 + V(Ki - 1)]
            x_i = z_i / (1 + V * (K_i - 1))
            
            # yi = Ki·xi
            y_i = K_i * x_i
            
            liquid_comp[name] = x_i
            vapor_comp[name] = y_i
        
        return FlashResult(
            temperature=temperature,
            pressure=pressure,
            vapor_fraction=V,
            vapor_mole_fractions=vapor_comp,
            liquid_mole_fractions=liquid_comp,
            converged=converged,
            iterations=iteration + 1
        )


if __name__ == "__main__":
    # Example usage
    from src.core.component import create_water, create_methane
    from src.core.stream import UnitConversion
    
    print("=== Thermodynamic Models Demo ===\n")
    
    # 1. Ideal Gas Law
    print("1. IDEAL GAS LAW")
    print("-" * 50)
    T = 300  # K
    P = 101325  # Pa
    V_ideal = IdealGas.molar_volume(T, P)
    print(f"Ideal gas molar volume at {T}K, {P/1e5:.2f}bar: {V_ideal:.4f} m³/kmol")
    print()
    
    # 2. Van der Waals EOS
    print("2. VAN DER WAALS EQUATION OF STATE")
    print("-" * 50)
    methane = create_methane()
    a, b = VanDerWaalsEOS.calculate_parameters(methane)
    print(f"Methane van der Waals parameters:")
    print(f"  a = {a:.4e} Pa·m⁶/kmol²")
    print(f"  b = {b:.4e} m³/kmol")
    
    V_vdw = VanDerWaalsEOS.molar_volume(T, P, methane, phase='vapor')
    Z_vdw = VanDerWaalsEOS.compressibility_factor(T, P, methane, phase='vapor')
    print(f"Molar volume (vapor): {V_vdw:.4f} m³/kmol")
    print(f"Compressibility factor: {Z_vdw:.4f}")
    print()
    
    # 3. Redlich-Kwong EOS
    print("3. REDLICH-KWONG EQUATION OF STATE")
    print("-" * 50)
    a_rk, b_rk = RedlichKwongEOS.calculate_parameters(methane)
    print(f"Methane Redlich-Kwong parameters:")
    print(f"  a = {a_rk:.4e} Pa·m⁶·K^0.5/kmol²")
    print(f"  b = {b_rk:.4e} m³/kmol")
    
    V_rk = RedlichKwongEOS.molar_volume(T, P, methane, phase='vapor')
    Z_rk = RedlichKwongEOS.compressibility_factor(T, P, methane, phase='vapor')
    print(f"Molar volume (vapor): {V_rk:.4f} m³/kmol")
    print(f"Compressibility factor: {Z_rk:.4f}")
    print()
    
    # 4. VLE Calculations
    print("4. VAPOR-LIQUID EQUILIBRIUM")
    print("-" * 50)
    water = create_water()
    T_vle = UnitConversion.celsius_to_kelvin(80)  # 80°C
    P_vle = UnitConversion.bar_to_pascal(1)  # 1 bar
    
    components = {'Water': water, 'Methane': methane}
    k_values = VLE.raoult_law_k_values(T_vle, P_vle, components)
    print(f"K-values at {T_vle}K, {P_vle/1e5:.2f}bar:")
    for name, k in k_values.items():
        print(f"  {name}: {k:.4f}")
    
    # Bubble and dew point
    x = {'Water': 0.5, 'Methane': 0.5}
    P_bubble = VLE.bubble_point_pressure(T_vle, x, components)
    P_dew = VLE.dew_point_pressure(T_vle, x, components)
    print(f"\nBubble point pressure: {P_bubble/1e5:.4f} bar")
    print(f"Dew point pressure: {P_dew/1e5:.4f} bar")
    print()
    
    # 5. Flash Calculation
    print("5. ISOTHERMAL FLASH CALCULATION")
    print("-" * 50)
    feed_comp = {'Water': 0.5, 'Methane': 0.5}
    flash_result = Flash.isothermal_flash(T_vle, P_vle, feed_comp, components)
    
    print(f"Feed: {feed_comp}")
    print(f"Temperature: {flash_result.temperature}K")
    print(f"Pressure: {flash_result.pressure/1e5:.4f}bar")
    print(f"Vapor fraction: {flash_result.vapor_fraction:.4f}")
    print(f"Converged: {flash_result.converged} (iterations: {flash_result.iterations})")
    print(f"\nVapor composition:")
    for name, y in flash_result.vapor_mole_fractions.items():
        print(f"  {name}: {y:.4f}")
    print(f"\nLiquid composition:")
    for name, x in flash_result.liquid_mole_fractions.items():
        print(f"  {name}: {x:.4f}")
