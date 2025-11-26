"""
Unit Tests for Dimensional Analysis Module (dimanal)
"""

import pytest
import math

# Import from the correct location in the project structure
from src.dimanal.dim import (
    Prefix, KILO, MILLI, MICRO, NANO, MEGA, GIGA, CENTI,
    KIBI, MEBI, GIBI, SI_PREFIXES, BINARY_PREFIXES,
    Dimension, DIMENSIONLESS, LENGTH, MASS, TIME, TEMPERATURE,
    AREA, VOLUME, VELOCITY, ACCELERATION, FORCE, ENERGY, POWER, PRESSURE, FREQUENCY,
    Unit, METER, KILOGRAM, GRAM, SECOND, MINUTE, HOUR, DAY,
    KELVIN, CELSIUS, FAHRENHEIT, RANKINE,
    MOLE, AMPERE, RADIAN, DEGREE,
    INCH, FOOT, YARD, MILE, NAUTICAL_MILE, FATHOM,
    POUND, OUNCE, GRAIN, TROY_OUNCE,
    LITER, GALLON_US, GALLON_UK, CUBIC_METER, CUBIC_FOOT,
    NEWTON, POUND_FORCE,
    PASCAL, BAR, ATMOSPHERE, PSI, TORR, MMHG,
    JOULE, CALORIE, BTU, ELECTRONVOLT, WATT_HOUR,
    WATT, HORSEPOWER, HORSEPOWER_METRIC,
    HERTZ, RPM,
    AMPERE_HOUR,
    SQUARE_METER, ACRE, HECTARE,
    METER_PER_SECOND, KILOMETER_PER_HOUR, MILE_PER_HOUR, KNOT,
    POISE, CENTIPOISE, STOKES, PASCAL_SECOND, SQUARE_METER_PER_SECOND,
    BIT, BYTE,
    LIGHT_YEAR_LEN, PARSEC_LEN, ASTRONOMICAL_UNIT_LEN,
    DALTON, ELECTRON_MASS_UNIT,
    METER_PER_SECOND_SQ,
    Quantity, DimensionError, UnitError,
    Q, convert, get_unit, UnitRegistry,
    STANDARD_GRAVITY, STANDARD_ATMOSPHERE, SPEED_OF_LIGHT,
    AVOGADRO_NUMBER, BOLTZMANN_CONSTANT,
)


class TestPrefix:
    def test_si_prefix_values(self):
        assert KILO.factor == 1e3
        assert MEGA.factor == 1e6
        assert MILLI.factor == 1e-3
        assert MICRO.factor == 1e-6
        assert NANO.factor == 1e-9

    def test_binary_prefix_values(self):
        assert KIBI.factor == 1024
        assert MEBI.factor == 1024**2
        assert GIBI.factor == 1024**3


class TestDimension:
    def test_dimensionless(self):
        assert DIMENSIONLESS.is_dimensionless
        assert not LENGTH.is_dimensionless

    def test_dimension_multiplication(self):
        assert VELOCITY * TIME == LENGTH
        assert LENGTH * LENGTH == AREA
        assert MASS * ACCELERATION == FORCE

    def test_dimension_division(self):
        assert LENGTH / TIME == VELOCITY
        assert ENERGY / TIME == POWER
        assert FORCE / AREA == PRESSURE

    def test_dimension_power(self):
        assert LENGTH ** 2 == AREA
        assert LENGTH ** 3 == VOLUME


