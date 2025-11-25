"""
Unit Tests for Stream Module
=============================

Tests for the Stream class and unit conversion utilities.

Author: Plant Simulation Software Project
Date: November 2025
"""

import pytest
from src.core.stream import Stream, UnitConversion
from src.core.component import create_water, create_methane, Component


class TestStreamBasics:
    """Test basic stream creation and validation."""
    
    def test_create_valid_stream(self):
        """Test creating a valid stream."""
        water = create_water()
        stream = Stream(
            name="Test",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0
        )
        assert stream.name == "Test"
        assert stream.temperature == 300
        assert stream.molar_flow == 10.0
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Stream(
                name="",
                temperature=300,
                pressure=101325
            )
    
    def test_zero_temperature_raises_error(self):
        """Test that zero temperature raises ValueError."""
        with pytest.raises(ValueError, match="Temperature must be positive"):
            Stream(
                name="Test",
                temperature=0,
                pressure=101325
            )
    
    def test_negative_temperature_raises_error(self):
        """Test that negative temperature raises ValueError."""
        with pytest.raises(ValueError, match="Temperature must be positive"):
            Stream(
                name="Test",
                temperature=-10,
                pressure=101325
            )
    
    def test_zero_pressure_raises_error(self):
        """Test that zero pressure raises ValueError."""
        with pytest.raises(ValueError, match="Pressure must be positive"):
            Stream(
                name="Test",
                temperature=300,
                pressure=0
            )
    
    def test_negative_flow_raises_error(self):
        """Test that negative flow raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Stream(
                name="Test",
                temperature=300,
                pressure=101325,
                molar_flow=-10
            )
    
    def test_mole_fractions_must_sum_to_one(self):
        """Test that mole fractions must sum to 1.0."""
        water = create_water()
        methane = create_methane()
        
        with pytest.raises(ValueError, match="must sum to 1.0"):
            Stream(
                name="Test",
                temperature=300,
                pressure=101325,
                components={'Water': water, 'Methane': methane},
                mole_fractions={'Water': 0.6, 'Methane': 0.6}  # Sum = 1.2
            )


class TestStreamProperties:
    """Test stream property calculations."""
    
    def test_molecular_weight_pure_component(self):
        """Test molecular weight for pure component."""
        water = create_water()
        stream = Stream(
            name="Pure Water",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0
        )
        mw = stream.molecular_weight()
        assert abs(mw - 18.015) < 0.001
    
    def test_molecular_weight_mixture(self):
        """Test molecular weight for mixture."""
        water = create_water()
        methane = create_methane()
        stream = Stream(
            name="Mixture",
            temperature=300,
            pressure=101325,
            components={'Water': water, 'Methane': methane},
            mole_fractions={'Water': 0.5, 'Methane': 0.5},
            molar_flow=10.0
        )
        # MW = 0.5*18.015 + 0.5*16.043 = 17.029
        mw = stream.molecular_weight()
        expected = 0.5 * 18.015 + 0.5 * 16.043
        assert abs(mw - expected) < 0.001
    
    def test_mass_flow(self):
        """Test mass flow calculation."""
        water = create_water()
        stream = Stream(
            name="Water",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0  # kmol/s
        )
        # mass_flow = 10.0 * 18.015 = 180.15 kg/s
        mass_flow = stream.mass_flow()
        expected = 10.0 * 18.015
        assert abs(mass_flow - expected) < 0.001
    
    def test_component_molar_flows(self):
        """Test individual component molar flows."""
        water = create_water()
        methane = create_methane()
        stream = Stream(
            name="Mixture",
            temperature=300,
            pressure=101325,
            components={'Water': water, 'Methane': methane},
            mole_fractions={'Water': 0.6, 'Methane': 0.4},
            molar_flow=100.0
        )
        comp_flows = stream.component_molar_flows()
        assert abs(comp_flows['Water'] - 60.0) < 0.001
        assert abs(comp_flows['Methane'] - 40.0) < 0.001
    
    def test_component_mass_flows(self):
        """Test individual component mass flows."""
        water = create_water()
        methane = create_methane()
        stream = Stream(
            name="Mixture",
            temperature=300,
            pressure=101325,
            components={'Water': water, 'Methane': methane},
            mole_fractions={'Water': 0.6, 'Methane': 0.4},
            molar_flow=100.0
        )
        mass_flows = stream.component_mass_flows()
        # Water: 60 kmol/s * 18.015 kg/kmol
        # Methane: 40 kmol/s * 16.043 kg/kmol
        assert abs(mass_flows['Water'] - 60 * 18.015) < 0.1
        assert abs(mass_flows['Methane'] - 40 * 16.043) < 0.1
    
    def test_mass_fractions(self):
        """Test conversion from mole to mass fractions."""
        water = create_water()
        methane = create_methane()
        stream = Stream(
            name="Mixture",
            temperature=300,
            pressure=101325,
            components={'Water': water, 'Methane': methane},
            mole_fractions={'Water': 0.5, 'Methane': 0.5},
            molar_flow=100.0
        )
        mass_fracs = stream.mass_fractions()
        
        # Should sum to 1.0
        total = sum(mass_fracs.values())
        assert abs(total - 1.0) < 0.001
        
        # Water mass fraction should be higher (heavier molecule)
        assert mass_fracs['Water'] > mass_fracs['Methane']
    
    def test_ideal_gas_density(self):
        """Test ideal gas density calculation."""
        methane = create_methane()
        stream = Stream(
            name="Methane Gas",
            temperature=300,  # K
            pressure=101325,  # Pa
            components={'Methane': methane},
            mole_fractions={'Methane': 1.0},
            molar_flow=10.0
        )
        density = stream.ideal_gas_density()
        # ρ = P*MW/(R*T) = 101325 * 16.043 / (8314.46 * 300)
        expected = (101325 * 16.043) / (8314.46 * 300)
        assert abs(density - expected) < 0.001


class TestStreamOperations:
    """Test stream operations like mixing and splitting."""
    
    def test_copy_stream(self):
        """Test stream copying."""
        water = create_water()
        original = Stream(
            name="Original",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0
        )
        copy = original.copy()
        
        assert copy.name == "Original_copy"
        assert copy.temperature == original.temperature
        assert copy.molar_flow == original.molar_flow
        
        # Modify copy shouldn't affect original
        copy.temperature = 350
        assert original.temperature == 300
    
    def test_mix_two_streams(self):
        """Test mixing two streams."""
        water = create_water()
        methane = create_methane()
        
        stream1 = Stream(
            name="S1",
            temperature=300,
            pressure=200000,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0
        )
        
        stream2 = Stream(
            name="S2",
            temperature=350,
            pressure=150000,
            components={'Methane': methane},
            mole_fractions={'Methane': 1.0},
            molar_flow=20.0
        )
        
        mixed = stream1.mix_with(stream2)
        
        # Total flow should be sum
        assert abs(mixed.molar_flow - 30.0) < 0.001
        
        # Pressure should be minimum
        assert mixed.pressure == 150000
        
        # Should have both components
        assert 'Water' in mixed.components
        assert 'Methane' in mixed.components
        
        # Check compositions
        assert abs(mixed.mole_fractions['Water'] - 10/30) < 0.001
        assert abs(mixed.mole_fractions['Methane'] - 20/30) < 0.001
    
    def test_split_stream(self):
        """Test splitting a stream."""
        water = create_water()
        original = Stream(
            name="Feed",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=100.0
        )
        
        split1 = original.split(0.7, "_top")
        split2 = original.split(0.3, "_bottom")
        
        # Check flows
        assert abs(split1.molar_flow - 70.0) < 0.001
        assert abs(split2.molar_flow - 30.0) < 0.001
        
        # Check that compositions are same
        assert split1.mole_fractions == original.mole_fractions
        assert split2.mole_fractions == original.mole_fractions
        
        # Check that temperature and pressure are same
        assert split1.temperature == original.temperature
        assert split2.temperature == original.temperature
    
    def test_split_invalid_fraction_raises_error(self):
        """Test that invalid split fraction raises error."""
        water = create_water()
        stream = Stream(
            name="Feed",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=100.0
        )
        
        with pytest.raises(ValueError, match="between 0 and 1"):
            stream.split(1.5)
        
        with pytest.raises(ValueError, match="between 0 and 1"):
            stream.split(-0.1)


class TestUnitConversion:
    """Test unit conversion utilities."""
    
    def test_celsius_to_kelvin(self):
        """Test Celsius to Kelvin conversion."""
        assert UnitConversion.celsius_to_kelvin(0) == 273.15
        assert UnitConversion.celsius_to_kelvin(100) == 373.15
        assert abs(UnitConversion.celsius_to_kelvin(25) - 298.15) < 0.01
    
    def test_kelvin_to_celsius(self):
        """Test Kelvin to Celsius conversion."""
        assert UnitConversion.kelvin_to_celsius(273.15) == 0
        assert UnitConversion.kelvin_to_celsius(373.15) == 100
        assert abs(UnitConversion.kelvin_to_celsius(298.15) - 25) < 0.01
    
    def test_fahrenheit_to_kelvin(self):
        """Test Fahrenheit to Kelvin conversion."""
        assert abs(UnitConversion.fahrenheit_to_kelvin(32) - 273.15) < 0.01
        assert abs(UnitConversion.fahrenheit_to_kelvin(212) - 373.15) < 0.01
    
    def test_bar_to_pascal(self):
        """Test bar to Pascal conversion."""
        assert UnitConversion.bar_to_pascal(1) == 1e5
        assert UnitConversion.bar_to_pascal(10) == 1e6
    
    def test_pascal_to_bar(self):
        """Test Pascal to bar conversion."""
        assert UnitConversion.pascal_to_bar(1e5) == 1
        assert UnitConversion.pascal_to_bar(1e6) == 10
    
    def test_psi_to_pascal(self):
        """Test psi to Pascal conversion."""
        p_pa = UnitConversion.psi_to_pascal(14.7)
        # 14.7 psi ≈ 101325 Pa (1 atm)
        assert abs(p_pa - 101325) < 1000
    
    def test_atm_to_pascal(self):
        """Test atm to Pascal conversion."""
        assert UnitConversion.atm_to_pascal(1) == 101325
        assert UnitConversion.atm_to_pascal(2) == 202650
    
    def test_flow_rate_conversions(self):
        """Test flow rate unit conversions."""
        assert UnitConversion.kmol_s_to_kmol_h(1) == 3600
        assert UnitConversion.kmol_h_to_kmol_s(3600) == 1


class TestStreamSummary:
    """Test stream summary and string representations."""
    
    def test_repr(self):
        """Test __repr__ method."""
        water = create_water()
        stream = Stream(
            name="Test",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0
        )
        repr_str = repr(stream)
        assert "Stream" in repr_str
        assert "Test" in repr_str
    
    def test_str(self):
        """Test __str__ method."""
        water = create_water()
        stream = Stream(
            name="Test",
            temperature=300,
            pressure=101325,
            components={'Water': water},
            mole_fractions={'Water': 1.0},
            molar_flow=10.0
        )
        str_repr = str(stream)
        assert "Test" in str_repr
        assert "300" in str_repr
    
    def test_summary(self):
        """Test summary method."""
        water = create_water()
        methane = create_methane()
        stream = Stream(
            name="Mixed",
            temperature=300,
            pressure=101325,
            components={'Water': water, 'Methane': methane},
            mole_fractions={'Water': 0.6, 'Methane': 0.4},
            molar_flow=100.0
        )
        summary = stream.summary()
        
        # Check that key information is present
        assert "Mixed" in summary
        assert "300" in summary
        assert "Water" in summary
        assert "Methane" in summary
        assert "0.6" in summary or "0.60" in summary


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
