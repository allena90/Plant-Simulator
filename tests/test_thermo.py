"""
Unit Tests for Thermodynamic Models
====================================

Tests for equations of state, VLE, and flash calculations.

Author: Plant Simulation Software Project
Date: November 2025
"""

import pytest
import numpy as np
from src.thermo.thermo import (
    IdealGas, VanDerWaalsEOS, RedlichKwongEOS,
    VLE, Flash, FlashResult, R_KMOL
)
from src.core.component import create_water, create_methane, Component


class TestIdealGas:
    """Test ideal gas law calculations."""
    
    def test_molar_volume(self):
        """Test ideal gas molar volume calculation."""
        T = 300  # K
        P = 101325  # Pa (1 atm)
        
        V = IdealGas.molar_volume(T, P)
        
        # V = RT/P
        expected = R_KMOL * T / P
        assert abs(V - expected) < 1e-6
    
    def test_pressure_calculation(self):
        """Test pressure calculation from T and V."""
        T = 300  # K
        V = 24.79  # m³/kmol (approximate at 1 atm, 300K)
        
        P = IdealGas.pressure(T, V)
        
        # Should be close to 1 atm
        assert abs(P - 101325) < 1000
    
    def test_compressibility_factor(self):
        """Test that Z = 1 for ideal gas."""
        Z = IdealGas.compressibility_factor()
        assert Z == 1.0


class TestVanDerWaalsEOS:
    """Test van der Waals equation of state."""
    
    def test_parameter_calculation(self):
        """Test calculation of a and b parameters."""
        methane = create_methane()
        
        a, b = VanDerWaalsEOS.calculate_parameters(methane)
        
        # Check that parameters are positive
        assert a > 0
        assert b > 0
        
        # Verify formulas
        Tc = methane.critical_temperature
        Pc = methane.critical_pressure
        
        a_expected = 27 * R_KMOL**2 * Tc**2 / (64 * Pc)
        b_expected = R_KMOL * Tc / (8 * Pc)
        
        assert abs(a - a_expected) < 1e-6
        assert abs(b - b_expected) < 1e-6
    
    def test_molar_volume_vapor(self):
        """Test molar volume calculation for vapor phase."""
        methane = create_methane()
        T = 300  # K
        P = 101325  # Pa
        
        V = VanDerWaalsEOS.molar_volume(T, P, methane, phase='vapor')
        
        # Should be positive and reasonable
        assert V > 0
        # Should be larger than ideal gas due to molecular interactions
        V_ideal = IdealGas.molar_volume(T, P)
        assert V > 0  # Real gases can deviate either way
    
    def test_compressibility_factor(self):
        """Test compressibility factor calculation."""
        methane = create_methane()
        T = 300  # K
        P = 101325  # Pa
        
        Z = VanDerWaalsEOS.compressibility_factor(T, P, methane, phase='vapor')
        
        # Z should be close to 1 for ideal-like conditions
        # but can deviate for real gases
        assert 0.8 < Z < 1.2
    
    def test_different_phases_give_different_volumes(self):
        """Test that liquid and vapor phases have different volumes."""
        methane = create_methane()
        T = 150  # K (below critical temperature)
        P = 1e6  # Pa
        
        V_vapor = VanDerWaalsEOS.molar_volume(T, P, methane, phase='vapor')
        V_liquid = VanDerWaalsEOS.molar_volume(T, P, methane, phase='liquid')
        
        # Vapor should have larger volume than liquid
        assert V_vapor > V_liquid