class TestUnit:
    def test_unit_with_prefix(self):
        km = METER.with_prefix(KILO)
        assert km.symbol == "km"
        assert km.to_si == 1000.0

        mm = METER.with_prefix(MILLI)
        assert mm.symbol == "mm"
        assert mm.to_si == 0.001

    def test_unit_to_si_value(self):
        assert METER.to_si_value(5.0) == 5.0
        assert FOOT.to_si_value(1.0) == pytest.approx(0.3048)
        assert CELSIUS.to_si_value(0) == pytest.approx(273.15)

    def test_unit_convert_to(self):
        assert FOOT.convert_to(1.0, INCH) == pytest.approx(12.0)
        assert MILE.convert_to(1.0, FOOT) == pytest.approx(5280.0)

    def test_unit_convert_dimension_mismatch(self):
        with pytest.raises(DimensionError):
            METER.convert_to(1.0, KILOGRAM)

    def test_unit_multiplication(self):
        m_squared = METER * METER
        assert m_squared.dimension == AREA

    def test_unit_division(self):
        m_per_s = METER / SECOND
        assert m_per_s.dimension == VELOCITY


class TestQuantity:
    def test_quantity_conversion(self):
        q = Quantity(1.0, MILE)
        q_ft = q.to(FOOT)
        assert q_ft.value == pytest.approx(5280.0)

    def test_quantity_addition(self):
        q1 = Quantity(1.0, METER)
        q2 = Quantity(50.0, METER.with_prefix(CENTI))
        result = q1 + q2
        assert result.value == pytest.approx(1.5)

    def test_quantity_addition_dimension_mismatch(self):
        with pytest.raises(DimensionError):
            Quantity(1.0, METER) + Quantity(1.0, SECOND)

    def test_quantity_multiplication(self):
        length = Quantity(5.0, METER)
        width = Quantity(3.0, METER)
        area = length * width
        assert area.dimension == AREA
        assert area.value == pytest.approx(15.0)

    def test_quantity_division(self):
        distance = Quantity(100, METER)
        time = Quantity(10, SECOND)
        speed = distance / time
        assert speed.dimension == VELOCITY
        assert speed.value == pytest.approx(10.0)

    def test_quantity_comparison(self):
        q1 = Quantity(1.0, MILE)
        q2 = Quantity(5280.0, FOOT)
        assert q1 == q2


class TestTemperature:
    def test_celsius_kelvin(self):
        assert convert(0, CELSIUS, KELVIN) == pytest.approx(273.15)
        assert convert(100, CELSIUS, KELVIN) == pytest.approx(373.15)
        assert convert(273.15, KELVIN, CELSIUS) == pytest.approx(0.0)

    def test_fahrenheit_celsius(self):
        assert convert(32, FAHRENHEIT, CELSIUS) == pytest.approx(0.0)
        assert convert(212, FAHRENHEIT, CELSIUS) == pytest.approx(100.0)
        assert convert(-40, FAHRENHEIT, CELSIUS) == pytest.approx(-40.0)

    def test_celsius_fahrenheit(self):
        assert convert(0, CELSIUS, FAHRENHEIT) == pytest.approx(32.0)
        assert convert(100, CELSIUS, FAHRENHEIT) == pytest.approx(212.0)


