"""
Dimensional Analysis Module (dimanal)
======================================

A comprehensive module for handling physical dimensions, units, and quantities
in chemical process engineering calculations.

This module includes:
- Proper SI prefix system (from quecto to quetta)
- Binary prefixes (kibi, mebi, gibi, etc.)
- Extensive collection of units from various systems
- Dimensional analysis and unit conversion

Author: Plant Simulation Software Project
Date: November 2025
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple, Callable
from enum import Enum
import math


# =============================================================================
# PHYSICAL CONSTANTS (CODATA 2018/2022)
# =============================================================================

SPEED_OF_LIGHT = 299792458  # m/s (exact)
PLANCK_CONSTANT = 6.62607015e-34  # J·s (exact)
REDUCED_PLANCK = 1.054571817e-34  # J·s (ℏ = h/2π)
ELEMENTARY_CHARGE = 1.602176634e-19  # C (exact)
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K (exact)
AVOGADRO_NUMBER = 6.02214076e23  # mol⁻¹ (exact)
GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/(kg·s²)
ELECTRON_MASS = 9.1093837015e-31  # kg
PROTON_MASS = 1.67262192369e-27  # kg
NEUTRON_MASS = 1.67492749804e-27  # kg
ATOMIC_MASS_UNIT = 1.66053906660e-27  # kg
BOHR_RADIUS = 5.29177210903e-11  # m
FINE_STRUCTURE_CONSTANT = 7.2973525693e-3
RYDBERG_CONSTANT = 10973731.568160  # m⁻¹
STEFAN_BOLTZMANN = 5.670374419e-8  # W/(m²·K⁴)
GAS_CONSTANT = 8.314462618  # J/(mol·K)
STANDARD_GRAVITY = 9.80665  # m/s² (exact)
STANDARD_ATMOSPHERE = 101325  # Pa (exact)
WIEN_DISPLACEMENT = 2.897771955e-3  # m·K
FARADAY_CONSTANT = 96485.33212  # C/mol
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m
VACUUM_PERMEABILITY = 1.25663706212e-6  # H/m
IMPEDANCE_OF_FREE_SPACE = 376.730313668  # Ω

# Astronomical
ASTRONOMICAL_UNIT = 149597870700  # m (exact)
LIGHT_YEAR = 9460730472580800  # m
PARSEC = 3.0856775814913673e16  # m
SOLAR_MASS = 1.98892e30  # kg
EARTH_MASS = 5.9722e24  # kg
EARTH_RADIUS_EQUATORIAL = 6378137  # m
LUNAR_MASS = 7.342e22  # kg
JUPITER_MASS = 1.898e27  # kg
SOLAR_RADIUS = 6.96e8  # m
LUNAR_DISTANCE_AVG = 3.844e8  # m


# =============================================================================
# SI PREFIXES
# =============================================================================

@dataclass(frozen=True)
class Prefix:
    """Represents a metric or binary prefix."""
    name: str
    symbol: str
    factor: float
    base: int = 10
    exponent: int = 0
    
    def __str__(self) -> str:
        return self.symbol
    
    def __repr__(self) -> str:
        return f"Prefix({self.name}, {self.symbol}, 10^{self.exponent})"


# SI Prefixes (powers of 10)
QUETTA = Prefix("quetta", "Q", 1e30, 10, 30)
RONNA = Prefix("ronna", "R", 1e27, 10, 27)
YOTTA = Prefix("yotta", "Y", 1e24, 10, 24)
ZETTA = Prefix("zetta", "Z", 1e21, 10, 21)
EXA = Prefix("exa", "E", 1e18, 10, 18)
PETA = Prefix("peta", "P", 1e15, 10, 15)
TERA = Prefix("tera", "T", 1e12, 10, 12)
GIGA = Prefix("giga", "G", 1e9, 10, 9)
MEGA = Prefix("mega", "M", 1e6, 10, 6)
KILO = Prefix("kilo", "k", 1e3, 10, 3)
HECTO = Prefix("hecto", "h", 1e2, 10, 2)
DECA = Prefix("deca", "da", 1e1, 10, 1)
NO_PREFIX = Prefix("", "", 1.0, 10, 0)
DECI = Prefix("deci", "d", 1e-1, 10, -1)
CENTI = Prefix("centi", "c", 1e-2, 10, -2)
MILLI = Prefix("milli", "m", 1e-3, 10, -3)
MICRO = Prefix("micro", "μ", 1e-6, 10, -6)
NANO = Prefix("nano", "n", 1e-9, 10, -9)
PICO = Prefix("pico", "p", 1e-12, 10, -12)
FEMTO = Prefix("femto", "f", 1e-15, 10, -15)
ATTO = Prefix("atto", "a", 1e-18, 10, -18)
ZEPTO = Prefix("zepto", "z", 1e-21, 10, -21)
YOCTO = Prefix("yocto", "y", 1e-24, 10, -24)
RONTO = Prefix("ronto", "r", 1e-27, 10, -27)
QUECTO = Prefix("quecto", "q", 1e-30, 10, -30)

# Binary Prefixes (IEC)
KIBI = Prefix("kibi", "Ki", 2**10, 2, 10)
MEBI = Prefix("mebi", "Mi", 2**20, 2, 20)
GIBI = Prefix("gibi", "Gi", 2**30, 2, 30)
TEBI = Prefix("tebi", "Ti", 2**40, 2, 40)
PEBI = Prefix("pebi", "Pi", 2**50, 2, 50)
EXBI = Prefix("exbi", "Ei", 2**60, 2, 60)
ZEBI = Prefix("zebi", "Zi", 2**70, 2, 70)
YOBI = Prefix("yobi", "Yi", 2**80, 2, 80)

SI_PREFIXES = [
    QUETTA, RONNA, YOTTA, ZETTA, EXA, PETA, TERA, GIGA, MEGA, KILO,
    HECTO, DECA, DECI, CENTI, MILLI, MICRO, NANO, PICO,
    FEMTO, ATTO, ZEPTO, YOCTO, RONTO, QUECTO
]

BINARY_PREFIXES = [KIBI, MEBI, GIBI, TEBI, PEBI, EXBI, ZEBI, YOBI]

SI_PREFIX_BY_SYMBOL = {p.symbol: p for p in SI_PREFIXES if p.symbol}
SI_PREFIX_BY_NAME = {p.name: p for p in SI_PREFIXES if p.name}


# =============================================================================
# DIMENSION CLASS
# =============================================================================

@dataclass(frozen=True)
class Dimension:
    """
    Represents a physical dimension as a combination of base dimensions.
    
    Base dimensions: Length, Mass, Time, Temperature, Amount, Current, 
    Luminosity, Angle, Solid Angle, Information
    """
    length: int = 0
    mass: int = 0
    time: int = 0
    temperature: int = 0
    amount: int = 0
    current: int = 0
    luminosity: int = 0
    angle: int = 0
    solid_angle: int = 0
    information: int = 0
    name: str = ""
    
    @property
    def is_dimensionless(self) -> bool:
        return all(exp == 0 for exp in self._exponents)
    
    @property
    def _exponents(self) -> Tuple[int, ...]:
        return (self.length, self.mass, self.time, self.temperature,
                self.amount, self.current, self.luminosity,
                self.angle, self.solid_angle, self.information)
    
    def __mul__(self, other: Dimension) -> Dimension:
        return Dimension(
            self.length + other.length, self.mass + other.mass,
            self.time + other.time, self.temperature + other.temperature,
            self.amount + other.amount, self.current + other.current,
            self.luminosity + other.luminosity, self.angle + other.angle,
            self.solid_angle + other.solid_angle, self.information + other.information
        )
    
    def __truediv__(self, other: Dimension) -> Dimension:
        return Dimension(
            self.length - other.length, self.mass - other.mass,
            self.time - other.time, self.temperature - other.temperature,
            self.amount - other.amount, self.current - other.current,
            self.luminosity - other.luminosity, self.angle - other.angle,
            self.solid_angle - other.solid_angle, self.information - other.information
        )
    
    def __pow__(self, power: int) -> Dimension:
        return Dimension(
            self.length * power, self.mass * power, self.time * power,
            self.temperature * power, self.amount * power, self.current * power,
            self.luminosity * power, self.angle * power,
            self.solid_angle * power, self.information * power
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dimension):
            return False
        return self._exponents == other._exponents
    
    def __hash__(self) -> int:
        return hash(self._exponents)
    
    def __str__(self) -> str:
        if self.name:
            return self.name
        if self.is_dimensionless:
            return "dimensionless"
        parts = []
        symbols = [("L", self.length), ("M", self.mass), ("T", self.time),
                   ("Θ", self.temperature), ("N", self.amount), ("I", self.current),
                   ("J", self.luminosity), ("A", self.angle), ("Ω", self.solid_angle),
                   ("B", self.information)]
        for symbol, exp in symbols:
            if exp == 1:
                parts.append(symbol)
            elif exp != 0:
                parts.append(f"{symbol}^{exp}")
        return "·".join(parts) if parts else "1"
    
    def __repr__(self) -> str:
        return f"Dimension({self})"


# =============================================================================
# PREDEFINED DIMENSIONS
# =============================================================================

# Base
DIMENSIONLESS = Dimension(name="Dimensionless")
LENGTH = Dimension(length=1, name="Length")
MASS = Dimension(mass=1, name="Mass")
TIME = Dimension(time=1, name="Time")
TEMPERATURE = Dimension(temperature=1, name="Temperature")
AMOUNT = Dimension(amount=1, name="Amount")
ELECTRIC_CURRENT = Dimension(current=1, name="Electric Current")
LUMINOUS_INTENSITY = Dimension(luminosity=1, name="Luminous Intensity")
PLANE_ANGLE = Dimension(angle=1, name="Plane Angle")
SOLID_ANGLE_DIM = Dimension(solid_angle=1, name="Solid Angle")
INFORMATION_DIM = Dimension(information=1, name="Information")

# Geometric
AREA = Dimension(length=2, name="Area")
VOLUME = Dimension(length=3, name="Volume")
WAVENUMBER = Dimension(length=-1, name="Wavenumber")

# Mechanical
VELOCITY = Dimension(length=1, time=-1, name="Velocity")
ACCELERATION = Dimension(length=1, time=-2, name="Acceleration")
JERK = Dimension(length=1, time=-3, name="Jerk")
FORCE = Dimension(mass=1, length=1, time=-2, name="Force")
MOMENTUM = Dimension(mass=1, length=1, time=-1, name="Momentum")
ANGULAR_MOMENTUM = Dimension(mass=1, length=2, time=-1, name="Angular Momentum")
TORQUE = Dimension(mass=1, length=2, time=-2, name="Torque")
ENERGY = Dimension(mass=1, length=2, time=-2, name="Energy")
POWER = Dimension(mass=1, length=2, time=-3, name="Power")
PRESSURE = Dimension(mass=1, length=-1, time=-2, name="Pressure")
DENSITY = Dimension(mass=1, length=-3, name="Density")
SPECIFIC_VOLUME = Dimension(mass=-1, length=3, name="Specific Volume")
LINEAR_DENSITY = Dimension(mass=1, length=-1, name="Linear Density")
SURFACE_DENSITY = Dimension(mass=1, length=-2, name="Surface Density")
DYNAMIC_VISCOSITY = Dimension(mass=1, length=-1, time=-1, name="Dynamic Viscosity")
KINEMATIC_VISCOSITY = Dimension(length=2, time=-1, name="Kinematic Viscosity")
SURFACE_TENSION = Dimension(mass=1, time=-2, name="Surface Tension")
ACTION = Dimension(mass=1, length=2, time=-1, name="Action")

# Frequency
FREQUENCY = Dimension(time=-1, name="Frequency")
ANGULAR_VELOCITY = Dimension(angle=1, time=-1, name="Angular Velocity")
RADIOACTIVITY = Dimension(time=-1, name="Radioactivity")

# Flow
MASS_FLOW = Dimension(mass=1, time=-1, name="Mass Flow Rate")
VOLUMETRIC_FLOW = Dimension(length=3, time=-1, name="Volumetric Flow Rate")
MOLAR_FLOW = Dimension(amount=1, time=-1, name="Molar Flow Rate")
MASS_FLUX = Dimension(mass=1, length=-2, time=-1, name="Mass Flux")
HEAT_FLUX = Dimension(mass=1, time=-3, name="Heat Flux")

# Thermodynamic
HEAT_CAPACITY = Dimension(mass=1, length=2, time=-2, temperature=-1, name="Heat Capacity")
SPECIFIC_HEAT = Dimension(length=2, time=-2, temperature=-1, name="Specific Heat")
MOLAR_HEAT_CAPACITY = Dimension(mass=1, length=2, time=-2, temperature=-1, amount=-1, name="Molar Heat Capacity")
ENTROPY = Dimension(mass=1, length=2, time=-2, temperature=-1, name="Entropy")
THERMAL_CONDUCTIVITY = Dimension(mass=1, length=1, time=-3, temperature=-1, name="Thermal Conductivity")
HEAT_TRANSFER_COEFF = Dimension(mass=1, time=-3, temperature=-1, name="Heat Transfer Coefficient")

# Chemical
MOLAR_MASS = Dimension(mass=1, amount=-1, name="Molar Mass")
MOLAR_VOLUME = Dimension(length=3, amount=-1, name="Molar Volume")
MOLAR_ENERGY = Dimension(mass=1, length=2, time=-2, amount=-1, name="Molar Energy")
CONCENTRATION = Dimension(amount=1, length=-3, name="Concentration")
MOLALITY = Dimension(amount=1, mass=-1, name="Molality")
CATALYTIC_ACTIVITY = Dimension(amount=1, time=-1, name="Catalytic Activity")

# Electrical
ELECTRIC_CHARGE = Dimension(current=1, time=1, name="Electric Charge")
VOLTAGE = Dimension(mass=1, length=2, time=-3, current=-1, name="Voltage")
CAPACITANCE = Dimension(mass=-1, length=-2, time=4, current=2, name="Capacitance")
RESISTANCE = Dimension(mass=1, length=2, time=-3, current=-2, name="Resistance")
CONDUCTANCE = Dimension(mass=-1, length=-2, time=3, current=2, name="Conductance")
INDUCTANCE = Dimension(mass=1, length=2, time=-2, current=-2, name="Inductance")
MAGNETIC_FLUX = Dimension(mass=1, length=2, time=-2, current=-1, name="Magnetic Flux")
MAGNETIC_FLUX_DENSITY = Dimension(mass=1, time=-2, current=-1, name="Magnetic Flux Density")
MAGNETIC_FIELD_STRENGTH = Dimension(current=1, length=-1, name="Magnetic Field Strength")
PERMITTIVITY = Dimension(mass=-1, length=-3, time=4, current=2, name="Permittivity")
PERMEABILITY = Dimension(mass=1, length=1, time=-2, current=-2, name="Permeability")
ELECTRIC_FIELD = Dimension(mass=1, length=1, time=-3, current=-1, name="Electric Field")

# Optical
LUMINOUS_FLUX = Dimension(luminosity=1, solid_angle=1, name="Luminous Flux")
ILLUMINANCE = Dimension(luminosity=1, solid_angle=1, length=-2, name="Illuminance")
LUMINANCE = Dimension(luminosity=1, length=-2, name="Luminance")
IRRADIANCE = Dimension(mass=1, time=-3, name="Irradiance")

# Nuclear
ABSORBED_DOSE = Dimension(length=2, time=-2, name="Absorbed Dose")
EQUIVALENT_DOSE = Dimension(length=2, time=-2, name="Equivalent Dose")
EXPOSURE_RADIATION = Dimension(current=1, time=1, mass=-1, name="Radiation Exposure")

# Information
DATA_RATE = Dimension(information=1, time=-1, name="Data Rate")


# =============================================================================
# EXCEPTIONS
# =============================================================================

class DimensionError(Exception):
    """Raised for dimensional mismatches."""
    pass

class UnitError(Exception):
    """Raised for unit-related errors."""
    pass


# =============================================================================
# UNIT CLASS
# =============================================================================

@dataclass
class Unit:
    """Represents a unit of measurement."""
    name: str
    symbol: str
    dimension: Dimension
    to_si: float = 1.0
    offset: float = 0.0
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Unit name cannot be empty")
        if not self.symbol:
            raise ValueError("Unit symbol cannot be empty")
        if self.to_si <= 0:
            raise ValueError("Conversion factor must be positive")
    
    def with_prefix(self, prefix: Prefix) -> Unit:
        """Create a new unit with the given prefix."""
        return Unit(
            name=f"{prefix.name}{self.name}",
            symbol=f"{prefix.symbol}{self.symbol}",
            dimension=self.dimension,
            to_si=self.to_si * prefix.factor,
            offset=self.offset
        )
    
    def to_si_value(self, value: float) -> float:
        return value * self.to_si + self.offset
    
    def from_si_value(self, si_value: float) -> float:
        return (si_value - self.offset) / self.to_si
    
    def convert_to(self, value: float, target: Unit) -> float:
        if self.dimension != target.dimension:
            raise DimensionError(
                f"Cannot convert {self.name} ({self.dimension}) to "
                f"{target.name} ({target.dimension})"
            )
        return target.from_si_value(self.to_si_value(value))
    
    def __mul__(self, other: Unit) -> Unit:
        return Unit(f"{self.name}·{other.name}", f"{self.symbol}·{other.symbol}",
                    self.dimension * other.dimension, self.to_si * other.to_si)
    
    def __truediv__(self, other: Unit) -> Unit:
        return Unit(f"{self.name}/{other.name}", f"{self.symbol}/{other.symbol}",
                    self.dimension / other.dimension, self.to_si / other.to_si)
    
    def __pow__(self, power: int) -> Unit:
        if power == 1:
            return self
        return Unit(f"{self.name}^{power}", f"{self.symbol}^{power}",
                    self.dimension ** power, self.to_si ** power)
    
    def __str__(self) -> str:
        return self.symbol
    
    def __repr__(self) -> str:
        return f"Unit({self.name}, {self.symbol})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return False
        return (self.dimension == other.dimension and 
                abs(self.to_si - other.to_si) < 1e-15 and
                abs(self.offset - other.offset) < 1e-15)
    
    def __hash__(self) -> int:
        return hash((self.symbol, self.dimension, self.to_si, self.offset))


# =============================================================================
# QUANTITY CLASS
# =============================================================================

@dataclass
class Quantity:
    """A physical quantity: value + unit."""
    value: float
    unit: Unit
    
    def to(self, target_unit: Unit) -> Quantity:
        new_value = self.unit.convert_to(self.value, target_unit)
        return Quantity(new_value, target_unit)
    
    def to_si(self) -> Quantity:
        si_value = self.unit.to_si_value(self.value)
        si_unit = _get_si_unit(self.unit.dimension)
        return Quantity(si_value, si_unit)
    
    @property
    def dimension(self) -> Dimension:
        return self.unit.dimension
    
    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError(f"Cannot add Quantity and {type(other)}")
        if self.dimension != other.dimension:
            raise DimensionError(f"Cannot add {self.dimension} and {other.dimension}")
        return Quantity(self.value + other.to(self.unit).value, self.unit)
    
    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            raise TypeError(f"Cannot subtract Quantity and {type(other)}")
        if self.dimension != other.dimension:
            raise DimensionError(f"Cannot subtract {self.dimension} and {other.dimension}")
        return Quantity(self.value - other.to(self.unit).value, self.unit)
    
    def __mul__(self, other: Union[Quantity, float, int]) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        raise TypeError(f"Cannot multiply Quantity by {type(other)}")
    
    def __rmul__(self, other: Union[float, int]) -> Quantity:
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[Quantity, float, int]) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value / other, self.unit)
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        raise TypeError(f"Cannot divide Quantity by {type(other)}")
    
    def __pow__(self, power: int) -> Quantity:
        return Quantity(self.value ** power, self.unit ** power)
    
    def __neg__(self) -> Quantity:
        return Quantity(-self.value, self.unit)
    
    def __abs__(self) -> Quantity:
        return Quantity(abs(self.value), self.unit)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quantity):
            return False
        if self.dimension != other.dimension:
            return False
        return abs(self.to_si().value - other.to_si().value) < 1e-10
    
    def __lt__(self, other: Quantity) -> bool:
        if self.dimension != other.dimension:
            raise DimensionError("Cannot compare different dimensions")
        return self.to_si().value < other.to_si().value
    
    def __le__(self, other: Quantity) -> bool:
        return self == other or self < other
    
    def __gt__(self, other: Quantity) -> bool:
        if self.dimension != other.dimension:
            raise DimensionError("Cannot compare different dimensions")
        return self.to_si().value > other.to_si().value
    
    def __ge__(self, other: Quantity) -> bool:
        return self == other or self > other
    
    def __str__(self) -> str:
        return f"{self.value} {self.unit.symbol}"
    
    def __repr__(self) -> str:
        return f"Quantity({self.value}, {self.unit.symbol})"
    
    def __format__(self, format_spec: str) -> str:
        if format_spec:
            return f"{self.value:{format_spec}} {self.unit.symbol}"
        return str(self)


# =============================================================================
# BASE UNITS (SI and others - no prefixes)
# =============================================================================

# --- Dimensionless ---
UNITLESS = Unit("unitless", "-", DIMENSIONLESS, 1.0)
PERCENT = Unit("percent", "%", DIMENSIONLESS, 0.01)
PERMILLE = Unit("permille", "‰", DIMENSIONLESS, 0.001)
PPM = Unit("parts per million", "ppm", DIMENSIONLESS, 1e-6)
PPB = Unit("parts per billion", "ppb", DIMENSIONLESS, 1e-9)
PPT = Unit("parts per trillion", "ppt", DIMENSIONLESS, 1e-12)
BASIS_POINT = Unit("basis point", "bp", DIMENSIONLESS, 1e-4)

# --- Length (SI base: meter) ---
METER = Unit("meter", "m", LENGTH, 1.0)
ANGSTROM = Unit("angstrom", "Å", LENGTH, 1e-10)
FERMI = Unit("fermi", "fm", LENGTH, 1e-15)
BOHR_UNIT = Unit("bohr", "a₀", LENGTH, BOHR_RADIUS)
PLANCK_LENGTH = Unit("Planck length", "ℓP", LENGTH, 1.616255e-35)

# Imperial/US
INCH = Unit("inch", "in", LENGTH, 0.0254)
FOOT = Unit("foot", "ft", LENGTH, 0.3048)
YARD = Unit("yard", "yd", LENGTH, 0.9144)
MILE = Unit("mile", "mi", LENGTH, 1609.344)
NAUTICAL_MILE = Unit("nautical mile", "nmi", LENGTH, 1852.0)
FATHOM = Unit("fathom", "ftm", LENGTH, 1.8288)
CHAIN = Unit("chain", "ch", LENGTH, 20.1168)
FURLONG = Unit("furlong", "fur", LENGTH, 201.168)
LEAGUE = Unit("league", "lea", LENGTH, 4828.032)
ROD = Unit("rod", "rd", LENGTH, 5.0292)
LINK = Unit("link", "li", LENGTH, 0.201168)
THOU = Unit("thou", "th", LENGTH, 2.54e-5)
MIL = Unit("mil", "mil", LENGTH, 2.54e-5)
HAND = Unit("hand", "hh", LENGTH, 0.1016)
SPAN = Unit("span", "span", LENGTH, 0.2286)
CUBIT = Unit("cubit", "cubit", LENGTH, 0.4572)
ELL = Unit("ell", "ell", LENGTH, 1.143)
CABLE = Unit("cable", "cable", LENGTH, 185.2)
SHACKLE = Unit("shackle", "shackle", LENGTH, 27.432)

# Astronomical
ASTRONOMICAL_UNIT_LEN = Unit("astronomical unit", "AU", LENGTH, ASTRONOMICAL_UNIT)
LIGHT_YEAR_LEN = Unit("light-year", "ly", LENGTH, LIGHT_YEAR)
PARSEC_LEN = Unit("parsec", "pc", LENGTH, PARSEC)
LIGHT_SECOND = Unit("light-second", "ls", LENGTH, SPEED_OF_LIGHT)
LIGHT_MINUTE = Unit("light-minute", "lmin", LENGTH, SPEED_OF_LIGHT * 60)
SOLAR_RADIUS_LEN = Unit("solar radius", "R☉", LENGTH, SOLAR_RADIUS)
EARTH_RADIUS_LEN = Unit("earth radius", "R⊕", LENGTH, EARTH_RADIUS_EQUATORIAL)
LUNAR_DISTANCE = Unit("lunar distance", "LD", LENGTH, LUNAR_DISTANCE_AVG)

# Typographic
POINT = Unit("point", "pt", LENGTH, 0.0003527778)
PICA = Unit("pica", "pica", LENGTH, 0.004233333)
TWIP = Unit("twip", "twip", LENGTH, 1.7639e-5)
CICERO = Unit("cicero", "cc", LENGTH, 0.004512)
DIDOT = Unit("didot point", "dd", LENGTH, 0.000376)

# Historical/Regional
FRENCH_FOOT = Unit("French foot", "pied", LENGTH, 0.3248)
RUSSIAN_VERST = Unit("verst", "verst", LENGTH, 1066.8)
RUSSIAN_ARSHIN = Unit("arshin", "arshin", LENGTH, 0.7112)
ROMAN_MILE = Unit("Roman mile", "mp", LENGTH, 1479.5)
GREEK_STADION = Unit("stadion", "stadion", LENGTH, 185.0)
JAPANESE_SHAKU = Unit("shaku", "尺", LENGTH, 0.303030303)
JAPANESE_KEN = Unit("ken", "間", LENGTH, 1.818181818)
JAPANESE_RI = Unit("ri", "里", LENGTH, 3927.27)
CHINESE_LI = Unit("li", "里", LENGTH, 500.0)
CHINESE_CHI = Unit("chi", "尺", LENGTH, 0.333333)
INDIAN_YOJANA = Unit("yojana", "yojana", LENGTH, 12875.0)
GERMAN_MEILE = Unit("German mile", "Meile", LENGTH, 7532.5)
SCOTTISH_ELL = Unit("Scottish ell", "Sc ell", LENGTH, 0.941)

# Survey
US_SURVEY_FOOT = Unit("US survey foot", "ft_us", LENGTH, 0.3048006096)
US_SURVEY_MILE = Unit("US survey mile", "mi_us", LENGTH, 1609.3472187)

# --- Mass (SI base: kilogram) ---
KILOGRAM = Unit("kilogram", "kg", MASS, 1.0)
GRAM = Unit("gram", "g", MASS, 0.001)
TONNE = Unit("tonne", "t", MASS, 1000.0)

# Atomic
DALTON = Unit("dalton", "Da", MASS, ATOMIC_MASS_UNIT)
ATOMIC_MASS = Unit("atomic mass unit", "u", MASS, ATOMIC_MASS_UNIT)
ELECTRON_MASS_UNIT = Unit("electron mass", "mₑ", MASS, ELECTRON_MASS)
PLANCK_MASS = Unit("Planck mass", "mP", MASS, 2.176434e-8)

# Imperial/US
POUND = Unit("pound", "lb", MASS, 0.45359237)
OUNCE = Unit("ounce", "oz", MASS, 0.028349523125)
GRAIN = Unit("grain", "gr", MASS, 6.479891e-5)
DRAM = Unit("dram", "dr", MASS, 0.001771845195)
STONE = Unit("stone", "st", MASS, 6.35029318)
QUARTER_MASS = Unit("quarter", "qr", MASS, 12.70058636)
HUNDREDWEIGHT_LONG = Unit("long hundredweight", "cwt", MASS, 50.80234544)
HUNDREDWEIGHT_SHORT = Unit("short hundredweight", "cwt_s", MASS, 45.359237)
TON_LONG = Unit("long ton", "ton_l", MASS, 1016.0469088)
TON_SHORT = Unit("short ton", "ton_s", MASS, 907.18474)
SLUG = Unit("slug", "slug", MASS, 14.593903)

# Troy (precious metals)
TROY_OUNCE = Unit("troy ounce", "oz t", MASS, 0.0311034768)
TROY_POUND = Unit("troy pound", "lb t", MASS, 0.3732417216)
PENNYWEIGHT = Unit("pennyweight", "dwt", MASS, 0.00155517384)

# Apothecary
SCRUPLE = Unit("scruple", "℈", MASS, 0.0012959782)
APOTHECARY_DRAM = Unit("apothecary dram", "ʒ", MASS, 0.0038879346)
APOTHECARY_OUNCE = Unit("apothecary ounce", "℥", MASS, 0.0311034768)

# Astronomical
SOLAR_MASS_UNIT = Unit("solar mass", "M☉", MASS, SOLAR_MASS)
EARTH_MASS_UNIT = Unit("earth mass", "M⊕", MASS, EARTH_MASS)
JUPITER_MASS_UNIT = Unit("Jupiter mass", "MJ", MASS, JUPITER_MASS)
LUNAR_MASS_UNIT = Unit("lunar mass", "ML", MASS, LUNAR_MASS)

# Historical/Regional
CARAT = Unit("carat", "ct", MASS, 0.0002)
TALENT = Unit("talent", "talent", MASS, 26.0)
MINA = Unit("mina", "mina", MASS, 0.571)
SHEKEL = Unit("shekel", "shekel", MASS, 0.0114)
CHINESE_JIN = Unit("jin", "斤", MASS, 0.5)
CHINESE_LIANG = Unit("liang", "两", MASS, 0.0375)
JAPANESE_KAN = Unit("kan", "貫", MASS, 3.75)
JAPANESE_MOMME = Unit("momme", "匁", MASS, 0.00375)
INDIAN_TOLA = Unit("tola", "tola", MASS, 0.01166)
INDIAN_SEER = Unit("seer", "seer", MASS, 0.9331)
INDIAN_MAUND = Unit("maund", "maund", MASS, 37.324)
RUSSIAN_POOD = Unit("pood", "pood", MASS, 16.3805)
SPANISH_ARROBA = Unit("arroba", "arroba", MASS, 11.502)
QUINTAL = Unit("quintal", "q", MASS, 100.0)

# --- Time (SI base: second) ---
SECOND = Unit("second", "s", TIME, 1.0)
MINUTE = Unit("minute", "min", TIME, 60.0)
HOUR = Unit("hour", "h", TIME, 3600.0)
DAY = Unit("day", "d", TIME, 86400.0)
WEEK = Unit("week", "wk", TIME, 604800.0)
FORTNIGHT = Unit("fortnight", "fn", TIME, 1209600.0)
MONTH_30 = Unit("month (30 days)", "mo", TIME, 2592000.0)
MONTH_SYNODIC = Unit("synodic month", "mo_syn", TIME, 2551442.8)
YEAR_JULIAN = Unit("Julian year", "a", TIME, 31557600.0)
YEAR_GREGORIAN = Unit("Gregorian year", "yr", TIME, 31556952.0)
YEAR_TROPICAL = Unit("tropical year", "yr_trop", TIME, 31556925.445)
YEAR_SIDEREAL = Unit("sidereal year", "yr_sid", TIME, 31558149.7635)
DECADE = Unit("decade", "dec", TIME, 315576000.0)
CENTURY = Unit("century", "c", TIME, 3155760000.0)
MILLENNIUM = Unit("millennium", "ka", TIME, 31557600000.0)
SIDEREAL_DAY = Unit("sidereal day", "d_sid", TIME, 86164.0905)

# Atomic/Quantum
PLANCK_TIME = Unit("Planck time", "tP", TIME, 5.391247e-44)
ATOMIC_TIME = Unit("atomic time unit", "ℏ/Eh", TIME, 2.4188843265857e-17)
SHAKE = Unit("shake", "shake", TIME, 1e-8)
JIFFY_PHYSICS = Unit("jiffy (physics)", "jiffy", TIME, 3e-24)

# Historical
MOMENT = Unit("moment", "moment", TIME, 90.0)
HELEK = Unit("helek", "helek", TIME, 3.333)
GHATI = Unit("ghati", "ghati", TIME, 1440.0)
KE = Unit("ke", "刻", TIME, 864.0)

# --- Temperature (SI base: kelvin) ---
KELVIN = Unit("kelvin", "K", TEMPERATURE, 1.0, 0.0)
CELSIUS = Unit("celsius", "°C", TEMPERATURE, 1.0, 273.15)
FAHRENHEIT = Unit("fahrenheit", "°F", TEMPERATURE, 5/9, 273.15 - 32*5/9)
RANKINE = Unit("rankine", "°R", TEMPERATURE, 5/9, 0.0)
# Note: Delisle scale is inverted - requires special handling, not included here
NEWTON_TEMP = Unit("newton", "°N", TEMPERATURE, 100/33, 273.15)
REAUMUR = Unit("réaumur", "°Ré", TEMPERATURE, 5/4, 273.15)
ROMER = Unit("rømer", "°Rø", TEMPERATURE, 40/21, 273.15 - 7.5*40/21)

# --- Amount of Substance (SI base: mole) ---
MOLE = Unit("mole", "mol", AMOUNT, 1.0)
POUND_MOLE = Unit("pound-mole", "lb-mol", AMOUNT, 453.59237)

# --- Electric Current (SI base: ampere) ---
AMPERE = Unit("ampere", "A", ELECTRIC_CURRENT, 1.0)
BIOT = Unit("biot", "Bi", ELECTRIC_CURRENT, 10.0)
STATAMPERE = Unit("statampere", "statA", ELECTRIC_CURRENT, 3.335641e-10)
ABAMPERE = Unit("abampere", "abA", ELECTRIC_CURRENT, 10.0)

# --- Luminous Intensity (SI base: candela) ---
CANDELA = Unit("candela", "cd", LUMINOUS_INTENSITY, 1.0)
CANDLEPOWER = Unit("candlepower", "cp", LUMINOUS_INTENSITY, 0.981)
HEFNER = Unit("Hefner unit", "HK", LUMINOUS_INTENSITY, 0.903)
CARCEL = Unit("carcel", "carcel", LUMINOUS_INTENSITY, 9.74)

# --- Plane Angle (SI: radian) ---
RADIAN = Unit("radian", "rad", PLANE_ANGLE, 1.0)
DEGREE = Unit("degree", "°", PLANE_ANGLE, math.pi / 180)
ARCMINUTE = Unit("arcminute", "′", PLANE_ANGLE, math.pi / 10800)
ARCSECOND = Unit("arcsecond", "″", PLANE_ANGLE, math.pi / 648000)
GRADIAN = Unit("gradian", "gon", PLANE_ANGLE, math.pi / 200)
TURN = Unit("turn", "tr", PLANE_ANGLE, 2 * math.pi)
REVOLUTION = Unit("revolution", "rev", PLANE_ANGLE, 2 * math.pi)
QUADRANT = Unit("quadrant", "quad", PLANE_ANGLE, math.pi / 2)
SEXTANT = Unit("sextant", "sext", PLANE_ANGLE, math.pi / 3)
OCTANT = Unit("octant", "oct", PLANE_ANGLE, math.pi / 4)
SIGN = Unit("sign", "sign", PLANE_ANGLE, math.pi / 6)
HOUR_ANGLE = Unit("hour angle", "ha", PLANE_ANGLE, math.pi / 12)
COMPASS_POINT = Unit("compass point", "pt", PLANE_ANGLE, math.pi / 16)
MIL_NATO = Unit("mil (NATO)", "mil", PLANE_ANGLE, math.pi / 3200)
BINARY_DEGREE = Unit("binary degree", "brad", PLANE_ANGLE, math.pi / 128)

# --- Solid Angle (SI: steradian) ---
STERADIAN = Unit("steradian", "sr", SOLID_ANGLE_DIM, 1.0)
SQUARE_DEGREE = Unit("square degree", "deg²", SOLID_ANGLE_DIM, (math.pi / 180) ** 2)
SPAT = Unit("spat", "sp", SOLID_ANGLE_DIM, 4 * math.pi)

# --- Information (base: bit) ---
BIT = Unit("bit", "b", INFORMATION_DIM, 1.0)
BYTE = Unit("byte", "B", INFORMATION_DIM, 8.0)
NIBBLE = Unit("nibble", "nibble", INFORMATION_DIM, 4.0)
WORD = Unit("word", "word", INFORMATION_DIM, 32.0)  # 32-bit word
NAT = Unit("nat", "nat", INFORMATION_DIM, 1.442695)  # Natural unit
BAN = Unit("ban", "ban", INFORMATION_DIM, 3.321928)  # Hartley

# --- Area (derived: m²) ---
SQUARE_METER = Unit("square meter", "m²", AREA, 1.0)
HECTARE = Unit("hectare", "ha", AREA, 1e4)
ARE = Unit("are", "a", AREA, 100.0)
BARN = Unit("barn", "b", AREA, 1e-28)
SQUARE_INCH = Unit("square inch", "in²", AREA, 6.4516e-4)
SQUARE_FOOT = Unit("square foot", "ft²", AREA, 0.09290304)
SQUARE_YARD = Unit("square yard", "yd²", AREA, 0.83612736)
SQUARE_MILE = Unit("square mile", "mi²", AREA, 2589988.110336)
ACRE = Unit("acre", "ac", AREA, 4046.8564224)
ROOD = Unit("rood", "rood", AREA, 1011.7141056)
SQUARE_ROD = Unit("square rod", "rd²", AREA, 25.29285264)
CIRCULAR_MIL = Unit("circular mil", "cmil", AREA, 5.067075e-10)
SECTION = Unit("section", "section", AREA, 2589988.110336)
TOWNSHIP = Unit("township", "township", AREA, 93239571.972096)
HOMESTEAD = Unit("homestead", "homestead", AREA, 647497.027584)
MORGEN = Unit("morgen", "Mg", AREA, 8565.0)
STREMMA = Unit("stremma", "stremma", AREA, 1000.0)
DUNAM = Unit("dunam", "dunam", AREA, 1000.0)
MU_AREA = Unit("mu", "亩", AREA, 666.67)
TSUBO = Unit("tsubo", "坪", AREA, 3.30579)
PYEONG = Unit("pyeong", "평", AREA, 3.30579)
BIGHA = Unit("bigha", "bigha", AREA, 1618.7)
FEDDAN = Unit("feddan", "feddan", AREA, 4200.0)
CUERDA = Unit("cuerda", "cda", AREA, 3930.395625)

# --- Volume (derived: m³) ---
CUBIC_METER = Unit("cubic meter", "m³", VOLUME, 1.0)
LITER = Unit("liter", "L", VOLUME, 0.001)
STERE = Unit("stere", "st", VOLUME, 1.0)
LAMBDA_VOL = Unit("lambda", "λ", VOLUME, 1e-9)
CUBIC_INCH = Unit("cubic inch", "in³", VOLUME, 1.6387064e-5)
CUBIC_FOOT = Unit("cubic foot", "ft³", VOLUME, 0.028316846592)
CUBIC_YARD = Unit("cubic yard", "yd³", VOLUME, 0.764554857984)
GALLON_US = Unit("US gallon", "gal", VOLUME, 0.003785411784)
GALLON_UK = Unit("UK gallon", "gal_UK", VOLUME, 0.00454609)
QUART_US = Unit("US quart", "qt", VOLUME, 9.46352946e-4)
QUART_UK = Unit("UK quart", "qt_UK", VOLUME, 0.0011365225)
PINT_US = Unit("US pint", "pt", VOLUME, 4.73176473e-4)
PINT_UK = Unit("UK pint", "pt_UK", VOLUME, 5.6826125e-4)
CUP_US = Unit("US cup", "cup", VOLUME, 2.365882365e-4)
FLUID_OUNCE_US = Unit("US fluid ounce", "fl oz", VOLUME, 2.95735295625e-5)
FLUID_OUNCE_UK = Unit("UK fluid ounce", "fl oz_UK", VOLUME, 2.84130625e-5)
TABLESPOON = Unit("tablespoon", "tbsp", VOLUME, 1.47867647813e-5)
TEASPOON = Unit("teaspoon", "tsp", VOLUME, 4.92892159375e-6)
GILL_US = Unit("US gill", "gi", VOLUME, 1.1829411825e-4)
MINIM_US = Unit("US minim", "min", VOLUME, 6.1611519921875e-8)
FLUID_DRAM = Unit("fluid dram", "fl dr", VOLUME, 3.6966911953125e-6)
DROP = Unit("drop", "gtt", VOLUME, 5e-8)
BARREL_OIL = Unit("barrel (oil)", "bbl", VOLUME, 0.158987294928)
BARREL_US = Unit("barrel (US)", "bbl_US", VOLUME, 0.119240471196)
PECK = Unit("peck", "pk", VOLUME, 0.00880976754172)
BUSHEL_US = Unit("US bushel", "bu", VOLUME, 0.03523907016688)
BUSHEL_UK = Unit("UK bushel", "bu_UK", VOLUME, 0.03636872)
CORD = Unit("cord", "cord", VOLUME, 3.624556)
BOARD_FOOT = Unit("board foot", "fbm", VOLUME, 0.002359737)
ACRE_FOOT = Unit("acre-foot", "ac·ft", VOLUME, 1233.48183754752)
REGISTER_TON = Unit("register ton", "RT", VOLUME, 2.8316846592)
HOGSHEAD = Unit("hogshead", "hhd", VOLUME, 0.238480942392)
TUN = Unit("tun", "tun", VOLUME, 0.953923769568)
PIPE = Unit("pipe", "pipe", VOLUME, 0.476961884784)
BUTT = Unit("butt", "butt", VOLUME, 0.476961884784)
FIRKIN = Unit("firkin", "fir", VOLUME, 0.040914812)
JIGGER = Unit("jigger", "jig", VOLUME, 4.43603e-5)
WINE_BOTTLE = Unit("wine bottle", "bottle", VOLUME, 7.5e-4)
MAGNUM = Unit("magnum", "magnum", VOLUME, 1.5e-3)
GO_VOL = Unit("gō", "合", VOLUME, 1.8039e-4)
SHO = Unit("shō", "升", VOLUME, 1.8039e-3)
KOKU = Unit("koku", "石", VOLUME, 0.18039)

# --- Velocity (derived: m/s) ---
METER_PER_SECOND = Unit("meter per second", "m/s", VELOCITY, 1.0)
KILOMETER_PER_HOUR = Unit("kilometer per hour", "km/h", VELOCITY, 1/3.6)
MILE_PER_HOUR = Unit("mile per hour", "mph", VELOCITY, 0.44704)
FOOT_PER_SECOND = Unit("foot per second", "ft/s", VELOCITY, 0.3048)
KNOT = Unit("knot", "kn", VELOCITY, 0.514444)
MACH_SEA_LEVEL = Unit("Mach", "Ma", VELOCITY, 340.29)
SPEED_OF_LIGHT_UNIT = Unit("speed of light", "c", VELOCITY, SPEED_OF_LIGHT)
FURLONG_PER_FORTNIGHT = Unit("furlong per fortnight", "fur/fn", VELOCITY, 1.663095e-4)

# --- Acceleration (derived: m/s²) ---
METER_PER_SECOND_SQ = Unit("meter per second squared", "m/s²", ACCELERATION, 1.0)
STANDARD_GRAVITY_UNIT = Unit("standard gravity", "g₀", ACCELERATION, STANDARD_GRAVITY)
GAL = Unit("gal", "Gal", ACCELERATION, 0.01)
FOOT_PER_SECOND_SQ = Unit("foot per second squared", "ft/s²", ACCELERATION, 0.3048)

# --- Force (derived: newton) ---
NEWTON = Unit("newton", "N", FORCE, 1.0)
DYNE = Unit("dyne", "dyn", FORCE, 1e-5)
KILOGRAM_FORCE = Unit("kilogram-force", "kgf", FORCE, STANDARD_GRAVITY)
GRAM_FORCE = Unit("gram-force", "gf", FORCE, STANDARD_GRAVITY * 0.001)
TONNE_FORCE = Unit("tonne-force", "tf", FORCE, STANDARD_GRAVITY * 1000)
POND = Unit("pond", "p", FORCE, STANDARD_GRAVITY * 0.001)
KILOPOND = Unit("kilopond", "kp", FORCE, STANDARD_GRAVITY)
STHENE = Unit("sthène", "sn", FORCE, 1000.0)
POUND_FORCE = Unit("pound-force", "lbf", FORCE, 4.4482216152605)
OUNCE_FORCE = Unit("ounce-force", "ozf", FORCE, 0.27801385095378)
POUNDAL = Unit("poundal", "pdl", FORCE, 0.138254954376)
KIP = Unit("kip", "kip", FORCE, 4448.2216152605)

# --- Pressure (derived: pascal) ---
PASCAL = Unit("pascal", "Pa", PRESSURE, 1.0)
BAR = Unit("bar", "bar", PRESSURE, 1e5)
ATMOSPHERE = Unit("atmosphere", "atm", PRESSURE, STANDARD_ATMOSPHERE)
TECHNICAL_ATMOSPHERE = Unit("technical atmosphere", "at", PRESSURE, 98066.5)
PSI = Unit("pound per square inch", "psi", PRESSURE, 6894.757293168)
PSF = Unit("pound per square foot", "psf", PRESSURE, 47.88025898034)
TORR = Unit("torr", "Torr", PRESSURE, 133.32236842105)
MMHG = Unit("millimeter of mercury", "mmHg", PRESSURE, 133.322387415)
INHG = Unit("inch of mercury", "inHg", PRESSURE, 3386.389)
MMH2O = Unit("millimeter of water", "mmH₂O", PRESSURE, 9.80665)
CMH2O = Unit("centimeter of water", "cmH₂O", PRESSURE, 98.0665)
INH2O = Unit("inch of water", "inH₂O", PRESSURE, 249.08891)
FTH2O = Unit("foot of water", "ftH₂O", PRESSURE, 2989.0669)
BARYE = Unit("barye", "Ba", PRESSURE, 0.1)
PIEZE = Unit("pièze", "pz", PRESSURE, 1000.0)

# --- Energy (derived: joule) ---
JOULE = Unit("joule", "J", ENERGY, 1.0)
ERG = Unit("erg", "erg", ENERGY, 1e-7)
ELECTRONVOLT = Unit("electronvolt", "eV", ENERGY, ELEMENTARY_CHARGE)
CALORIE = Unit("calorie (thermochemical)", "cal", ENERGY, 4.184)
CALORIE_IT = Unit("calorie (IT)", "cal_IT", ENERGY, 4.1868)
CALORIE_15C = Unit("calorie (15°C)", "cal_15", ENERGY, 4.1855)
BTU = Unit("British thermal unit", "BTU", ENERGY, 1055.06)
BTU_IT = Unit("BTU (IT)", "BTU_IT", ENERGY, 1055.05585)
THERM = Unit("therm", "thm", ENERGY, 1.05506e8)
QUAD = Unit("quad", "quad", ENERGY, 1.05506e18)
WATT_HOUR = Unit("watt-hour", "Wh", ENERGY, 3600.0)
FOOT_POUND = Unit("foot-pound", "ft·lbf", ENERGY, 1.3558179483314)
FOOT_POUNDAL = Unit("foot-poundal", "ft·pdl", ENERGY, 0.04214011)
THERM_US = Unit("therm (US)", "thm_US", ENERGY, 1.054804e8)
TON_TNT = Unit("ton of TNT", "tTNT", ENERGY, 4.184e9)
HARTREE = Unit("hartree", "Eh", ENERGY, 4.3597447222071e-18)
RYDBERG_ENERGY = Unit("rydberg", "Ry", ENERGY, 2.1798723611035e-18)
BARREL_OIL_EQUIVALENT = Unit("barrel of oil equivalent", "boe", ENERGY, 6.1178632e9)
TONNE_OIL_EQUIVALENT = Unit("tonne of oil equivalent", "toe", ENERGY, 4.1868e10)
TONNE_COAL_EQUIVALENT = Unit("tonne of coal equivalent", "tce", ENERGY, 2.93076e10)
CUBIC_FOOT_NATURAL_GAS = Unit("cubic foot of natural gas", "cf_ng", ENERGY, 1.0551e6)

# --- Power (derived: watt) ---
WATT = Unit("watt", "W", POWER, 1.0)
HORSEPOWER = Unit("horsepower", "hp", POWER, 745.69987158227)
HORSEPOWER_METRIC = Unit("metric horsepower", "PS", POWER, 735.49875)
HORSEPOWER_BOILER = Unit("boiler horsepower", "hp_b", POWER, 9809.5)
HORSEPOWER_ELECTRIC = Unit("electric horsepower", "hp_e", POWER, 746.0)
BTU_PER_HOUR = Unit("BTU per hour", "BTU/h", POWER, 0.29307107)
TON_REFRIGERATION = Unit("ton of refrigeration", "TR", POWER, 3516.8528)
LUSEC = Unit("lusec", "lusec", POWER, 1.333e-4)
PONCELET = Unit("poncelet", "p", POWER, 980.665)

# --- Frequency (derived: hertz) ---
HERTZ = Unit("hertz", "Hz", FREQUENCY, 1.0)
RPM = Unit("revolutions per minute", "rpm", FREQUENCY, 1/60)
RPS = Unit("revolutions per second", "rps", FREQUENCY, 1.0)

# --- Electric Charge (derived: coulomb) ---
COULOMB = Unit("coulomb", "C", ELECTRIC_CHARGE, 1.0)
AMPERE_HOUR = Unit("ampere-hour", "Ah", ELECTRIC_CHARGE, 3600.0)
FARADAY = Unit("faraday", "F", ELECTRIC_CHARGE, FARADAY_CONSTANT)
STATCOULOMB = Unit("statcoulomb", "statC", ELECTRIC_CHARGE, 3.335641e-10)
ABCOULOMB = Unit("abcoulomb", "abC", ELECTRIC_CHARGE, 10.0)
FRANKLIN = Unit("franklin", "Fr", ELECTRIC_CHARGE, 3.335641e-10)

# --- Voltage (derived: volt) ---
VOLT = Unit("volt", "V", VOLTAGE, 1.0)
STATVOLT = Unit("statvolt", "statV", VOLTAGE, 299.792458)
ABVOLT = Unit("abvolt", "abV", VOLTAGE, 1e-8)

# --- Capacitance (derived: farad) ---
FARAD = Unit("farad", "F", CAPACITANCE, 1.0)
STATFARAD = Unit("statfarad", "statF", CAPACITANCE, 1.1126e-12)
ABFARAD = Unit("abfarad", "abF", CAPACITANCE, 1e9)

# --- Resistance (derived: ohm) ---
OHM = Unit("ohm", "Ω", RESISTANCE, 1.0)
STATOHM = Unit("statohm", "statΩ", RESISTANCE, 8.987552e11)
ABOHM = Unit("abohm", "abΩ", RESISTANCE, 1e-9)

# --- Conductance (derived: siemens) ---
SIEMENS = Unit("siemens", "S", CONDUCTANCE, 1.0)
MHO = Unit("mho", "℧", CONDUCTANCE, 1.0)

# --- Inductance (derived: henry) ---
HENRY = Unit("henry", "H", INDUCTANCE, 1.0)
STATHENRY = Unit("stathenry", "statH", INDUCTANCE, 8.987552e11)
ABHENRY = Unit("abhenry", "abH", INDUCTANCE, 1e-9)

# --- Magnetic Flux (derived: weber) ---
WEBER = Unit("weber", "Wb", MAGNETIC_FLUX, 1.0)
MAXWELL = Unit("maxwell", "Mx", MAGNETIC_FLUX, 1e-8)

# --- Magnetic Flux Density (derived: tesla) ---
TESLA = Unit("tesla", "T", MAGNETIC_FLUX_DENSITY, 1.0)
GAUSS = Unit("gauss", "G", MAGNETIC_FLUX_DENSITY, 1e-4)
GAMMA_MAG = Unit("gamma", "γ", MAGNETIC_FLUX_DENSITY, 1e-9)

# --- Magnetic Field Strength ---
AMPERE_PER_METER = Unit("ampere per meter", "A/m", MAGNETIC_FIELD_STRENGTH, 1.0)
OERSTED = Unit("oersted", "Oe", MAGNETIC_FIELD_STRENGTH, 79.5774715)

# --- Luminous Flux (derived: lumen) ---
LUMEN = Unit("lumen", "lm", LUMINOUS_FLUX, 1.0)

# --- Illuminance (derived: lux) ---
LUX = Unit("lux", "lx", ILLUMINANCE, 1.0)
PHOT = Unit("phot", "ph", ILLUMINANCE, 1e4)
FOOT_CANDLE = Unit("foot-candle", "fc", ILLUMINANCE, 10.7639)

# --- Luminance ---
CANDELA_PER_SQ_METER = Unit("candela per square meter", "cd/m²", LUMINANCE, 1.0)
NIT = Unit("nit", "nt", LUMINANCE, 1.0)
STILB = Unit("stilb", "sb", LUMINANCE, 1e4)
LAMBERT = Unit("lambert", "L", LUMINANCE, 3183.0988618)
FOOT_LAMBERT = Unit("foot-lambert", "fL", LUMINANCE, 3.4262590996)
APOSTILB = Unit("apostilb", "asb", LUMINANCE, 0.3183098862)

# --- Radioactivity (derived: becquerel) ---
BECQUEREL = Unit("becquerel", "Bq", RADIOACTIVITY, 1.0)
CURIE = Unit("curie", "Ci", RADIOACTIVITY, 3.7e10)
RUTHERFORD = Unit("rutherford", "Rd", RADIOACTIVITY, 1e6)

# --- Absorbed Dose (derived: gray) ---
GRAY = Unit("gray", "Gy", ABSORBED_DOSE, 1.0)
RAD_DOSE = Unit("rad", "rad", ABSORBED_DOSE, 0.01)

# --- Equivalent Dose (derived: sievert) ---
SIEVERT = Unit("sievert", "Sv", EQUIVALENT_DOSE, 1.0)
REM = Unit("rem", "rem", EQUIVALENT_DOSE, 0.01)
BANANA_EQUIVALENT = Unit("banana equivalent dose", "BED", EQUIVALENT_DOSE, 1e-7)

# --- Exposure ---
ROENTGEN = Unit("roentgen", "R", EXPOSURE_RADIATION, 2.58e-4)

# --- Catalytic Activity (derived: katal) ---
KATAL = Unit("katal", "kat", CATALYTIC_ACTIVITY, 1.0)
ENZYME_UNIT = Unit("enzyme unit", "U", CATALYTIC_ACTIVITY, 1.6667e-8)

# --- Density ---
KG_PER_CUBIC_METER = Unit("kilogram per cubic meter", "kg/m³", DENSITY, 1.0)
G_PER_CUBIC_CM = Unit("gram per cubic centimeter", "g/cm³", DENSITY, 1000.0)
LB_PER_CUBIC_FOOT = Unit("pound per cubic foot", "lb/ft³", DENSITY, 16.018463)
LB_PER_GALLON = Unit("pound per gallon", "lb/gal", DENSITY, 119.826)

# --- Dynamic Viscosity ---
PASCAL_SECOND = Unit("pascal second", "Pa·s", DYNAMIC_VISCOSITY, 1.0)
POISE = Unit("poise", "P", DYNAMIC_VISCOSITY, 0.1)
CENTIPOISE = Unit("centipoise", "cP", DYNAMIC_VISCOSITY, 0.001)
LB_PER_FT_S = Unit("pound per foot second", "lb/(ft·s)", DYNAMIC_VISCOSITY, 1.488164)
LB_PER_FT_H = Unit("pound per foot hour", "lb/(ft·h)", DYNAMIC_VISCOSITY, 0.000413379)
REYN = Unit("reyn", "reyn", DYNAMIC_VISCOSITY, 6894.757)

# --- Kinematic Viscosity ---
SQUARE_METER_PER_SECOND = Unit("square meter per second", "m²/s", KINEMATIC_VISCOSITY, 1.0)
STOKES = Unit("stokes", "St", KINEMATIC_VISCOSITY, 1e-4)
CENTISTOKES = Unit("centistokes", "cSt", KINEMATIC_VISCOSITY, 1e-6)

# --- Flow Rates ---
CUBIC_METER_PER_SECOND = Unit("cubic meter per second", "m³/s", VOLUMETRIC_FLOW, 1.0)
CUBIC_METER_PER_HOUR = Unit("cubic meter per hour", "m³/h", VOLUMETRIC_FLOW, 1/3600)
LITER_PER_SECOND = Unit("liter per second", "L/s", VOLUMETRIC_FLOW, 0.001)
LITER_PER_MINUTE = Unit("liter per minute", "L/min", VOLUMETRIC_FLOW, 1/60000)
GALLON_PER_MINUTE = Unit("gallon per minute", "gpm", VOLUMETRIC_FLOW, 6.30902e-5)
GALLON_PER_DAY = Unit("gallon per day", "gpd", VOLUMETRIC_FLOW, 4.38126e-8)
CUBIC_FOOT_PER_SECOND = Unit("cubic foot per second", "cfs", VOLUMETRIC_FLOW, 0.028316846592)
CUBIC_FOOT_PER_MINUTE = Unit("cubic foot per minute", "cfm", VOLUMETRIC_FLOW, 4.7194744e-4)
BARREL_PER_DAY = Unit("barrel per day", "bpd", VOLUMETRIC_FLOW, 1.8401e-6)
ACRE_FOOT_PER_DAY = Unit("acre-foot per day", "ac·ft/d", VOLUMETRIC_FLOW, 0.01427641)
SVERDRUP = Unit("sverdrup", "Sv", VOLUMETRIC_FLOW, 1e6)
MINER_INCH = Unit("miner's inch", "min_in", VOLUMETRIC_FLOW, 7.07921e-4)

KG_PER_SECOND = Unit("kilogram per second", "kg/s", MASS_FLOW, 1.0)
KG_PER_HOUR = Unit("kilogram per hour", "kg/h", MASS_FLOW, 1/3600)
TONNE_PER_HOUR = Unit("tonne per hour", "t/h", MASS_FLOW, 1000/3600)
LB_PER_SECOND = Unit("pound per second", "lb/s", MASS_FLOW, 0.45359237)
LB_PER_HOUR = Unit("pound per hour", "lb/h", MASS_FLOW, 0.45359237/3600)

MOL_PER_SECOND = Unit("mole per second", "mol/s", MOLAR_FLOW, 1.0)
KMOL_PER_HOUR = Unit("kilomole per hour", "kmol/h", MOLAR_FLOW, 1000/3600)

# --- Heat Capacity/Specific Heat ---
J_PER_K = Unit("joule per kelvin", "J/K", HEAT_CAPACITY, 1.0)
J_PER_KG_K = Unit("joule per kilogram kelvin", "J/(kg·K)", SPECIFIC_HEAT, 1.0)
BTU_PER_LB_F = Unit("BTU per pound fahrenheit", "BTU/(lb·°F)", SPECIFIC_HEAT, 4186.8)
CAL_PER_G_C = Unit("calorie per gram celsius", "cal/(g·°C)", SPECIFIC_HEAT, 4184.0)

# --- Thermal Conductivity ---
W_PER_M_K = Unit("watt per meter kelvin", "W/(m·K)", THERMAL_CONDUCTIVITY, 1.0)
BTU_PER_H_FT_F = Unit("BTU per hour foot fahrenheit", "BTU/(h·ft·°F)", THERMAL_CONDUCTIVITY, 1.730735)

# --- Heat Transfer Coefficient ---
W_PER_SQ_M_K = Unit("watt per square meter kelvin", "W/(m²·K)", HEAT_TRANSFER_COEFF, 1.0)
BTU_PER_H_SQ_FT_F = Unit("BTU per hour square foot fahrenheit", "BTU/(h·ft²·°F)", HEAT_TRANSFER_COEFF, 5.678263)

# --- Molar Quantities ---
KG_PER_MOL = Unit("kilogram per mole", "kg/mol", MOLAR_MASS, 1.0)
G_PER_MOL = Unit("gram per mole", "g/mol", MOLAR_MASS, 0.001)
KG_PER_KMOL = Unit("kilogram per kilomole", "kg/kmol", MOLAR_MASS, 0.001)

CUBIC_METER_PER_MOL = Unit("cubic meter per mole", "m³/mol", MOLAR_VOLUME, 1.0)
LITER_PER_MOL = Unit("liter per mole", "L/mol", MOLAR_VOLUME, 0.001)

J_PER_MOL = Unit("joule per mole", "J/mol", MOLAR_ENERGY, 1.0)
KJ_PER_MOL = Unit("kilojoule per mole", "kJ/mol", MOLAR_ENERGY, 1000.0)
CAL_PER_MOL = Unit("calorie per mole", "cal/mol", MOLAR_ENERGY, 4.184)
KCAL_PER_MOL = Unit("kilocalorie per mole", "kcal/mol", MOLAR_ENERGY, 4184.0)

# --- Concentration ---
MOL_PER_CUBIC_METER = Unit("mole per cubic meter", "mol/m³", CONCENTRATION, 1.0)
MOL_PER_LITER = Unit("mole per liter", "mol/L", CONCENTRATION, 1000.0)
MOLAR = Unit("molar", "M", CONCENTRATION, 1000.0)
NORMAL = Unit("normal", "N", CONCENTRATION, 1000.0)

# --- Data Rate ---
BIT_PER_SECOND = Unit("bit per second", "bps", DATA_RATE, 1.0)
BYTE_PER_SECOND = Unit("byte per second", "B/s", DATA_RATE, 8.0)
BAUD = Unit("baud", "Bd", DATA_RATE, 1.0)

# --- Surface Tension ---
NEWTON_PER_METER = Unit("newton per meter", "N/m", SURFACE_TENSION, 1.0)
DYNE_PER_CM = Unit("dyne per centimeter", "dyn/cm", SURFACE_TENSION, 0.001)

# --- Torque ---
NEWTON_METER = Unit("newton meter", "N·m", TORQUE, 1.0)
FOOT_POUND_TORQUE = Unit("foot-pound", "ft·lbf", TORQUE, 1.3558179483314)
INCH_POUND = Unit("inch-pound", "in·lbf", TORQUE, 0.1129848290276)
KILOGRAM_METER = Unit("kilogram-force meter", "kgf·m", TORQUE, STANDARD_GRAVITY)

# --- Permeability (porous media) - dimension is L² ---
DARCY = Unit("darcy", "D", AREA, 9.869233e-13)
MILLIDARCY = Unit("millidarcy", "mD", AREA, 9.869233e-16)

# --- Sound ---
DECIBEL = Unit("decibel", "dB", DIMENSIONLESS, 1.0)  # Logarithmic, special handling
NEPER = Unit("neper", "Np", DIMENSIONLESS, 1.0)
BEL = Unit("bel", "B", DIMENSIONLESS, 1.0)

# --- Photography ---
DIAPHRAGM_STOP = Unit("f-stop", "f", DIMENSIONLESS, 1.0)  # Special
EXPOSURE_VALUE = Unit("exposure value", "EV", DIMENSIONLESS, 1.0)  # Special

# --- Typography/Printing ---
LINE_PER_INCH = Unit("lines per inch", "lpi", WAVENUMBER, 39.3701)
DOTS_PER_INCH = Unit("dots per inch", "dpi", WAVENUMBER, 39.3701)
PIXELS_PER_INCH = Unit("pixels per inch", "ppi", WAVENUMBER, 39.3701)

# --- Textile ---
TEX = Unit("tex", "tex", LINEAR_DENSITY, 1e-6)
DENIER = Unit("denier", "den", LINEAR_DENSITY, 1.111e-7)
DTEX = Unit("decitex", "dtex", LINEAR_DENSITY, 1e-7)

# --- Paper ---
GSM = Unit("grams per square meter", "gsm", SURFACE_DENSITY, 0.001)
LB_PER_REAM = Unit("pounds per ream", "lb/ream", SURFACE_DENSITY, 1.6278e-3)

# --- Fuel Efficiency (special: distance/volume = L^-2) ---
FUEL_EFFICIENCY_DIM = Dimension(length=-2, name="Fuel Efficiency")
LITER_PER_100KM = Unit("liter per 100 km", "L/100km", VOLUME, 1e-8)  # Special usage
MPG_US = Unit("miles per gallon (US)", "mpg", FUEL_EFFICIENCY_DIM, 4.25144e5)
MPG_UK = Unit("miles per gallon (UK)", "mpg_UK", FUEL_EFFICIENCY_DIM, 3.54006e5)
KM_PER_LITER = Unit("kilometers per liter", "km/L", FUEL_EFFICIENCY_DIM, 1e6)

# --- Cooking/Food ---
CALORIE_FOOD = Unit("food calorie", "Cal", ENERGY, 4184.0)
KILOJOULE_FOOD = Unit("kilojoule (food)", "kJ", ENERGY, 1000.0)

# --- Medical ---
SVEDBERG = Unit("svedberg", "S", TIME, 1e-13)
HOUNSFIELD = Unit("Hounsfield unit", "HU", DIMENSIONLESS, 1.0)
MESH = Unit("mesh", "mesh", WAVENUMBER, 39.3701)  # For sieves

# --- Astronomy specific ---
JANSKY = Unit("jansky", "Jy", IRRADIANCE, 1e-26)
SOLAR_LUMINOSITY = Unit("solar luminosity", "L☉", POWER, 3.828e26)
CRAB = Unit("crab", "Crab", IRRADIANCE, 2.4e-11)  # X-ray astronomy

# --- Agriculture ---
BUSHEL_PER_ACRE = Unit("bushels per acre", "bu/ac", AREA, 1.0)  # Yield measure - special


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _get_si_unit(dimension: Dimension) -> Unit:
    """Get the SI base unit for a dimension."""
    si_units = {
        DIMENSIONLESS: UNITLESS,
        LENGTH: METER,
        MASS: KILOGRAM,
        TIME: SECOND,
        TEMPERATURE: KELVIN,
        AMOUNT: MOLE,
        ELECTRIC_CURRENT: AMPERE,
        LUMINOUS_INTENSITY: CANDELA,
        PLANE_ANGLE: RADIAN,
        SOLID_ANGLE_DIM: STERADIAN,
        INFORMATION_DIM: BIT,
        AREA: SQUARE_METER,
        VOLUME: CUBIC_METER,
        VELOCITY: METER_PER_SECOND,
        ACCELERATION: METER_PER_SECOND_SQ,
        FORCE: NEWTON,
        ENERGY: JOULE,
        POWER: WATT,
        PRESSURE: PASCAL,
        FREQUENCY: HERTZ,
        ELECTRIC_CHARGE: COULOMB,
        VOLTAGE: VOLT,
        CAPACITANCE: FARAD,
        RESISTANCE: OHM,
        CONDUCTANCE: SIEMENS,
        INDUCTANCE: HENRY,
        MAGNETIC_FLUX: WEBER,
        MAGNETIC_FLUX_DENSITY: TESLA,
        LUMINOUS_FLUX: LUMEN,
        ILLUMINANCE: LUX,
        RADIOACTIVITY: BECQUEREL,
        ABSORBED_DOSE: GRAY,
        EQUIVALENT_DOSE: SIEVERT,
        CATALYTIC_ACTIVITY: KATAL,
        DENSITY: KG_PER_CUBIC_METER,
        DYNAMIC_VISCOSITY: PASCAL_SECOND,
        KINEMATIC_VISCOSITY: SQUARE_METER_PER_SECOND,
        VOLUMETRIC_FLOW: CUBIC_METER_PER_SECOND,
        MASS_FLOW: KG_PER_SECOND,
        MOLAR_FLOW: MOL_PER_SECOND,
    }
    return si_units.get(dimension, Unit(f"SI({dimension})", "SI", dimension, 1.0))


# =============================================================================
# UNIT REGISTRY
# =============================================================================

class UnitRegistry:
    """Registry for looking up units by name or symbol."""
    
    def __init__(self):
        self._by_symbol: Dict[str, Unit] = {}
        self._by_name: Dict[str, Unit] = {}
        self._by_dimension: Dict[Dimension, List[Unit]] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """Register all predefined units."""
        import sys
        current_module = sys.modules[__name__]
        for name in dir(current_module):
            obj = getattr(current_module, name)
            if isinstance(obj, Unit):
                self.register(obj)
    
    def register(self, unit: Unit):
        """Register a unit."""
        self._by_symbol[unit.symbol] = unit
        self._by_name[unit.name.lower()] = unit
        if unit.dimension not in self._by_dimension:
            self._by_dimension[unit.dimension] = []
        self._by_dimension[unit.dimension].append(unit)
    
    def get(self, identifier: str) -> Unit:
        """Get a unit by symbol or name."""
        if identifier in self._by_symbol:
            return self._by_symbol[identifier]
        if identifier.lower() in self._by_name:
            return self._by_name[identifier.lower()]
        raise UnitError(f"Unknown unit: {identifier}")
    
    def units_for_dimension(self, dimension: Dimension) -> List[Unit]:
        """Get all units for a dimension."""
        return self._by_dimension.get(dimension, [])
    
    def __contains__(self, identifier: str) -> bool:
        return identifier in self._by_symbol or identifier.lower() in self._by_name


_registry = UnitRegistry()


def get_unit(identifier: str) -> Unit:
    """Get a unit from the global registry."""
    return _registry.get(identifier)


def Q(value: float, unit: Union[Unit, str]) -> Quantity:
    """Shorthand for creating a Quantity."""
    if isinstance(unit, str):
        unit = get_unit(unit)
    return Quantity(value, unit)


def convert(value: float, from_unit: Union[Unit, str], to_unit: Union[Unit, str]) -> float:
    """Convert a value between units."""
    if isinstance(from_unit, str):
        from_unit = get_unit(from_unit)
    if isinstance(to_unit, str):
        to_unit = get_unit(to_unit)
    return from_unit.convert_to(value, to_unit)


# =============================================================================
# MODULE DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DIMENSIONAL ANALYSIS MODULE (dimanal)")
    print("=" * 60)
    
    # Count units
    import sys
    current_module = sys.modules[__name__]
    unit_count = sum(1 for name in dir(current_module) 
                     if isinstance(getattr(current_module, name), Unit))
    prefix_count = len(SI_PREFIXES) + len(BINARY_PREFIXES)
    dimension_count = sum(1 for name in dir(current_module) 
                          if isinstance(getattr(current_module, name), Dimension))
    
    print(f"\nTotal base units defined: {unit_count}")
    print(f"Total prefixes defined: {prefix_count}")
    print(f"Total dimensions defined: {dimension_count}")
    
    # Demo prefix system
    print("\n--- Prefix System Demo ---")
    km = METER.with_prefix(KILO)
    print(f"1 {km.symbol} = {km.to_si} m")
    mm = METER.with_prefix(MILLI)
    print(f"1 {mm.symbol} = {mm.to_si} m")
    
    # Demo conversions
    print("\n--- Conversion Demo ---")
    print(f"100 °C = {convert(100, CELSIUS, KELVIN):.2f} K")
    print(f"1 atm = {convert(1, ATMOSPHERE, PSI):.4f} psi")
    print(f"1 mile = {convert(1, MILE, METER):.3f} m")
    print(f"1 hp = {convert(1, HORSEPOWER, WATT):.2f} W")
    
    # Demo Quantity
    print("\n--- Quantity Demo ---")
    distance = Q(100, KILOMETER_PER_HOUR.with_prefix(NO_PREFIX))
    # Actually let's use the defined unit
    distance = Q(100, "km/h")  # This won't work without compound units
    
    # Direct calculation
    dist = Quantity(100, METER.with_prefix(KILO))
    time = Quantity(2, HOUR)
    speed = dist / time
    print(f"Speed: {dist} / {time} = {speed}")
    
    print("\n" + "=" * 60)

# =============================================================================
# ADDITIONAL SPECIALIZED UNITS
# =============================================================================

# --- More Acceleration Units ---
KNOT_PER_SECOND = Unit("knot per second", "kn/s", ACCELERATION, 0.514444)
LEO = Unit("leo", "leo", ACCELERATION, 10.0)  # Named unit = 10 m/s²

# --- More Force Units ---
ATOMIC_UNIT_FORCE = Unit("atomic unit of force", "Eh/a₀", FORCE, 8.2387234983e-8)
MILLINEWTON = Unit("millinewton", "mN", FORCE, 0.001)
KILONEWTON = Unit("kilonewton", "kN", FORCE, 1000.0)
MEGANEWTON = Unit("meganewton", "MN", FORCE, 1e6)
GIGANEWTON = Unit("giganewton", "GN", FORCE, 1e9)

# --- More Pressure Units ---
KILOPASCAL = Unit("kilopascal", "kPa", PRESSURE, 1000.0)
MEGAPASCAL = Unit("megapascal", "MPa", PRESSURE, 1e6)
GIGAPASCAL = Unit("gigapascal", "GPa", PRESSURE, 1e9)
MILLIBAR = Unit("millibar", "mbar", PRESSURE, 100.0)
KILOBAR = Unit("kilobar", "kbar", PRESSURE, 1e8)
KPSI = Unit("kilopound per square inch", "ksi", PRESSURE, 6894757.293168)

# --- More Energy Units ---
KILOJOULE = Unit("kilojoule", "kJ", ENERGY, 1000.0)
MEGAJOULE = Unit("megajoule", "MJ", ENERGY, 1e6)
GIGAJOULE = Unit("gigajoule", "GJ", ENERGY, 1e9)
KILOWATT_HOUR = Unit("kilowatt-hour", "kWh", ENERGY, 3.6e6)
MEGAWATT_HOUR = Unit("megawatt-hour", "MWh", ENERGY, 3.6e9)
KILOCALORIE = Unit("kilocalorie", "kcal", ENERGY, 4184.0)
KILOELECTRONVOLT = Unit("kiloelectronvolt", "keV", ENERGY, ELEMENTARY_CHARGE * 1e3)
MEGAELECTRONVOLT = Unit("megaelectronvolt", "MeV", ENERGY, ELEMENTARY_CHARGE * 1e6)
GIGAELECTRONVOLT = Unit("gigaelectronvolt", "GeV", ENERGY, ELEMENTARY_CHARGE * 1e9)
TERAELECTRONVOLT = Unit("teraelectronvolt", "TeV", ENERGY, ELEMENTARY_CHARGE * 1e12)

# --- More Power Units ---
KILOWATT = Unit("kilowatt", "kW", POWER, 1000.0)
MEGAWATT = Unit("megawatt", "MW", POWER, 1e6)
GIGAWATT = Unit("gigawatt", "GW", POWER, 1e9)
TERAWATT = Unit("terawatt", "TW", POWER, 1e12)
MILLIWATT = Unit("milliwatt", "mW", POWER, 0.001)
MICROWATT = Unit("microwatt", "μW", POWER, 1e-6)
NANOWATT = Unit("nanowatt", "nW", POWER, 1e-9)

# --- Frequency with SI Prefixes ---
MILLIHERTZ = Unit("millihertz", "mHz", FREQUENCY, 0.001)
KILOHERTZ = Unit("kilohertz", "kHz", FREQUENCY, 1e3)
MEGAHERTZ = Unit("megahertz", "MHz", FREQUENCY, 1e6)
GIGAHERTZ = Unit("gigahertz", "GHz", FREQUENCY, 1e9)
TERAHERTZ = Unit("terahertz", "THz", FREQUENCY, 1e12)

# --- Electric Charge with Prefixes ---
MILLICOULOMB = Unit("millicoulomb", "mC", ELECTRIC_CHARGE, 0.001)
MICROCOULOMB = Unit("microcoulomb", "μC", ELECTRIC_CHARGE, 1e-6)
NANOCOULOMB = Unit("nanocoulomb", "nC", ELECTRIC_CHARGE, 1e-9)
PICOCOULOMB = Unit("picocoulomb", "pC", ELECTRIC_CHARGE, 1e-12)
MILLIAMPERE_HOUR = Unit("milliampere-hour", "mAh", ELECTRIC_CHARGE, 3.6)

# --- Voltage with Prefixes ---
MILLIVOLT = Unit("millivolt", "mV", VOLTAGE, 0.001)
MICROVOLT = Unit("microvolt", "μV", VOLTAGE, 1e-6)
KILOVOLT = Unit("kilovolt", "kV", VOLTAGE, 1000.0)
MEGAVOLT = Unit("megavolt", "MV", VOLTAGE, 1e6)

# --- Capacitance with Prefixes ---
MICROFARAD = Unit("microfarad", "μF", CAPACITANCE, 1e-6)
NANOFARAD = Unit("nanofarad", "nF", CAPACITANCE, 1e-9)
PICOFARAD = Unit("picofarad", "pF", CAPACITANCE, 1e-12)
FEMTOFARAD = Unit("femtofarad", "fF", CAPACITANCE, 1e-15)

# --- Resistance with Prefixes ---
MILLIOHM = Unit("milliohm", "mΩ", RESISTANCE, 0.001)
KILOHM = Unit("kilohm", "kΩ", RESISTANCE, 1000.0)
MEGOHM = Unit("megohm", "MΩ", RESISTANCE, 1e6)
GIGOHM = Unit("gigohm", "GΩ", RESISTANCE, 1e9)

# --- Inductance with Prefixes ---
MILLIHENRY = Unit("millihenry", "mH", INDUCTANCE, 0.001)
MICROHENRY = Unit("microhenry", "μH", INDUCTANCE, 1e-6)
NANOHENRY = Unit("nanohenry", "nH", INDUCTANCE, 1e-9)

# --- Magnetic Field with Prefixes ---
MILLITESLA = Unit("millitesla", "mT", MAGNETIC_FLUX_DENSITY, 0.001)
MICROTESLA = Unit("microtesla", "μT", MAGNETIC_FLUX_DENSITY, 1e-6)
NANOTESLA = Unit("nanotesla", "nT", MAGNETIC_FLUX_DENSITY, 1e-9)
MILLIGAUSS = Unit("milligauss", "mG", MAGNETIC_FLUX_DENSITY, 1e-7)
KILOGAUSS = Unit("kilogauss", "kG", MAGNETIC_FLUX_DENSITY, 0.1)

# --- Radioactivity with Prefixes ---
KILOBECQUEREL = Unit("kilobecquerel", "kBq", RADIOACTIVITY, 1e3)
MEGABECQUEREL = Unit("megabecquerel", "MBq", RADIOACTIVITY, 1e6)
GIGABECQUEREL = Unit("gigabecquerel", "GBq", RADIOACTIVITY, 1e9)
TERABECQUEREL = Unit("terabecquerel", "TBq", RADIOACTIVITY, 1e12)
MILLICURIE = Unit("millicurie", "mCi", RADIOACTIVITY, 3.7e7)
MICROCURIE = Unit("microcurie", "μCi", RADIOACTIVITY, 3.7e4)
NANOCURIE = Unit("nanocurie", "nCi", RADIOACTIVITY, 37.0)
PICOCURIE = Unit("picocurie", "pCi", RADIOACTIVITY, 0.037)

# --- Dose with Prefixes ---
MILLIGRAY = Unit("milligray", "mGy", ABSORBED_DOSE, 0.001)
MICROGRAY = Unit("microgray", "μGy", ABSORBED_DOSE, 1e-6)
MILLISIEVERT = Unit("millisievert", "mSv", EQUIVALENT_DOSE, 0.001)
MICROSIEVERT = Unit("microsievert", "μSv", EQUIVALENT_DOSE, 1e-6)
NANOSIEVERT = Unit("nanosievert", "nSv", EQUIVALENT_DOSE, 1e-9)

# --- Data/Information Units ---
KILOBIT = Unit("kilobit", "kb", INFORMATION_DIM, 1e3)
MEGABIT = Unit("megabit", "Mb", INFORMATION_DIM, 1e6)
GIGABIT = Unit("gigabit", "Gb", INFORMATION_DIM, 1e9)
TERABIT = Unit("terabit", "Tb", INFORMATION_DIM, 1e12)
KILOBYTE = Unit("kilobyte", "kB", INFORMATION_DIM, 8e3)
MEGABYTE = Unit("megabyte", "MB", INFORMATION_DIM, 8e6)
GIGABYTE = Unit("gigabyte", "GB", INFORMATION_DIM, 8e9)
TERABYTE = Unit("terabyte", "TB", INFORMATION_DIM, 8e12)
PETABYTE = Unit("petabyte", "PB", INFORMATION_DIM, 8e15)

# Binary information units
KIBIBYTE = Unit("kibibyte", "KiB", INFORMATION_DIM, 8 * 2**10)
MEBIBYTE = Unit("mebibyte", "MiB", INFORMATION_DIM, 8 * 2**20)
GIBIBYTE = Unit("gibibyte", "GiB", INFORMATION_DIM, 8 * 2**30)
TEBIBYTE = Unit("tebibyte", "TiB", INFORMATION_DIM, 8 * 2**40)
PEBIBYTE = Unit("pebibyte", "PiB", INFORMATION_DIM, 8 * 2**50)

# --- Data Rate Units ---
KILOBIT_PER_SECOND = Unit("kilobit per second", "kbps", DATA_RATE, 1e3)
MEGABIT_PER_SECOND = Unit("megabit per second", "Mbps", DATA_RATE, 1e6)
GIGABIT_PER_SECOND = Unit("gigabit per second", "Gbps", DATA_RATE, 1e9)
TERABIT_PER_SECOND = Unit("terabit per second", "Tbps", DATA_RATE, 1e12)
KILOBYTE_PER_SECOND = Unit("kilobyte per second", "kB/s", DATA_RATE, 8e3)
MEGABYTE_PER_SECOND = Unit("megabyte per second", "MB/s", DATA_RATE, 8e6)
GIGABYTE_PER_SECOND = Unit("gigabyte per second", "GB/s", DATA_RATE, 8e9)

# --- Illuminance with Prefixes ---
KILOLUX = Unit("kilolux", "klx", ILLUMINANCE, 1e3)
MEGALUX = Unit("megalux", "Mlx", ILLUMINANCE, 1e6)
MILLILUX = Unit("millilux", "mlx", ILLUMINANCE, 0.001)
MICROLUX = Unit("microlux", "μlx", ILLUMINANCE, 1e-6)

# --- Catalytic Activity ---
MICROKATAL = Unit("microkatal", "μkat", CATALYTIC_ACTIVITY, 1e-6)
NANOKATAL = Unit("nanokatal", "nkat", CATALYTIC_ACTIVITY, 1e-9)
FEMTOKATAL = Unit("femtokatal", "fkat", CATALYTIC_ACTIVITY, 1e-15)

# --- Obsolete/Historical CGS Units ---
CGS_VELOCITY = Unit("centimeter per second", "cm/s", VELOCITY, 0.01)
CGS_ACCELERATION = Unit("gal", "cm/s²", ACCELERATION, 0.01)
KAYSER = Unit("kayser", "K", WAVENUMBER, 100.0)  # cm⁻¹
LANGLEY = Unit("langley", "ly", ENERGY, 41840.0)  # Energy per unit area

# --- Photographic Units ---
ASA = Unit("ASA", "ASA", DIMENSIONLESS, 1.0)  # Film speed
ISO = Unit("ISO", "ISO", DIMENSIONLESS, 1.0)  # Film speed

# --- Textile Additional ---
KILOTEX = Unit("kilotex", "ktex", LINEAR_DENSITY, 1e-3)
MILLITEX = Unit("millitex", "mtex", LINEAR_DENSITY, 1e-9)

# --- Water Hardness ---
DEGREE_GERMAN_HARDNESS = Unit("German hardness degree", "°dH", CONCENTRATION, 0.1783)
DEGREE_FRENCH_HARDNESS = Unit("French hardness degree", "°fH", CONCENTRATION, 0.1)
DEGREE_ENGLISH_HARDNESS = Unit("English hardness degree", "°e", CONCENTRATION, 0.1424)
PPM_CACO3 = Unit("ppm as CaCO3", "ppm CaCO₃", CONCENTRATION, 0.01)

# --- Enzyme Units ---
INTERNATIONAL_UNIT = Unit("international unit", "IU", CATALYTIC_ACTIVITY, 1.6667e-8)
KATAL_PER_LITER = Unit("katal per liter", "kat/L", Dimension(amount=1, length=-3, time=-1), 1000.0)

# --- Spectroscopy ---
RECIPROCAL_CENTIMETER = Unit("reciprocal centimeter", "cm⁻¹", WAVENUMBER, 100.0)
WAVE_NUMBER = Unit("wave number", "1/cm", WAVENUMBER, 100.0)

# --- Printing/Publishing ---
CICERO_12 = Unit("cicero", "cc", LENGTH, 0.00451)
AGATE_LINE = Unit("agate", "ag", LENGTH, 0.00179)

# --- Musical ---
CENT_MUSIC = Unit("cent", "¢", DIMENSIONLESS, 1.0)  # 1/1200 of octave
SAVART = Unit("savart", "savart", DIMENSIONLESS, 1.0)  # 1/301 of octave
OCTAVE = Unit("octave", "oct", DIMENSIONLESS, 1.0)  # Frequency ratio

# --- Colorimetry ---
DELTA_E = Unit("delta E", "ΔE", DIMENSIONLESS, 1.0)  # Color difference

# --- Food/Nutrition ---
DIETARY_CALORIE = Unit("dietary calorie", "Cal", ENERGY, 4184.0)  # Same as kcal
KILOJOULE_FOOD = Unit("kilojoule", "kJ", ENERGY, 1000.0)

# --- Vehicle/Transportation ---
PASSENGER_KILOMETER = Unit("passenger-kilometer", "pkm", LENGTH, 1000.0)
TONNE_KILOMETER = Unit("tonne-kilometer", "tkm", Dimension(mass=1, length=1), 1e6)
VEHICLE_KILOMETER = Unit("vehicle-kilometer", "vkm", LENGTH, 1000.0)

# --- Environmental ---
CARBON_DIOXIDE_EQUIVALENT = Unit("CO2 equivalent", "CO₂-eq", MASS, 1.0)
GLOBAL_WARMING_POTENTIAL = Unit("GWP", "GWP", DIMENSIONLESS, 1.0)

# --- Construction ---
CUBIC_YARD_CONCRETE = Unit("cubic yard", "cy", VOLUME, 0.764554857984)
SQUARE_FOOT_CONSTRUCTION = Unit("square foot", "sf", AREA, 0.09290304)
LINEAR_FOOT = Unit("linear foot", "lf", LENGTH, 0.3048)
BOARD_FOOT_LUMBER = Unit("board foot", "bf", VOLUME, 0.002359737)

# --- Oil & Gas Industry ---
THOUSAND_CUBIC_FEET = Unit("thousand cubic feet", "Mcf", VOLUME, 28.316846592)
MILLION_CUBIC_FEET = Unit("million cubic feet", "MMcf", VOLUME, 28316.846592)
BILLION_CUBIC_FEET = Unit("billion cubic feet", "Bcf", VOLUME, 28316846.592)
TRILLION_CUBIC_FEET = Unit("trillion cubic feet", "Tcf", VOLUME, 28316846592.0)
THOUSAND_BARRELS = Unit("thousand barrels", "Mbbl", VOLUME, 158.987294928)
MILLION_BARRELS = Unit("million barrels", "MMbbl", VOLUME, 158987.294928)
BARRELS_PER_DAY_OIL = Unit("barrels per day", "bpd", VOLUMETRIC_FLOW, 1.8401e-6)
THOUSAND_BARRELS_PER_DAY = Unit("thousand barrels per day", "Mbpd", VOLUMETRIC_FLOW, 1.8401e-3)

# --- Mining ---
TROY_OUNCE_PER_TON = Unit("troy ounce per ton", "oz/t", Dimension(amount=1, mass=-1), 3.4286e-5)
GRAMS_PER_TONNE = Unit("grams per tonne", "g/t", Dimension(amount=1, mass=-1), 1e-6)
PENNYWEIGHT_PER_TON = Unit("pennyweight per ton", "dwt/t", Dimension(amount=1, mass=-1), 1.714e-6)

# --- Semiconductor ---
ELECTRON_MOBILITY = Unit("electron mobility", "cm²/(V·s)", Dimension(length=2, time=1, mass=-1, current=1), 1e-4)

# --- Acoustics Additional ---
PHON = Unit("phon", "phon", DIMENSIONLESS, 1.0)  # Loudness level
SONE = Unit("sone", "sone", DIMENSIONLESS, 1.0)  # Loudness
SABINE = Unit("sabin", "sabin", AREA, 0.09290304)  # Acoustic absorption

# --- Flow (more industry units) ---
STANDARD_CUBIC_FOOT_PER_MINUTE = Unit("standard cubic foot per minute", "SCFM", VOLUMETRIC_FLOW, 4.7195e-4)
STANDARD_CUBIC_METER_PER_HOUR = Unit("standard cubic meter per hour", "Sm³/h", VOLUMETRIC_FLOW, 2.7778e-4)
NORMAL_CUBIC_METER_PER_HOUR = Unit("normal cubic meter per hour", "Nm³/h", VOLUMETRIC_FLOW, 2.7778e-4)
ACTUAL_CUBIC_FEET_PER_MINUTE = Unit("actual cubic feet per minute", "ACFM", VOLUMETRIC_FLOW, 4.7195e-4)

# --- Torque Additional ---
INCH_OUNCE = Unit("inch-ounce", "in·oz", TORQUE, 0.00706155)
FOOT_OUNCE = Unit("foot-ounce", "ft·oz", TORQUE, 0.084739)
DYNE_CENTIMETER = Unit("dyne-centimeter", "dyn·cm", TORQUE, 1e-7)

# --- Historical Electrical ---
INTERNATIONAL_OHM = Unit("international ohm", "Ω_int", RESISTANCE, 1.00049)
INTERNATIONAL_AMPERE = Unit("international ampere", "A_int", ELECTRIC_CURRENT, 0.99985)
INTERNATIONAL_VOLT = Unit("international volt", "V_int", VOLTAGE, 1.00034)


# =============================================================================
# CONVENIENCE FUNCTIONS FOR COMMON CONVERSIONS
# =============================================================================

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def miles_to_kilometers(miles: float) -> float:
    """Convert miles to kilometers."""
    return miles * 1.609344

def kilometers_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return km / 1.609344

def pounds_to_kilograms(pounds: float) -> float:
    """Convert pounds to kilograms."""
    return pounds * 0.45359237

def kilograms_to_pounds(kg: float) -> float:
    """Convert kilograms to pounds."""
    return kg / 0.45359237

def gallons_to_liters(gallons: float, us: bool = True) -> float:
    """Convert gallons to liters (US or UK)."""
    if us:
        return gallons * 3.785411784
    else:
        return gallons * 4.54609

def liters_to_gallons(liters: float, us: bool = True) -> float:
    """Convert liters to gallons (US or UK)."""
    if us:
        return liters / 3.785411784
    else:
        return liters / 4.54609

def psi_to_bar(psi: float) -> float:
    """Convert psi to bar."""
    return psi * 0.0689476

def bar_to_psi(bar: float) -> float:
    """Convert bar to psi."""
    return bar / 0.0689476

def hp_to_kw(hp: float) -> float:
    """Convert horsepower to kilowatts."""
    return hp * 0.7457

def kw_to_hp(kw: float) -> float:
    """Convert kilowatts to horsepower."""
    return kw / 0.7457


# =============================================================================
# UPDATE REGISTRY
# =============================================================================

# Re-register all units (the registry should auto-register on import)
_registry = UnitRegistry()
