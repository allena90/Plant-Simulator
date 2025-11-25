"""
Unit Tests for Component Module
================================

Tests for the Component class and related functions.

Author: Plant Simulation Software Project
Date: November 2025
"""

import pytest
import math
from src.core.component import Component, create_water, create_methane


class TestComponentBasics:
    """Test basic component creation and validation."""
    
    def test_create_valid_component(self):
        """Test creating a valid component."""
        comp = Component(
            name="Nitrogen",
            formula="N2",
            molecular_weight=28.014,
            critical_temperature=126.2,
            critical_pressure=3.39e6
        )
        assert comp.name == "Nitrogen"
        assert comp.formula == "N2"
        assert comp.molecular_weight == 28.014
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Component(
                name="",
                formula="N2",
                molecular_weight=28.014
            )
    
    def test_empty_formula_raises_error(self):
        """Test that empty formula raises ValueError."""
        with pytest.raises(ValueError, match="formula cannot be empty"):
            Component(
                name="Nitrogen",
                formula="",
                molecular_weight=28.014
            )
    
    def test_zero_molecular_weight_raises_error(self):
        """Test that zero or negative MW raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            Component(
                name="Nitrogen",
                formula="N2",
                molecular_weight=0
            )
    
    def test_negative_molecular_weight_raises_error(self):
        """Test that negative MW raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            Component(
                name="Nitrogen",
                formula="N2",
                molecular_weight=-10
            )


class TestComponentProperties:
    """Test component property calculations."""
    
    def test_reduced_temperature(self):
        """Test reduced temperature calculation."""
        water = create_water()
        T = 373.15  # K (100°C)
        Tr = water.reduced_temperature(T)
        expected = T / water.critical_temperature
        assert abs(Tr - expected) < 1e-6
    
    def test_reduced_pressure(self):
        """Test reduced pressure calculation."""
        water = create_water()
        P = 101325  # Pa (1 atm)
        Pr = water.reduced_pressure(P)
        expected = P / water.critical_pressure
        assert abs(Pr - expected) < 1e-6
    
    def test_reduced_temp_without_tc_raises_error(self):
        """Test that reduced temperature without Tc raises error."""
        comp = Component(
            name="Test",
            formula="T",
            molecular_weight=10,
            critical_temperature=0  # Invalid
        )
        with pytest.raises(ValueError, match="Critical temperature not defined"):
            comp.reduced_temperature(300)
    
    def test_reduced_pressure_without_pc_raises_error(self):
        """Test that reduced pressure without Pc raises error."""
        comp = Component(
            name="Test",
            formula="T",
            molecular_weight=10,
            critical_pressure=0  # Invalid
        )
        with pytest.raises(ValueError, match="Critical pressure not defined"):
            comp.reduced_pressure(101325)


class TestVaporPressure:
    """Test vapor pressure calculations using Antoine equation."""
    
    def test_water_vapor_pressure_at_100C(self):
        """Test water vapor pressure at 100°C (should be ~1 atm)."""
        water = create_water()
        T = 373.15  # K
        P_sat = water.vapor_pressure(T)
        # At 100°C, water vapor pressure should be close to 1 atm (101325 Pa)
        assert abs(P_sat - 101325) < 5000  # Within 5 kPa
    
    def test_vapor_pressure_without_antoine_raises_error(self):
        """Test that vapor pressure without Antoine coeffs raises error."""
        comp = Component(
            name="Test",
            formula="T",
            molecular_weight=10
        )
        with pytest.raises(ValueError, match="Antoine coefficients not defined"):
            comp.vapor_pressure(300)
    
    def test_vapor_pressure_increases_with_temperature(self):
        """Test that vapor pressure increases with temperature."""
        water = create_water()
        P1 = water.vapor_pressure(350)
        P2 = water.vapor_pressure(360)
        P3 = water.vapor_pressure(370)
        assert P2 > P1
        assert P3 > P2


class TestHeatCapacity:
    """Test ideal gas heat capacity calculations."""
    
    def test_water_heat_capacity(self):
        """Test water ideal gas heat capacity calculation."""
        water = create_water()
        T = 373.15  # K
        cp = water.cp_ideal_gas(T)
        # Water Cp at 100°C should be around 33-34 kJ/(kmol·K)
        assert 43000 < cp < 45000
    
    def test_heat_capacity_without_coeffs_raises_error(self):
        """Test that Cp calculation without coeffs raises error."""
        comp = Component(
            name="Test",
            formula="T",
            molecular_weight=10
        )
        with pytest.raises(ValueError, match="Heat capacity coefficients not defined"):
            comp.cp_ideal_gas(300)
    
    def test_heat_capacity_increases_with_temperature(self):
        """Test that heat capacity generally increases with temperature."""
        water = create_water()
        cp1 = water.cp_ideal_gas(300)
        cp2 = water.cp_ideal_gas(400)
        cp3 = water.cp_ideal_gas(500)
        # For most substances, Cp increases with T
        assert cp2 > cp1
        assert cp3 > cp2


class TestPreDefinedComponents:
    """Test pre-defined component creation functions."""
    
    def test_create_water(self):
        """Test water component creation."""
        water = create_water()
        assert water.name == "Water"
        assert water.formula == "H2O"
        assert water.molecular_weight == 18.015
        assert water.phase_at_stp == "liquid"
    
    def test_create_methane(self):
        """Test methane component creation."""
        methane = create_methane()
        assert methane.name == "Methane"
        assert methane.formula == "CH4"
        assert methane.molecular_weight == 16.043
        assert methane.phase_at_stp == "gas"
    
    def test_water_has_all_properties(self):
        """Test that water has all necessary properties defined."""
        water = create_water()
        assert water.critical_temperature > 0
        assert water.critical_pressure > 0
        assert water.acentric_factor >= 0
        assert water.normal_boiling_point is not None
        assert water.antoine_a is not None


class TestSerialization:
    """Test component serialization and deserialization."""
    
    def test_to_dict(self):
        """Test converting component to dictionary."""
        water = create_water()
        data = water.to_dict()
        assert isinstance(data, dict)
        assert data['name'] == "Water"
        assert data['formula'] == "H2O"
        assert data['molecular_weight'] == 18.015
    
    def test_from_dict(self):
        """Test creating component from dictionary."""
        data = {
            'name': "Oxygen",
            'formula': "O2",
            'cas_number': "7782-44-7",
            'molecular_weight': 32.0,
            'critical_temperature': 154.6,
            'critical_pressure': 5.043e6,
            'acentric_factor': 0.022,
            'phase_at_stp': "gas"
        }
        comp = Component.from_dict(data)
        assert comp.name == "Oxygen"
        assert comp.formula == "O2"
        assert comp.molecular_weight == 32.0
    
    def test_round_trip_serialization(self):
        """Test that serialization and deserialization preserves data."""
        original = create_water()
        data = original.to_dict()
        restored = Component.from_dict(data)
        
        assert restored.name == original.name
        assert restored.formula == original.formula
        assert restored.molecular_weight == original.molecular_weight
        assert restored.critical_temperature == original.critical_temperature


class TestStringRepresentations:
    """Test string representation methods."""
    
    def test_repr(self):
        """Test __repr__ method."""
        water = create_water()
        repr_str = repr(water)
        assert "Component" in repr_str
        assert "Water" in repr_str
        assert "H2O" in repr_str
    
    def test_str(self):
        """Test __str__ method."""
        water = create_water()
        str_repr = str(water)
        assert "Water" in str_repr
        assert "H2O" in str_repr


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