class TestConversions:
    def test_length(self):
        assert convert(1, MILE, FOOT) == pytest.approx(5280.0)
        assert convert(1, YARD, INCH) == pytest.approx(36.0)
        assert convert(1, NAUTICAL_MILE, METER) == pytest.approx(1852.0)
        assert convert(1, FATHOM, FOOT) == pytest.approx(6.0)

    def test_mass(self):
        assert convert(1, POUND, OUNCE) == pytest.approx(16.0)
        assert convert(1, POUND, GRAIN) == pytest.approx(7000.0)
        assert convert(1, KILOGRAM, POUND) == pytest.approx(2.20462, rel=1e-4)

    def test_time(self):
        assert convert(1, HOUR, MINUTE) == pytest.approx(60.0)
        assert convert(1, DAY, SECOND) == pytest.approx(86400.0)

    def test_volume(self):
        assert convert(1, GALLON_US, LITER) == pytest.approx(3.78541, rel=1e-4)
        assert convert(1, CUBIC_FOOT, LITER) == pytest.approx(28.3168, rel=1e-4)

    def test_pressure(self):
        assert convert(1, ATMOSPHERE, PASCAL) == pytest.approx(101325.0)
        assert convert(1, ATMOSPHERE, BAR) == pytest.approx(1.01325)
        assert convert(1, ATMOSPHERE, PSI) == pytest.approx(14.696, rel=1e-3)
        assert convert(760, TORR, ATMOSPHERE) == pytest.approx(1.0, rel=1e-3)

    def test_energy(self):
        assert convert(1, CALORIE, JOULE) == pytest.approx(4.184)
        assert convert(1, BTU, JOULE) == pytest.approx(1055.06, rel=1e-3)
        assert convert(1, WATT_HOUR, JOULE) == pytest.approx(3600.0)

    def test_power(self):
        assert convert(1, HORSEPOWER, WATT) == pytest.approx(745.7, rel=1e-3)
        assert convert(1, HORSEPOWER_METRIC, WATT) == pytest.approx(735.5, rel=1e-3)

    def test_frequency(self):
        assert convert(60, RPM, HERTZ) == pytest.approx(1.0)

    def test_velocity(self):
        assert convert(1, KNOT, METER_PER_SECOND) == pytest.approx(0.5144, rel=1e-3)
        assert convert(100, KILOMETER_PER_HOUR, METER_PER_SECOND) == pytest.approx(27.778, rel=1e-3)

    def test_viscosity(self):
        assert convert(1, POISE, PASCAL_SECOND) == pytest.approx(0.1)
        assert convert(1, CENTIPOISE, PASCAL_SECOND) == pytest.approx(0.001)
        assert convert(1, STOKES, SQUARE_METER_PER_SECOND) == pytest.approx(1e-4)

    def test_area(self):
        assert convert(1, ACRE, SQUARE_METER) == pytest.approx(4046.86, rel=1e-4)
        assert convert(1, HECTARE, ACRE) == pytest.approx(2.47105, rel=1e-4)

    def test_angle(self):
        assert convert(180, DEGREE, RADIAN) == pytest.approx(math.pi)
        assert convert(math.pi, RADIAN, DEGREE) == pytest.approx(180.0)

    def test_information(self):
        assert convert(1, BYTE, BIT) == pytest.approx(8.0)


class TestHelperFunctions:
    def test_Q_function(self):
        q = Q(5.0, METER)
        assert q.value == 5.0
        assert q.unit == METER

    def test_convert_function(self):
        result = convert(1.0, MILE, METER)
        assert result == pytest.approx(1609.344)

    def test_get_unit(self):
        assert get_unit("m") == METER
        assert get_unit("meter") == METER
        with pytest.raises(UnitError):
            get_unit("nonexistent")


class TestRegistry:
    def test_registry_get(self):
        registry = UnitRegistry()
        assert registry.get("m") == METER
        assert registry.get("kg") == KILOGRAM

    def test_registry_contains(self):
        registry = UnitRegistry()
        assert "m" in registry
        assert "nonexistent" not in registry


class TestCompoundUnits:
    def test_velocity_calculation(self):
        dist = Quantity(100, METER)
        time = Quantity(10, SECOND)
        speed = dist / time
        assert speed.dimension == VELOCITY
        assert speed.value == pytest.approx(10.0)

    def test_force_calculation(self):
        mass = Quantity(10, KILOGRAM)
        accel = Quantity(9.8, METER_PER_SECOND_SQ)
        force = mass * accel
        assert force.dimension == FORCE
        assert force.value == pytest.approx(98.0)

    def test_energy_calculation(self):
        force = Quantity(100, NEWTON)
        dist = Quantity(5, METER)
        energy = force * dist
        assert energy.dimension == ENERGY
        assert energy.value == pytest.approx(500.0)


class TestPhysicalConstants:
    def test_speed_of_light(self):
        assert SPEED_OF_LIGHT == 299792458

    def test_standard_gravity(self):
        assert STANDARD_GRAVITY == 9.80665

    def test_standard_atmosphere(self):
        assert STANDARD_ATMOSPHERE == 101325

    def test_avogadro(self):
        assert AVOGADRO_NUMBER == pytest.approx(6.02214076e23, rel=1e-8)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
