# API Reference
## Industrial Plant Simulation Software

**Version:** 0.1.0-dev  
**Last Updated:** November 2025  
**Status:** Phase 1 Complete

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Module](#core-module)
   - [Component API](#component-api)
   - [Stream API](#stream-api)
5. [Thermodynamics Module](#thermodynamics-module)
   - [Equations of State](#equations-of-state)
   - [Vapor-Liquid Equilibrium](#vapor-liquid-equilibrium)
   - [Flash Calculations](#flash-calculations)
6. [Dimensional Analysis Module](#dimensional-analysis-module)
   - [Dimensions](#dimensions)
   - [Units](#units)
   - [Quantities](#quantities)
   - [Prefixes](#prefixes)
   - [Physical Constants](#physical-constants)
7. [Utility Functions](#utility-functions)
8. [Error Handling](#error-handling)
9. [Type Hints Reference](#type-hints-reference)
10. [Examples](#examples)
11. [Migration Guide](#migration-guide)

---

## 🎯 Introduction

This API reference provides complete documentation for all public APIs in the Plant Simulation Software. The software is organized into three main modules:

- **`src.core`** - Core data structures (Component, Stream)
- **`src.thermo`** - Thermodynamic calculations (EOS, VLE, Flash)
- **`src.dimanal`** - Dimensional analysis and unit system

### Conventions

- All temperatures in **Kelvin (K)**
- All pressures in **Pascal (Pa)**
- All flows in **kilomoles per second (kmol/s)**
- All energies in **Joules (J)**
- Type hints provided for all functions
- Exceptions documented for each method

---

## 📦 Installation

### Basic Installation

```bash
# Clone repository
git clone https://github.com/yourusername/plant-simulation-software.git
cd plant-simulation-software

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install in development mode
pip install -e .
```

### Dependencies

```
numpy>=1.24.0
scipy>=1.10.0
pandas>=2.0.0
```

---

## 🚀 Quick Start

### Basic Example

```python
# Import modules
from src.core.component import create_water, create_methane
from src.core.stream import Stream, UnitConversion
from src.thermo.thermo import Flash, VLE

# Create components
water = create_water()
methane = create_methane()

# Create a stream
stream = Stream(
    name="Feed",
    temperature=UnitConversion.celsius_to_kelvin(25),
    pressure=UnitConversion.bar_to_pascal(10),
    components={'Water': water, 'Methane': methane},
    mole_fractions={'Water': 0.5, 'Methane': 0.5},
    molar_flow=100.0
)

# Perform flash calculation
components = {'Water': water, 'Methane': methane}
feed = {'Water': 0.5, 'Methane': 0.5}
result = Flash.isothermal_flash(320, 500000, feed, components)

print(f"Vapor fraction: {result.vapor_fraction:.4f}")
```

---

## 📦 Core Module

### Component API

#### `Component` Class

Represents a chemical compound with thermodynamic and physical properties.

**Module:** `src.core.component`

##### Class Definition

```python
@dataclass(frozen=True)
class Component:
    """
    Chemical component with thermodynamic properties.
    
    Attributes:
        name (str): Common name of component
        formula (str): Chemical formula
        cas_number (str): CAS Registry Number
        molecular_weight (float): Molecular weight in kg/kmol
        critical_temperature (float): Critical temperature in K
        critical_pressure (float): Critical pressure in Pa
        critical_volume (float): Critical molar volume in m³/kmol
        acentric_factor (float): Pitzer acentric factor (dimensionless)
        normal_boiling_point (Optional[float]): Normal boiling point in K
        normal_melting_point (Optional[float]): Normal melting point in K
        cp_ideal_gas_a (Optional[float]): Heat capacity coefficient A
        cp_ideal_gas_b (Optional[float]): Heat capacity coefficient B
        cp_ideal_gas_c (Optional[float]): Heat capacity coefficient C
        cp_ideal_gas_d (Optional[float]): Heat capacity coefficient D
        antoine_a (Optional[float]): Antoine coefficient A
        antoine_b (Optional[float]): Antoine coefficient B
        antoine_c (Optional[float]): Antoine coefficient C
        antoine_tmin (Optional[float]): Valid temperature range minimum in K
        antoine_tmax (Optional[float]): Valid temperature range maximum in K
        heat_of_vaporization (Optional[float]): Heat of vaporization in J/kmol
        phase_at_stp (str): Phase at STP ('gas', 'liquid', 'solid')
        description (str): Additional notes
    """
```

##### Methods

###### `vapor_pressure(temperature: float) -> float`

Calculate vapor pressure using Antoine equation.

**Parameters:**
- `temperature` (float): Temperature in K

**Returns:**
- `float`: Vapor pressure in Pa

**Raises:**
- `ValueError`: If Antoine coefficients are not defined

**Example:**
```python
water = create_water()
p_sat = water.vapor_pressure(373.15)  # ~101325 Pa at 100°C
```

**Notes:**
- Uses Antoine equation: log₁₀(P) = A - B/(T+C)
- Warns if temperature is outside valid range
- Pressure returned in Pascal (Pa)

---

###### `cp_ideal_gas(temperature: float) -> float`

Calculate ideal gas heat capacity at given temperature.

**Parameters:**
- `temperature` (float): Temperature in K

**Returns:**
- `float`: Heat capacity in J/(kmol·K)

**Raises:**
- `ValueError`: If heat capacity coefficients are not defined

**Example:**
```python
water = create_water()
cp = water.cp_ideal_gas(300)  # J/(kmol·K) at 300K
```

**Notes:**
- Uses polynomial: Cp = A + B·T + C·T² + D·T³
- Temperature-dependent property
- Ideal gas assumption

---

###### `reduced_temperature(temperature: float) -> float`

Calculate reduced temperature (T/Tc).

**Parameters:**
- `temperature` (float): Temperature in K

**Returns:**
- `float`: Reduced temperature (dimensionless)

**Raises:**
- `ValueError`: If critical temperature is not defined or zero

**Example:**
```python
water = create_water()
Tr = water.reduced_temperature(400)  # ~0.618
```

---

###### `reduced_pressure(pressure: float) -> float`

Calculate reduced pressure (P/Pc).

**Parameters:**
- `pressure` (float): Pressure in Pa

**Returns:**
- `float`: Reduced pressure (dimensionless)

**Raises:**
- `ValueError`: If critical pressure is not defined or zero

**Example:**
```python
water = create_water()
Pr = water.reduced_pressure(101325)  # ~0.00459
```

---

###### `to_dict() -> Dict[str, Any]`

Convert component to dictionary for serialization.

**Returns:**
- `Dict[str, Any]`: Component properties as dictionary

**Example:**
```python
water = create_water()
data = water.to_dict()
# Save to JSON, database, etc.
```

---

###### `from_dict(data: Dict[str, Any]) -> Component` (classmethod)

Create component from dictionary.

**Parameters:**
- `data` (Dict[str, Any]): Component properties as dictionary

**Returns:**
- `Component`: New component instance

**Example:**
```python
data = {
    'name': 'Nitrogen',
    'formula': 'N2',
    'molecular_weight': 28.014,
    # ... more properties
}
nitrogen = Component.from_dict(data)
```

---

##### Factory Functions

###### `create_water() -> Component`

Create water component with standard properties.

**Returns:**
- `Component`: Water (H₂O) with complete properties

**Example:**
```python
from src.core.component import create_water

water = create_water()
print(water.name)  # "Water"
print(water.formula)  # "H2O"
print(water.molecular_weight)  # 18.015
```

**Properties Included:**
- Critical properties (Tc=647.1K, Pc=22.064 MPa)
- Antoine coefficients for vapor pressure
- Heat capacity polynomial coefficients
- Normal boiling point (373.15K)
- Heat of vaporization

---

###### `create_methane() -> Component`

Create methane component with standard properties.

**Returns:**
- `Component`: Methane (CH₄) with complete properties

**Example:**
```python
from src.core.component import create_methane

methane = create_methane()
print(methane.name)  # "Methane"
print(methane.phase_at_stp)  # "gas"
```

---

### Stream API

#### `Stream` Class

Represents a process stream with temperature, pressure, composition, and flow rate.

**Module:** `src.core.stream`

##### Class Definition

```python
@dataclass
class Stream:
    """
    Process stream with thermodynamic state and composition.
    
    Attributes:
        name (str): Stream identifier
        temperature (float): Temperature in K
        pressure (float): Pressure in Pa
        components (Dict[str, Component]): Dictionary of components by name
        mole_fractions (Dict[str, float]): Mole fractions (sum = 1.0)
        molar_flow (float): Total molar flow rate in kmol/s
        phase (str): Phase state ('vapor', 'liquid', 'mixed', 'unknown')
    """
```

##### Methods

###### `molecular_weight() -> float`

Calculate average molecular weight of the mixture.

**Returns:**
- `float`: Average molecular weight in kg/kmol

**Formula:**
```
MW_avg = Σ(xi · MWi)
```

**Example:**
```python
stream = Stream(
    name="Mix",
    temperature=300,
    pressure=101325,
    components={'Water': water, 'Methane': methane},
    mole_fractions={'Water': 0.5, 'Methane': 0.5},
    molar_flow=100
)
mw = stream.molecular_weight()  # ~17.029 kg/kmol
```

---

###### `mass_flow() -> float`

Calculate total mass flow rate.

**Returns:**
- `float`: Mass flow rate in kg/s

**Formula:**
```
ṁ = ṅ · MW_avg
```

**Example:**
```python
m_dot = stream.mass_flow()  # kg/s
```

---

###### `component_molar_flows() -> Dict[str, float]`

Calculate individual component molar flow rates.

**Returns:**
- `Dict[str, float]`: Molar flow rates in kmol/s for each component

**Formula:**
```
ṅi = ṅtotal · xi
```

**Example:**
```python
comp_flows = stream.component_molar_flows()
# {'Water': 50.0, 'Methane': 50.0}
```

---

###### `component_mass_flows() -> Dict[str, float]`

Calculate individual component mass flow rates.

**Returns:**
- `Dict[str, float]`: Mass flow rates in kg/s for each component

**Formula:**
```
ṁi = ṅi · MWi
```

**Example:**
```python
mass_flows = stream.component_mass_flows()
# {'Water': 900.75, 'Methane': 802.15}
```

---

###### `mass_fractions() -> Dict[str, float]`

Calculate mass fractions from mole fractions.

**Returns:**
- `Dict[str, float]`: Mass fractions for each component

**Formula:**
```
wi = (xi · MWi) / MW_avg
```

**Example:**
```python
mass_fracs = stream.mass_fractions()
# {'Water': 0.529, 'Methane': 0.471}
```

---

###### `volumetric_flow(density: float) -> float`

Calculate volumetric flow rate.

**Parameters:**
- `density` (float): Density in kg/m³

**Returns:**
- `float`: Volumetric flow rate in m³/s

**Formula:**
```
Q = ṁ / ρ
```

**Raises:**
- `ValueError`: If density is zero or negative

**Example:**
```python
rho = stream.ideal_gas_density()
Q = stream.volumetric_flow(rho)  # m³/s
```

---

###### `ideal_gas_density() -> float`

Calculate density assuming ideal gas behavior.

**Returns:**
- `float`: Density in kg/m³

**Formula:**
```
ρ = (P · MW) / (R · T)
```

**Example:**
```python
rho = stream.ideal_gas_density()  # kg/m³
```

**Notes:**
- Assumes ideal gas (PV = nRT)
- Use only for gases at low pressure
- R = 8314.46 J/(kmol·K)

---

###### `molar_volume_ideal_gas() -> float`

Calculate molar volume assuming ideal gas.

**Returns:**
- `float`: Molar volume in m³/kmol

**Formula:**
```
Vm = R·T / P
```

**Example:**
```python
V = stream.molar_volume_ideal_gas()  # m³/kmol
```

---

###### `enthalpy_ideal_gas(reference_temp: float = 298.15) -> float`

Calculate enthalpy assuming ideal gas behavior.

**Parameters:**
- `reference_temp` (float, optional): Reference temperature in K. Default: 298.15

**Returns:**
- `float`: Specific enthalpy in J/kg

**Notes:**
- Simplified calculation using constant Cp
- More rigorous calculation requires temperature-dependent Cp integration
- Ideal gas assumption

**Example:**
```python
h = stream.enthalpy_ideal_gas()  # J/kg
```

---

###### `copy() -> Stream`

Create a deep copy of the stream.

**Returns:**
- `Stream`: New stream instance with same properties

**Example:**
```python
stream_copy = stream.copy()
stream_copy.temperature = 350  # Doesn't affect original
```

---

###### `mix_with(other: Stream) -> Stream`

Mix this stream with another stream (adiabatic mixing).

**Parameters:**
- `other` (Stream): Stream to mix with

**Returns:**
- `Stream`: New mixed stream

**Conservation Laws:**
- Mass: ṅout = ṅ1 + ṅ2
- Component: ṅi,out = ṅi,1 + ṅi,2
- Energy: Hout = H1 + H2 (adiabatic)
- Pressure: Pout = min(P1, P2)

**Example:**
```python
stream1 = Stream(name="S1", temperature=300, ...)
stream2 = Stream(name="S2", temperature=350, ...)
mixed = stream1.mix_with(stream2)
print(mixed.name)  # "S1+S2"
```

**Notes:**
- Temperature calculation is mass-weighted
- Pressure drops to minimum
- Components are combined
- Creates new stream (original streams unchanged)

---

###### `split(fraction: float, name_suffix: str = "_split") -> Stream`

Split stream into two streams with same composition.

**Parameters:**
- `fraction` (float): Fraction going to output stream (0 to 1)
- `name_suffix` (str, optional): Suffix to add to stream name. Default: "_split"

**Returns:**
- `Stream`: New stream with flow = fraction × original flow

**Raises:**
- `ValueError`: If fraction is not between 0 and 1

**Example:**
```python
original = Stream(name="Feed", molar_flow=100, ...)
top = original.split(0.7, "_top")       # 70 kmol/s
bottom = original.split(0.3, "_bottom")  # 30 kmol/s
```

**Notes:**
- Composition unchanged
- Temperature and pressure unchanged
- Only flow rate changes

---

###### `summary() -> str`

Generate detailed summary of stream properties.

**Returns:**
- `str`: Multi-line summary string

**Example:**
```python
print(stream.summary())
```

**Output:**
```
Stream: Feed
==================================================
Temperature: 300.00 K (26.85 °C)
Pressure: 10.0000 bar (1.0000 MPa)
Phase: mixed

Flow Rates:
  Molar flow: 100.0000 kmol/s (360000.00 kmol/h)
  Mass flow: 1702.9000 kg/s (6130440.00 kg/h)
  Molecular weight: 17.0290 kg/kmol

Composition (Mole Basis):
  Methane             :   0.5000 (    50.0000 kmol/s)
  Water               :   0.5000 (    50.0000 kmol/s)

Composition (Mass Basis):
  Methane             :   0.4713 (   802.1500 kg/s)
  Water               :   0.5287 (   900.7500 kg/s)
```

---

#### `UnitConversion` Class

Utility class for unit conversions.

**Module:** `src.core.stream`

##### Methods

All methods are static and don't require instantiation.

###### Temperature Conversions

```python
UnitConversion.celsius_to_kelvin(temp_c: float) -> float
UnitConversion.kelvin_to_celsius(temp_k: float) -> float
UnitConversion.fahrenheit_to_kelvin(temp_f: float) -> float
UnitConversion.kelvin_to_fahrenheit(temp_k: float) -> float
```

**Examples:**
```python
T_k = UnitConversion.celsius_to_kelvin(25)      # 298.15 K
T_c = UnitConversion.kelvin_to_celsius(373.15)  # 100.0 °C
T_k = UnitConversion.fahrenheit_to_kelvin(77)   # 298.15 K
T_f = UnitConversion.kelvin_to_fahrenheit(300)  # 80.33 °F
```

###### Pressure Conversions

```python
UnitConversion.bar_to_pascal(pressure_bar: float) -> float
UnitConversion.pascal_to_bar(pressure_pa: float) -> float
UnitConversion.psi_to_pascal(pressure_psi: float) -> float
UnitConversion.pascal_to_psi(pressure_pa: float) -> float
UnitConversion.atm_to_pascal(pressure_atm: float) -> float
UnitConversion.pascal_to_atm(pressure_pa: float) -> float
```

**Examples:**
```python
P_pa = UnitConversion.bar_to_pascal(10)        # 1000000 Pa
P_bar = UnitConversion.pascal_to_bar(101325)   # 1.01325 bar
P_pa = UnitConversion.atm_to_pascal(1)         # 101325 Pa
P_psi = UnitConversion.pascal_to_psi(101325)   # 14.696 psi
```

###### Flow Rate Conversions

```python
UnitConversion.kmol_s_to_kmol_h(flow_kmol_s: float) -> float
UnitConversion.kmol_h_to_kmol_s(flow_kmol_h: float) -> float
```

**Examples:**
```python
flow_h = UnitConversion.kmol_s_to_kmol_h(10)    # 36000 kmol/h
flow_s = UnitConversion.kmol_h_to_kmol_s(3600)  # 1.0 kmol/s
```

---

## 🌡️ Thermodynamics Module

### Equations of State

#### `IdealGas` Class

Ideal gas law calculations (PV = nRT).

**Module:** `src.thermo.thermo`

##### Methods

###### `molar_volume(temperature: float, pressure: float) -> float` (static)

Calculate molar volume of ideal gas.

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa

**Returns:**
- `float`: Molar volume in m³/kmol

**Formula:**
```
V = R·T / P
```

**Example:**
```python
from src.thermo.thermo import IdealGas

V = IdealGas.molar_volume(300, 101325)  # ~24.79 m³/kmol
```

---

###### `pressure(temperature: float, molar_volume: float) -> float` (static)

Calculate pressure from temperature and molar volume.

**Parameters:**
- `temperature` (float): Temperature in K
- `molar_volume` (float): Molar volume in m³/kmol

**Returns:**
- `float`: Pressure in Pa

**Formula:**
```
P = R·T / V
```

**Example:**
```python
P = IdealGas.pressure(300, 24.79)  # ~101325 Pa
```

---

###### `compressibility_factor() -> float` (static)

Return compressibility factor for ideal gas.

**Returns:**
- `float`: Always 1.0 for ideal gas

**Example:**
```python
Z = IdealGas.compressibility_factor()  # 1.0
```

---

#### `VanDerWaalsEOS` Class

Van der Waals equation of state for real gases.

**Module:** `src.thermo.thermo`

**Equation:**
```
(P + a/V²)(V - b) = RT
```

##### Methods

###### `calculate_parameters(component: Component) -> Tuple[float, float]` (static)

Calculate van der Waals parameters a and b from critical properties.

**Parameters:**
- `component` (Component): Component with critical properties

**Returns:**
- `Tuple[float, float]`: Parameters (a, b)
  - a in Pa·m⁶/kmol²
  - b in m³/kmol

**Formulas:**
```
a = 27·R²·Tc² / (64·Pc)
b = R·Tc / (8·Pc)
```

**Example:**
```python
from src.thermo.thermo import VanDerWaalsEOS
from src.core.component import create_methane

methane = create_methane()
a, b = VanDerWaalsEOS.calculate_parameters(methane)
```

---

###### `molar_volume(temperature, pressure, component, phase='vapor') -> float` (static)

Calculate molar volume using van der Waals EOS.

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa
- `component` (Component): Component
- `phase` (str, optional): 'vapor' or 'liquid'. Default: 'vapor'

**Returns:**
- `float`: Molar volume in m³/kmol

**Raises:**
- `ValueError`: If no valid roots found

**Example:**
```python
V_vapor = VanDerWaalsEOS.molar_volume(300, 101325, methane, 'vapor')
V_liquid = VanDerWaalsEOS.molar_volume(300, 101325, methane, 'liquid')
```

**Notes:**
- Solves cubic equation using NumPy
- Returns largest root for vapor, smallest for liquid
- May not have solution at all conditions

---

###### `compressibility_factor(temperature, pressure, component, phase='vapor') -> float` (static)

Calculate compressibility factor Z = PV/(RT).

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa
- `component` (Component): Component
- `phase` (str, optional): 'vapor' or 'liquid'. Default: 'vapor'

**Returns:**
- `float`: Compressibility factor (dimensionless)

**Example:**
```python
Z = VanDerWaalsEOS.compressibility_factor(300, 101325, methane, 'vapor')
```

---

#### `RedlichKwongEOS` Class

Redlich-Kwong equation of state for real gases.

**Module:** `src.thermo.thermo`

**Equation:**
```
P = R·T/(V-b) - a/(√T·V(V+b))
```

##### Methods

###### `calculate_parameters(component: Component) -> Tuple[float, float]` (static)

Calculate Redlich-Kwong parameters a and b.

**Parameters:**
- `component` (Component): Component with critical properties

**Returns:**
- `Tuple[float, float]`: Parameters (a, b)
  - a in Pa·m⁶·K^0.5/kmol²
  - b in m³/kmol

**Formulas:**
```
a = 0.42748·R²·Tc^2.5 / Pc
b = 0.08664·R·Tc / Pc
```

**Example:**
```python
from src.thermo.thermo import RedlichKwongEOS

a, b = RedlichKwongEOS.calculate_parameters(methane)
```

---

###### `molar_volume(temperature, pressure, component, phase='vapor') -> float` (static)

Calculate molar volume using Redlich-Kwong EOS.

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa
- `component` (Component): Component
- `phase` (str, optional): 'vapor' or 'liquid'. Default: 'vapor'

**Returns:**
- `float`: Molar volume in m³/kmol

**Example:**
```python
V = RedlichKwongEOS.molar_volume(300, 101325, methane, 'vapor')
```

---

###### `compressibility_factor(temperature, pressure, component, phase='vapor') -> float` (static)

Calculate compressibility factor.

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa
- `component` (Component): Component
- `phase` (str, optional): 'vapor' or 'liquid'. Default: 'vapor'

**Returns:**
- `float`: Compressibility factor (dimensionless)

**Example:**
```python
Z = RedlichKwongEOS.compressibility_factor(300, 101325, methane, 'vapor')
```

---

### Vapor-Liquid Equilibrium

#### `VLE` Class

Vapor-liquid equilibrium calculations using Raoult's Law.

**Module:** `src.thermo.thermo`

##### Methods

###### `raoult_law_k_values(temperature, pressure, components) -> Dict[str, float]` (static)

Calculate K-values using Raoult's Law for ideal mixtures.

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa
- `components` (Dict[str, Component]): Dictionary of components

**Returns:**
- `Dict[str, float]`: K-values for each component

**Formula:**
```
Ki = Pi_sat / P
```

**Example:**
```python
from src.thermo.thermo import VLE

components = {'Water': water, 'Methane': methane}
k_values = VLE.raoult_law_k_values(320, 500000, components)
# {'Water': 0.234, 'Methane': 45.2}
```

**Notes:**
- K > 1: Component prefers vapor (light/volatile)
- K < 1: Component prefers liquid (heavy)
- K = 1: At boiling point
- Valid for ideal mixtures only

---

###### `bubble_point_pressure(temperature, liquid_mole_fractions, components) -> float` (static)

Calculate bubble point pressure at given temperature.

**Parameters:**
- `temperature` (float): Temperature in K
- `liquid_mole_fractions` (Dict[str, float]): Liquid composition
- `components` (Dict[str, Component]): Dictionary of components

**Returns:**
- `float`: Bubble point pressure in Pa

**Formula:**
```
P_bubble = Σ(xi · Pi_sat)
```

**Example:**
```python
liquid_comp = {'Water': 0.5, 'Methane': 0.5}
P_bubble = VLE.bubble_point_pressure(300, liquid_comp, components)
```

**Notes:**
- Bubble point = pressure where first vapor bubble forms
- All liquid below this pressure
- Two-phase above this pressure

---

###### `dew_point_pressure(temperature, vapor_mole_fractions, components) -> float` (static)

Calculate dew point pressure at given temperature.

**Parameters:**
- `temperature` (float): Temperature in K
- `vapor_mole_fractions` (Dict[str, float]): Vapor composition
- `components` (Dict[str, Component]): Dictionary of components

**Returns:**
- `float`: Dew point pressure in Pa

**Formula:**
```
P_dew = 1 / Σ(yi / Pi_sat)
```

**Example:**
```python
vapor_comp = {'Water': 0.3, 'Methane': 0.7}
P_dew = VLE.dew_point_pressure(300, vapor_comp, components)
```

**Notes:**
- Dew point = pressure where first liquid drop forms
- All vapor above this pressure
- Two-phase below this pressure

---

### Flash Calculations

#### `FlashResult` Dataclass

Result from a flash calculation.

**Module:** `src.thermo.thermo`

```python
@dataclass
class FlashResult:
    """
    Flash calculation result.
    
    Attributes:
        temperature (float): Temperature in K
        pressure (float): Pressure in Pa
        vapor_fraction (float): Vapor mole fraction (0 = all liquid, 1 = all vapor)
        vapor_mole_fractions (Dict[str, float]): Vapor phase composition
        liquid_mole_fractions (Dict[str, float]): Liquid phase composition
        converged (bool): Whether calculation converged
        iterations (int): Number of iterations required
    """
```

**Example:**
```python
result = Flash.isothermal_flash(...)

print(f"Converged: {result.converged}")
print(f"Iterations: {result.iterations}")
print(f"Vapor fraction: {result.vapor_fraction:.4f}")
print(f"Vapor composition: {result.vapor_mole_fractions}")
print(f"Liquid composition: {result.liquid_mole_fractions}")
```

---

#### `Flash` Class

Flash calculations for vapor-liquid separation.

**Module:** `src.thermo.thermo`

##### Methods

###### `isothermal_flash(temperature, pressure, feed_mole_fractions, components, max_iterations=100, tolerance=1e-6) -> FlashResult` (static)

Perform isothermal flash calculation using Rachford-Rice equation.

**Parameters:**
- `temperature` (float): Temperature in K
- `pressure` (float): Pressure in Pa
- `feed_mole_fractions` (Dict[str, float]): Feed composition
- `components` (Dict[str, Component]): Dictionary of components
- `max_iterations` (int, optional): Maximum iterations. Default: 100
- `tolerance` (float, optional): Convergence tolerance. Default: 1e-6

**Returns:**
- `FlashResult`: Flash calculation results

**Algorithm:**
1. Calculate K-values using Raoult's Law
2. Check if single phase (all K<1 or all K>1)
3. If two-phase, solve Rachford-Rice equation:
   ```
   f(V) = Σ[zi(Ki-1)/(1+V(Ki-1))] = 0
   ```
4. Use Newton-Raphson iteration to find V
5. Calculate phase compositions:
   ```
   xi = zi / [1 + V(Ki - 1)]
   yi = Ki · xi
   ```

**Example:**
```python
from src.thermo.thermo import Flash

feed = {'Water': 0.5, 'Methane': 0.5}
components = {'Water': water, 'Methane': methane}

result = Flash.isothermal_flash(
    temperature=320,
    pressure=500000,
    feed_mole_fractions=feed,
    components=components,
    max_iterations=100,
    tolerance=1e-6
)

if result.converged:
    print(f"Vapor fraction: {result.vapor_fraction:.4f}")
    print(f"Methane in vapor: {result.vapor_mole_fractions['Methane']:.4f}")
else:
    print("Flash did not converge!")
```

**Special Cases:**
- If all K ≤ 1: Returns all liquid (V=0)
- If all K ≥ 1: Returns all vapor (V=1)
- If two-phase: Solves for V between 0 and 1

**Notes:**
- Uses Newton-Raphson for fast convergence (typically 3-10 iterations)
- Material balance satisfied: zi = V·yi + (1-V)·xi
- Valid for ideal mixtures (Raoult's Law)

---

## 📐 Dimensional Analysis Module

### Dimensions

#### `Dimension` Class

Represents a physical dimension as combination of base dimensions.

**Module:** `src.dimanal.dim`

**Base Dimensions:** Length, Mass, Time, Temperature, Amount, Current, Luminosity, Angle, Solid Angle, Information

```python
@dataclass(frozen=True)
class Dimension:
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
```

##### Operators

```python
dim1 * dim2   # Multiply dimensions
dim1 / dim2   # Divide dimensions
dim ** n      # Power of dimension
dim1 == dim2  # Compare dimensions
```

**Example:**
```python
from src.dimanal.dim import LENGTH, TIME, VELOCITY

# Velocity = Length / Time
assert VELOCITY == LENGTH / TIME

# Area = Length²
from src.dimanal.dim import AREA
assert AREA == LENGTH ** 2
```

##### Predefined Dimensions

**Base:**
```python
DIMENSIONLESS, LENGTH, MASS, TIME, TEMPERATURE, AMOUNT, 
ELECTRIC_CURRENT, LUMINOUS_INTENSITY, PLANE_ANGLE, 
SOLID_ANGLE_DIM, INFORMATION_DIM
```

**Derived:**
```python
AREA, VOLUME, VELOCITY, ACCELERATION, FORCE, MOMENTUM,
ENERGY, POWER, PRESSURE, DENSITY, FREQUENCY,
ELECTRIC_CHARGE, VOLTAGE, RESISTANCE, CAPACITANCE,
and 50+ more...
```

---

### Units

#### `Unit` Class

Represents a unit of measurement.

**Module:** `src.dimanal.dim`

```python
@dataclass
class Unit:
    name: str
    symbol: str
    dimension: Dimension
    to_si: float          # Conversion factor to SI
    offset: float = 0.0   # Offset for temperature units
```

##### Methods

###### `with_prefix(prefix: Prefix) -> Unit`

Create a new unit with a prefix.

**Parameters:**
- `prefix` (Prefix): SI or binary prefix

**Returns:**
- `Unit`: New unit with prefix

**Example:**
```python
from src.dimanal.dim import METER, KILO, MILLI

km = METER.with_prefix(KILO)   # kilometer
mm = METER.with_prefix(MILLI)  # millimeter
```

---

###### `convert_to(value: float, target: Unit) -> float`

Convert a value to another unit.

**Parameters:**
- `value` (float): Value in this unit
- `target` (Unit): Target unit

**Returns:**
- `float`: Value in target unit

**Raises:**
- `DimensionError`: If dimensions don't match

**Example:**
```python
from src.dimanal.dim import MILE, FOOT

feet = MILE.convert_to(1.0, FOOT)  # 5280.0
```

---

##### Operators

```python
unit1 * unit2   # Multiply units
unit1 / unit2   # Divide units  
unit ** n       # Power of unit
```

##### Predefined Units (500+)

**Length:**
```python
METER, KILOMETER, CENTIMETER, MILLIMETER, MICROMETER, NANOMETER,
INCH, FOOT, YARD, MILE, NAUTICAL_MILE, ANGSTROM, LIGHT_YEAR, PARSEC
```

**Mass:**
```python
KILOGRAM, GRAM, MILLIGRAM, TONNE,
POUND, OUNCE, GRAIN, TROY_OUNCE, CARAT
```

**Time:**
```python
SECOND, MINUTE, HOUR, DAY, WEEK, YEAR_JULIAN, MONTH_30
```

**Temperature:**
```python
KELVIN, CELSIUS, FAHRENHEIT, RANKINE
```

**Pressure:**
```python
PASCAL, BAR, ATMOSPHERE, PSI, TORR, MMHG
```

**Energy:**
```python
JOULE, CALORIE, BTU, ELECTRONVOLT, WATT_HOUR, KILOWATT_HOUR
```

**Power:**
```python
WATT, KILOWATT, HORSEPOWER, HORSEPOWER_METRIC
```

**And many more categories...**

---

### Quantities

#### `Quantity` Class

A physical quantity: value + unit.

**Module:** `src.dimanal.dim`

```python
@dataclass
class Quantity:
    value: float
    unit: Unit
```

##### Methods

###### `to(target_unit: Unit) -> Quantity`

Convert quantity to different unit.

**Parameters:**
- `target_unit` (Unit): Target unit

**Returns:**
- `Quantity`: New quantity in target unit

**Raises:**
- `DimensionError`: If dimensions don't match

**Example:**
```python
from src.dimanal.dim import Q, METER, FOOT

length = Q(100, METER)
length_ft = length.to(FOOT)
print(length_ft)  # 328.084 ft
```

---

###### `to_si() -> Quantity`

Convert to SI base unit.

**Returns:**
- `Quantity`: Quantity in SI unit

**Example:**
```python
from src.dimanal.dim import Q, MILE, METER

dist = Q(1, MILE)
dist_si = dist.to_si()  # 1609.344 m
```

---

##### Arithmetic Operations

```python
q1 + q2   # Addition (same dimension required)
q1 - q2   # Subtraction (same dimension required)
q1 * q2   # Multiplication
q1 / q2   # Division
q ** n    # Power
-q        # Negation
abs(q)    # Absolute value
```

**Example:**
```python
from src.dimanal.dim import Q, METER, SECOND

distance = Q(100, METER)
time = Q(10, SECOND)

velocity = distance / time  # 10 m/s
area = distance * distance   # 10000 m²
```

##### Comparison Operations

```python
q1 == q2  # Equal (dimension-aware)
q1 < q2   # Less than
q1 <= q2  # Less than or equal
q1 > q2   # Greater than
q1 >= q2  # Greater than or equal
```

---

### Prefixes

#### `Prefix` Class

Represents a metric or binary prefix.

**Module:** `src.dimanal.dim`

```python
@dataclass(frozen=True)
class Prefix:
    name: str
    symbol: str
    factor: float
    base: int = 10
    exponent: int = 0
```

#### SI Prefixes

**Large:**
```python
QUETTA (Q, 10³⁰), RONNA (R, 10²⁷), YOTTA (Y, 10²⁴),
ZETTA (Z, 10²¹), EXA (E, 10¹⁸), PETA (P, 10¹⁵),
TERA (T, 10¹²), GIGA (G, 10⁹), MEGA (M, 10⁶), KILO (k, 10³)
```

**Small:**
```python
MILLI (m, 10⁻³), MICRO (μ, 10⁻⁶), NANO (n, 10⁻⁹),
PICO (p, 10⁻¹²), FEMTO (f, 10⁻¹⁵), ATTO (a, 10⁻¹⁸),
ZEPTO (z, 10⁻²¹), YOCTO (y, 10⁻²⁴), RONTO (r, 10⁻²⁷),
QUECTO (q, 10⁻³⁰)
```

#### Binary Prefixes (IEC)

```python
KIBI (Ki, 2¹⁰), MEBI (Mi, 2²⁰), GIBI (Gi, 2³⁰),
TEBI (Ti, 2⁴⁰), PEBI (Pi, 2⁵⁰), EXBI (Ei, 2⁶⁰),
ZEBI (Zi, 2⁷⁰), YOBI (Yi, 2⁸⁰)
```

---

### Physical Constants

#### Fundamental Constants (CODATA 2018/2022)

```python
SPEED_OF_LIGHT = 299792458           # m/s (exact)
PLANCK_CONSTANT = 6.62607015e-34     # J·s (exact)
ELEMENTARY_CHARGE = 1.602176634e-19  # C (exact)
BOLTZMANN_CONSTANT = 1.380649e-23    # J/K (exact)
AVOGADRO_NUMBER = 6.02214076e23      # mol⁻¹ (exact)
GRAVITATIONAL_CONSTANT = 6.67430e-11 # m³/(kg·s²)
```

#### Engineering Constants

```python
GAS_CONSTANT = 8.314462618           # J/(mol·K)
STANDARD_GRAVITY = 9.80665           # m/s² (exact)
STANDARD_ATMOSPHERE = 101325         # Pa (exact)
FARADAY_CONSTANT = 96485.33212       # C/mol
```

#### Astronomical Constants

```python
ASTRONOMICAL_UNIT = 149597870700     # m (exact)
LIGHT_YEAR = 9460730472580800        # m
PARSEC = 3.0856775814913673e16       # m
SOLAR_MASS = 1.98892e30              # kg
EARTH_MASS = 5.9722e24               # kg
```

---

### Helper Functions

#### `Q(value: float, unit: Union[Unit, str]) -> Quantity`

Shorthand for creating a Quantity.

**Parameters:**
- `value` (float): Numerical value
- `unit` (Union[Unit, str]): Unit object or unit symbol/name

**Returns:**
- `Quantity`: New quantity

**Example:**
```python
from src.dimanal.dim import Q

length = Q(5.0, "m")      # Using string
temp = Q(25, "°C")        # Using string
pressure = Q(10, "bar")   # Using string
```

---

#### `convert(value: float, from_unit: Union[Unit, str], to_unit: Union[Unit, str]) -> float`

Convert a value between units.

**Parameters:**
- `value` (float): Value to convert
- `from_unit` (Union[Unit, str]): Source unit
- `to_unit` (Union[Unit, str]): Target unit

**Returns:**
- `float`: Converted value

**Example:**
```python
from src.dimanal.dim import convert

meters = convert(100, "ft", "m")        # 30.48
celsius = convert(77, "°F", "°C")       # 25.0
bars = convert(14.7, "psi", "bar")      # 1.0133
```

---

#### `get_unit(identifier: str) -> Unit`

Get a unit by symbol or name.

**Parameters:**
- `identifier` (str): Unit symbol or name

**Returns:**
- `Unit`: Unit object

**Raises:**
- `UnitError`: If unit not found

**Example:**
```python
from src.dimanal.dim import get_unit

m = get_unit("m")         # METER
kg = get_unit("kilogram") # KILOGRAM
```

---

## 🛠️ Utility Functions

### Constants

```python
# Universal gas constant
from src.thermo.thermo import R, R_KMOL

R       # 8.314462 J/(mol·K)
R_KMOL  # 8314.462 J/(kmol·K)
```

---

## ⚠️ Error Handling

### Exceptions

#### `ValueError`

Raised for invalid input parameters.

**Common Cases:**
- Empty component name
- Zero or negative molecular weight
- Zero or negative temperature
- Zero or negative pressure
- Negative flow rate
- Mole fractions not summing to 1.0
- Missing required coefficients

**Example:**
```python
try:
    component = Component(name="", formula="H2O", molecular_weight=18)
except ValueError as e:
    print(f"Error: {e}")  # "Component name cannot be empty"
```

---

#### `AttributeError`

Raised when required data is missing.

**Common Cases:**
- Calling `vapor_pressure()` without Antoine coefficients
- Calling `cp_ideal_gas()` without Cp coefficients

**Example:**
```python
try:
    comp = Component(name="Test", formula="T", molecular_weight=10)
    p_sat = comp.vapor_pressure(300)
except ValueError as e:
    print(f"Error: {e}")  # "Antoine coefficients not defined"
```

---

#### `DimensionError`

Raised for dimensional mismatches (dimanal module).

**Common Cases:**
- Adding quantities with different dimensions
- Converting between incompatible units

**Example:**
```python
from src.dimanal.dim import Q, METER, SECOND, DimensionError

try:
    result = Q(5, METER) + Q(10, SECOND)
except DimensionError as e:
    print(f"Error: {e}")
```

---

#### `UnitError`

Raised for unit-related errors (dimanal module).

**Common Cases:**
- Unknown unit symbol or name

**Example:**
```python
from src.dimanal.dim import get_unit, UnitError

try:
    unit = get_unit("xyz")
except UnitError as e:
    print(f"Error: {e}")  # "Unknown unit: xyz"
```

---

## 🔤 Type Hints Reference

### Common Types

```python
from typing import Dict, List, Optional, Tuple, Union

# Component types
ComponentDict = Dict[str, Component]
MoleFractionDict = Dict[str, float]

# Thermodynamic types
KValueDict = Dict[str, float]
CompositionDict = Dict[str, float]

# Return types
ParameterTuple = Tuple[float, float]  # (a, b) for EOS
```

### Function Signatures

```python
# Component
def vapor_pressure(self, temperature: float) -> float: ...
def cp_ideal_gas(self, temperature: float) -> float: ...
def to_dict(self) -> Dict[str, Any]: ...

# Stream
def molecular_weight(self) -> float: ...
def mix_with(self, other: Stream) -> Stream: ...
def split(self, fraction: float, name_suffix: str = "_split") -> Stream: ...

# Thermodynamics
def molar_volume(temperature: float, pressure: float, 
                 component: Component, phase: str = 'vapor') -> float: ...

def isothermal_flash(temperature: float, pressure: float,
                     feed_mole_fractions: Dict[str, float],
                     components: Dict[str, Component],
                     max_iterations: int = 100,
                     tolerance: float = 1e-6) -> FlashResult: ...
```

---

## 📚 Examples

### Example 1: Simple Property Calculation

```python
from src.core.component import create_water

# Create water
water = create_water()

# Calculate properties at 100°C
T = 373.15  # K

# Vapor pressure (should be ~1 atm)
p_sat = water.vapor_pressure(T)
print(f"Vapor pressure: {p_sat/1e5:.4f} bar")  # ~1.0133 bar

# Heat capacity
cp = water.cp_ideal_gas(T)
print(f"Heat capacity: {cp:.1f} J/(kmol·K)")

# Reduced temperature
Tr = water.reduced_temperature(T)
print(f"Reduced temperature: {Tr:.4f}")  # ~0.577
```

---

### Example 2: Stream Mixing

```python
from src.core.component import create_water, create_methane
from src.core.stream import Stream, UnitConversion

# Create components
water = create_water()
methane = create_methane()

# Create two streams
stream1 = Stream(
    name="Hot Water",
    temperature=UnitConversion.celsius_to_kelvin(80),
    pressure=UnitConversion.bar_to_pascal(2),
    components={'Water': water},
    mole_fractions={'Water': 1.0},
    molar_flow=50.0
)

stream2 = Stream(
    name="Cold Methane",
    temperature=UnitConversion.celsius_to_kelvin(25),
    pressure=UnitConversion.bar_to_pascal(2),
    components={'Methane': methane},
    mole_fractions={'Methane': 1.0},
    molar_flow=30.0
)

# Mix streams
mixed = stream1.mix_with(stream2)

# Display results
print(mixed.summary())
```

---

### Example 3: Flash Calculation

```python
from src.core.component import create_water, create_methane
from src.thermo.thermo import Flash, VLE

# Setup
water = create_water()
methane = create_methane()
components = {'Water': water, 'Methane': methane}

# Operating conditions
T = 320  # K
P = 500000  # Pa (5 bar)
feed = {'Water': 0.4, 'Methane': 0.6}

# Calculate K-values first
k_values = VLE.raoult_law_k_values(T, P, components)
print("K-values:")
for name, k in k_values.items():
    print(f"  {name}: {k:.4f}")

# Perform flash
result = Flash.isothermal_flash(T, P, feed, components)

# Display results
print(f"\nFlash Results:")
print(f"  Converged: {result.converged}")
print(f"  Iterations: {result.iterations}")
print(f"  Vapor fraction: {result.vapor_fraction:.4f}")

print(f"\nVapor composition:")
for name, y in result.vapor_mole_fractions.items():
    print(f"  {name}: {y:.4f}")

print(f"\nLiquid composition:")
for name, x in result.liquid_mole_fractions.items():
    print(f"  {name}: {x:.4f}")

# Verify material balance
print(f"\nMaterial Balance Check:")
V = result.vapor_fraction
for name in feed:
    z = feed[name]
    y = result.vapor_mole_fractions[name]
    x = result.liquid_mole_fractions[name]
    z_calc = V * y + (1 - V) * x
    print(f"  {name}: z={z:.4f}, calculated={z_calc:.4f}, error={abs(z-z_calc):.2e}")
```

---

### Example 4: Equation of State Comparison

```python
from src.core.component import create_methane
from src.thermo.thermo import IdealGas, VanDerWaalsEOS, RedlichKwongEOS

# Setup
methane = create_methane()
T = 300  # K
P = 5e6  # Pa (50 bar)

# Calculate with different models
V_ideal = IdealGas.molar_volume(T, P)
V_vdw = VanDerWaalsEOS.molar_volume(T, P, methane, 'vapor')
V_rk = RedlichKwongEOS.molar_volume(T, P, methane, 'vapor')

# Compressibility factors
Z_ideal = IdealGas.compressibility_factor()
Z_vdw = VanDerWaalsEOS.compressibility_factor(T, P, methane, 'vapor')
Z_rk = RedlichKwongEOS.compressibility_factor(T, P, methane, 'vapor')

# Display results
print(f"Conditions: {T}K, {P/1e6:.1f} MPa")
print(f"\n{'Model':<15} {'V (m³/kmol)':<15} {'Z':<10}")
print("-" * 40)
print(f"{'Ideal Gas':<15} {V_ideal:>10.4f}      {Z_ideal:>8.4f}")
print(f"{'van der Waals':<15} {V_vdw:>10.4f}      {Z_vdw:>8.4f}")
print(f"{'Redlich-Kwong':<15} {V_rk:>10.4f}      {Z_rk:>8.4f}")
```

---

### Example 5: Unit Conversion with Dimensional Analysis

```python
from src.dimanal.dim import Q, convert, CELSIUS, KELVIN, BAR, PSI

# Method 1: Using Quantity objects
temp_c = Q(25, CELSIUS)
temp_k = temp_c.to(KELVIN)
print(f"{temp_c} = {temp_k}")  # 25 °C = 298.15 K

# Method 2: Using convert function
pressure_psi = 14.7
pressure_bar = convert(pressure_psi, PSI, BAR)
print(f"{pressure_psi} psi = {pressure_bar:.4f} bar")

# Method 3: Using string identifiers
temp_k = convert(100, "°C", "K")
print(f"100 °C = {temp_k} K")

# Compound units
from src.dimanal.dim import METER, SECOND

distance = Q(100, METER)
time = Q(10, SECOND)
velocity = distance / time
print(f"Velocity: {velocity}")  # 10.0 m/s
```

---

## 🔄 Migration Guide

### Version 0.1.0 (Current)

Initial release - no migrations needed.

### Future Versions

Migration guides will be added for breaking changes in future versions.

---

## 📝 Notes

### Performance Tips

1. **Avoid repeated property calculations** - Cache results if calling multiple times
2. **Use appropriate EOS** - IdealGas is fastest, use for low-pressure gases
3. **Flash calculations** - Provide good initial guesses for faster convergence
4. **Batch operations** - Process multiple streams together when possible

### Best Practices

1. **Always specify units** - Use conversion utilities, don't assume
2. **Validate inputs** - Check ranges before calculations
3. **Handle exceptions** - Wrap calculations in try-except blocks
4. **Check convergence** - Always check `converged` flag in flash results
5. **Document units** - Comment units in your code clearly

### Common Pitfalls

1. **Unit confusion** - Mixing K and °C, Pa and bar
2. **Mole fractions** - Forgetting to normalize (sum to 1.0)
3. **Antoine range** - Using outside valid temperature range
4. **Phase specification** - Not specifying 'vapor' or 'liquid' for EOS
5. **Convergence** - Not checking if flash converged

---

## 🆘 Support

### Getting Help

- **Documentation**: Read this API reference and ARCHITECTURE.md
- **Examples**: Check `examples/` directory
- **Tests**: Review `tests/` for usage examples
- **Issues**: Report bugs on GitHub

### Contributing

See CONTRIBUTING.md for guidelines on:
- Adding new components
- Adding new thermodynamic models
- Adding new unit operations
- Improving documentation

---

## 📄 License

MIT License - See LICENSE file for details

---

## 📚 References

### Thermodynamics
- Smith, Van Ness & Abbott - "Introduction to Chemical Engineering Thermodynamics"
- Perry's Chemical Engineers' Handbook
- NIST Chemistry WebBook

### Software
- Python Documentation - https://docs.python.org/
- NumPy Documentation - https://numpy.org/doc/
- SciPy Documentation - https://scipy.org/doc/

---

**Last Updated:** November 2025  
**Version:** 0.1.0-dev  
**Status:** Phase 1 Complete

For the latest updates, visit: https://github.com/yourusername/plant-simulation-software