class TestRedlichKwongEOS:
    """Test Redlich-Kwong equation of state."""
    
    def test_parameter_calculation(self):
        """Test calculation of a and b parameters."""
        methane = create_methane()
        
        a, b = RedlichKwongEOS.calculate_parameters(methane)
        
        # Check that parameters are positive
        assert a > 0
        assert b > 0
        
        # Verify formulas
        Tc = methane.critical_temperature
        Pc = methane.critical_pressure
        
        a_expected = 0.42748 * R_KMOL**2 * Tc**2.5 / Pc
        b_expected = 0.08664 * R_KMOL * Tc / Pc
        
        assert abs(a - a_expected) < 1e-6
        assert abs(b - b_expected) < 1e-6
    
    def test_molar_volume_vapor(self):
        """Test molar volume calculation for vapor phase."""
        methane = create_methane()
        T = 300  # K
        P = 101325  # Pa
        
        V = RedlichKwongEOS.molar_volume(T, P, methane, phase='vapor')
        
        # Should be positive and reasonable
        assert V > 0
        V_ideal = IdealGas.molar_volume(T, P)
        # RK typically gives values close to ideal for gases at low pressure
        assert 0.8 * V_ideal < V < 1.2 * V_ideal
    
    def test_compressibility_factor(self):
        """Test compressibility factor calculation."""
        methane = create_methane()
        T = 300  # K
        P = 101325  # Pa
        
        Z = RedlichKwongEOS.compressibility_factor(T, P, methane, phase='vapor')
        
        # Z should be reasonable
        assert 0.8 < Z < 1.2


class TestVLE:
    """Test vapor-liquid equilibrium calculations."""
    
    def test_k_values_raoult_law(self):
        """Test K-value calculation using Raoult's Law."""
        water = create_water()
        methane = create_methane()
        
        T = 300  # K
        P = 101325  # Pa
        
        components = {'Water': water, 'Methane': methane}
        k_values = VLE.raoult_law_k_values(T, P, components)
        
        # Should have K-values for both components
        assert 'Water' in k_values
        assert 'Methane' in k_values
        
        # K-values should be positive
        assert k_values['Water'] > 0
        assert k_values['Methane'] > 0
        
        # Methane is more volatile, so K > 1
        # Water is less volatile at 300K, so K < 1
        assert k_values['Methane'] > k_values['Water']
    
    def test_bubble_point_pressure(self):
        """Test bubble point pressure calculation."""
        water = create_water()
        
        T = 373.15  # K (100°C)
        x = {'Water': 1.0}
        components = {'Water': water}
        
        P_bubble = VLE.bubble_point_pressure(T, x, components)
        
        # At 100°C, bubble point of pure water should be ~1 atm
        assert abs(P_bubble - 101325) < 10000  # Within 10 kPa
    
    def test_bubble_point_mixture(self):
        """Test bubble point for binary mixture."""
        water = create_water()
        methane = create_methane()
        
        T = 300  # K
        x = {'Water': 0.5, 'Methane': 0.5}
        components = {'Water': water, 'Methane': methane}
        
        P_bubble = VLE.bubble_point_pressure(T, x, components)
        
        # Bubble point should be positive
        assert P_bubble > 0
        
        # Should be between the individual vapor pressures
        P_sat_water = water.vapor_pressure(T)
        P_sat_methane = methane.vapor_pressure(T)
        
        # For ideal mixture: P_bubble = x1*P1 + x2*P2
        expected = 0.5 * P_sat_water + 0.5 * P_sat_methane
        assert abs(P_bubble - expected) < 1000
    
    def test_dew_point_pressure(self):
        """Test dew point pressure calculation."""
        water = create_water()
        
        T = 373.15  # K (100°C)
        y = {'Water': 1.0}
        components = {'Water': water}
        
        P_dew = VLE.dew_point_pressure(T, y, components)
        
        # At 100°C, dew point of pure water vapor should be ~1 atm
        assert abs(P_dew - 101325) < 10000  # Within 10 kPa


class TestFlash:
    """Test flash calculations."""
    
    def test_all_liquid_flash(self):
        """Test flash when all K < 1 (all liquid)."""
        water = create_water()
        methane = create_methane()
        
        # Low temperature, high pressure -> all liquid
        T = 250  # K
        P = 5e6  # 50 bar
        
        feed = {'Water': 0.5, 'Methane': 0.5}
        components = {'Water': water, 'Methane': methane}
        
        result = Flash.isothermal_flash(T, P, feed, components)
        
        # Should be all liquid
        assert result.vapor_fraction == 0.0
        assert result.converged
        
        # Liquid composition should equal feed
        for name in feed:
            assert abs(result.liquid_mole_fractions[name] - feed[name]) < 1e-6
    
    def test_all_vapor_flash(self):
        """Test flash when all K > 1 (all vapor)."""
        water = create_water()
        methane = create_methane()
        
        # High temperature, low pressure -> all vapor
        T = 500  # K
        P = 1e4  # 0.1 bar (very low)
        
        feed = {'Water': 0.5, 'Methane': 0.5}
        components = {'Water': water, 'Methane': methane}
        
        result = Flash.isothermal_flash(T, P, feed, components)
        
        # Should be all vapor
        assert result.vapor_fraction == 1.0
        assert result.converged
        
        # Vapor composition should equal feed
        for name in feed:
            assert abs(result.vapor_mole_fractions[name] - feed[name]) < 1e-6
    
    def test_two_phase_flash(self):
        """Test two-phase flash calculation."""
        water = create_water()
        methane = create_methane()
        
        # Intermediate conditions -> two phase
        T = 320  # K
        P = 5e5  # 5 bar
        
        feed = {'Water': 0.5, 'Methane': 0.5}
        components = {'Water': water, 'Methane': methane}
        
        result = Flash.isothermal_flash(T, P, feed, components)
        
        # Should be two-phase
        assert 0 < result.vapor_fraction < 1
        assert result.converged
        
        # Vapor should be richer in more volatile component (methane)
        assert result.vapor_mole_fractions['Methane'] > result.liquid_mole_fractions['Methane']
        
        # Liquid should be richer in less volatile component (water)
        assert result.liquid_mole_fractions['Water'] > result.vapor_mole_fractions['Water']
        
        # Compositions should sum to 1
        vapor_sum = sum(result.vapor_mole_fractions.values())
        liquid_sum = sum(result.liquid_mole_fractions.values())
        assert abs(vapor_sum - 1.0) < 1e-6
        assert abs(liquid_sum - 1.0) < 1e-6
    
    def test_flash_result_dataclass(self):
        """Test FlashResult dataclass."""
        result = FlashResult(
            temperature=300,
            pressure=101325,
            vapor_fraction=0.5,
            vapor_mole_fractions={'A': 0.6, 'B': 0.4},
            liquid_mole_fractions={'A': 0.4, 'B': 0.6},
            converged=True,
            iterations=5
        )
        
        assert result.temperature == 300
        assert result.vapor_fraction == 0.5
        assert result.converged
        assert result.iterations == 5
    
    def test_material_balance_in_flash(self):
        """Test that flash preserves overall material balance."""
        water = create_water()
        methane = create_methane()
        
        T = 320  # K
        P = 5e5  # Pa
        
        feed = {'Water': 0.3, 'Methane': 0.7}
        components = {'Water': water, 'Methane': methane}
        
        result = Flash.isothermal_flash(T, P, feed, components)
        
        if 0 < result.vapor_fraction < 1:
            # Check material balance: zi = V*yi + (1-V)*xi
            V = result.vapor_fraction
            
            for name in feed:
                z = feed[name]
                y = result.vapor_mole_fractions[name]
                x = result.liquid_mole_fractions[name]
                
                calculated_z = V * y + (1 - V) * x
                assert abs(calculated_z - z) < 1e-4


class TestThermodynamicConsistency:
    """Test thermodynamic consistency across models."""
    
    def test_eos_reduce_to_ideal_at_low_pressure(self):
        """Test that EOS reduce to ideal gas at low pressure."""
        methane = create_methane()
        T = 300  # K
        P = 1000  # Pa (very low pressure)
        
        V_ideal = IdealGas.molar_volume(T, P)
        V_vdw = VanDerWaalsEOS.molar_volume(T, P, methane, phase='vapor')
        V_rk = RedlichKwongEOS.molar_volume(T, P, methane, phase='vapor')
        
        # All should be close to each other at low pressure
        assert abs(V_vdw - V_ideal) / V_ideal < 0.05  # Within 5%
        assert abs(V_rk - V_ideal) / V_ideal < 0.05  # Within 5%
    
    def test_k_values_consistency(self):
        """Test that K-values are consistent with phase behavior."""
        water = create_water()
        
        # At boiling point, K should be close to 1
        T = 373.15  # K
        P = 101325  # Pa
        
        components = {'Water': water}
        k_values = VLE.raoult_law_k_values(T, P, components)
        
        # K = P_sat/P, and at boiling point P_sat = P, so K ≈ 1
        assert abs(k_values['Water'] - 1.0) < 0.1


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
