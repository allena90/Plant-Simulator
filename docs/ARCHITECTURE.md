# Software Architecture Documentation
## Industrial Plant Simulation Software

**Version:** 0.1.0-dev  
**Last Updated:** November 2025  
**Status:** Phase 1 Complete, Phase 2 In Progress

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [System Architecture](#system-architecture)
4. [Module Architecture](#module-architecture)
5. [Data Flow](#data-flow)
6. [Class Diagrams](#class-diagrams)
7. [Design Patterns](#design-patterns)
8. [API Design](#api-design)
9. [Extension Points](#extension-points)
10. [Performance Considerations](#performance-considerations)
11. [Future Architecture](#future-architecture)

---

## 🎯 Overview

### Purpose

This software is an educational chemical process simulation system designed to model steady-state and dynamic industrial processes. It provides thermodynamic calculations, unit operation models, and flowsheet solving capabilities.

### Target Users

- Chemical engineering students
- Process engineers (learning/educational purposes)
- Researchers exploring process simulation concepts
- Developers learning about process modeling software

### Scope

**Phase 1 (Current):** Foundation - Core data structures and thermodynamics  
**Phase 2-10:** Unit operations, solvers, GUI, dynamics, optimization

### Key Design Goals

1. **Educational clarity** over industrial complexity
2. **Extensibility** - easy to add new components, units, models
3. **Modularity** - independent, testable components
4. **Type safety** - comprehensive type hints
5. **Testability** - >80% code coverage
6. **Documentation** - every public API documented

---

## 🏛️ Design Philosophy

### Core Principles

#### 1. **Separation of Concerns**

Each module has a single, well-defined responsibility:

```
Component      → Chemical compound properties
Stream         → Material flows between units
Thermodynamics → Property calculations and phase equilibrium
Units          → Equipment models (mixers, reactors, etc.)
Solver         → Flowsheet convergence algorithms
```

#### 2. **Immutability Where Appropriate**

- Components are immutable after creation (frozen dataclass)
- Streams can be modified but copying is encouraged
- Calculation results are returned as new objects

#### 3. **Explicit Over Implicit**

- Units are always specified (K, Pa, kmol/s)
- No "magic" conversions
- Clear method names (e.g., `celsius_to_kelvin` not `convert_temp`)

#### 4. **Fail Fast**

- Input validation on construction
- Type hints enforced
- Raise exceptions for invalid states
- No silent failures

#### 5. **Progressive Enhancement**

- Start with simple models (ideal gas)
- Add complexity as needed (real gas, non-ideal)
- Allow model selection by user

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (GUI / CLI / API)                         │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Flowsheet  │  │   Solver     │  │  Optimizer   │     │
│  │   Manager    │  │   Engine     │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────┐
│                     Domain Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Units     │  │   Streams    │  │  Dynamics    │     │
│  │  Operations  │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────┐
│                   Foundation Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Components  │  │    Thermo    │  │   Dimanal    │     │
│  │              │  │              │  │   (Units)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### **Foundation Layer** (Phase 1 - ✅ Complete)

**Purpose:** Core data structures and fundamental calculations

**Modules:**
- `src.core.component` - Chemical compound definitions
- `src.core.stream` - Material flow representation
- `src.thermo.thermo` - Thermodynamic models and calculations
- `src.dimanal.dim` - Dimensional analysis and unit system

**Dependencies:** Only external scientific libraries (NumPy, SciPy)

**Characteristics:**
- No dependencies on upper layers
- Stateless calculations
- Pure functions where possible
- Comprehensive unit tests

#### **Domain Layer** (Phase 2-3 - In Progress)

**Purpose:** Process engineering domain models

**Modules:**
- `src.units` - Unit operation models
- `src.dynamics` - Dynamic simulation components
- `src.thermo` (advanced) - Advanced property models

**Dependencies:** Foundation layer only

**Characteristics:**
- Encapsulates engineering knowledge
- Stateful operations (equipment has state)
- Material and energy balances
- Convergence and iteration

#### **Application Layer** (Phase 4-7 - Planned)

**Purpose:** Orchestration and high-level workflows

**Modules:**
- `src.solver` - Flowsheet solving algorithms
- `src.optimizer` - Optimization routines
- `src.flowsheet` - Flowsheet management

**Dependencies:** Foundation + Domain layers

**Characteristics:**
- Coordinates multiple units
- Manages calculation sequences
- Handles convergence
- Provides high-level API

#### **Interface Layer** (Phase 5, 8-10 - Planned)

**Purpose:** User interaction and I/O

**Modules:**
- `src.gui` - Graphical user interface
- `src.cli` - Command-line interface
- `src.api` - Programmatic API

**Dependencies:** All lower layers

**Characteristics:**
- User input handling
- Visualization
- File I/O
- External integration

---

## 📦 Module Architecture

### Core Module (`src.core`)

#### Component (`component.py`)

**Purpose:** Represent chemical compounds with properties

**Architecture:**

```python
@dataclass
class Component:
    """Immutable chemical compound definition"""
    
    # Identification
    name: str
    formula: str
    cas_number: str
    
    # Critical Properties
    critical_temperature: float
    critical_pressure: float
    critical_volume: float
    acentric_factor: float
    
    # Correlations
    antoine_a, antoine_b, antoine_c: float  # Vapor pressure
    cp_ideal_gas_a, b, c, d: float          # Heat capacity
    
    # Methods (pure functions)
    def vapor_pressure(T: float) -> float
    def cp_ideal_gas(T: float) -> float
    def reduced_temperature(T: float) -> float
    def reduced_pressure(P: float) -> float
    
    # Serialization
    def to_dict() -> Dict
    @classmethod
    def from_dict(data: Dict) -> Component
```

**Design Decisions:**
- ✅ Dataclass for clean syntax and automatic methods
- ✅ Frozen to prevent accidental modification
- ✅ Type hints for all attributes
- ✅ Property calculations as methods (not cached)
- ✅ No dependencies on other modules

**Extension Points:**
- Add new properties (e.g., viscosity, surface tension)
- Add new correlations (e.g., DIPPR equations)
- Support different units (currently SI)

#### Stream (`stream.py`)

**Purpose:** Represent material flows with thermodynamic state

**Architecture:**

```python
@dataclass
class Stream:
    """Material flow with state"""
    
    # State Variables
    name: str
    temperature: float              # K
    pressure: float                 # Pa
    molar_flow: float              # kmol/s
    phase: str                     # 'vapor', 'liquid', 'mixed'
    
    # Composition
    components: Dict[str, Component]
    mole_fractions: Dict[str, float]
    
    # Property Calculations
    def molecular_weight() -> float
    def mass_flow() -> float
    def component_molar_flows() -> Dict[str, float]
    def component_mass_flows() -> Dict[str, float]
    def mass_fractions() -> Dict[str, float]
    
    # Operations (return new streams)
    def copy() -> Stream
    def mix_with(other: Stream) -> Stream
    def split(fraction: float) -> Stream
    
    # Thermodynamic Properties
    def ideal_gas_density() -> float
    def enthalpy_ideal_gas() -> float
```

**Design Decisions:**
- ✅ Mutable by default (process streams change)
- ✅ Composition stored as dict for flexibility
- ✅ Operations return new streams (immutable pattern)
- ✅ Validation in `__post_init__`
- ✅ Components stored by reference (not copied)

**Key Features:**
- Material balance enforcement
- Energy balance in mixing
- Component tracking
- Phase state tracking

**Extension Points:**
- Add enthalpy/entropy calculations
- Support solids (three-phase)
- Add stream specifications (e.g., "saturated liquid")
- Stream property caching for performance

---

### Thermodynamics Module (`src.thermo`)

#### Architecture Overview

```python
# Equations of State
class IdealGas:
    @staticmethod
    def molar_volume(T, P) -> float
    @staticmethod
    def compressibility_factor() -> float

class VanDerWaalsEOS:
    @staticmethod
    def calculate_parameters(comp) -> Tuple[float, float]
    @staticmethod
    def molar_volume(T, P, comp, phase) -> float
    @staticmethod
    def compressibility_factor(T, P, comp, phase) -> float

class RedlichKwongEOS:
    # Similar structure to VanDerWaalsEOS
    ...

# Vapor-Liquid Equilibrium
class VLE:
    @staticmethod
    def raoult_law_k_values(T, P, components) -> Dict[str, float]
    @staticmethod
    def bubble_point_pressure(T, x, components) -> float
    @staticmethod
    def dew_point_pressure(T, y, components) -> float

# Flash Calculations
@dataclass
class FlashResult:
    temperature: float
    pressure: float
    vapor_fraction: float
    vapor_mole_fractions: Dict[str, float]
    liquid_mole_fractions: Dict[str, float]
    converged: bool
    iterations: int

class Flash:
    @staticmethod
    def isothermal_flash(T, P, feed, components, 
                         max_iterations, tolerance) -> FlashResult
```

**Design Decisions:**
- ✅ Static methods (stateless calculations)
- ✅ Separate classes for each model (Single Responsibility)
- ✅ FlashResult dataclass for structured output
- ✅ No mutable state
- ✅ Explicit parameters (no global state)

**Key Algorithms:**
- Cubic equation solving (for EOS)
- Newton-Raphson iteration (for flash)
- Rachford-Rice equation
- Material balance closure

**Extension Points:**
- Add more EOS (Peng-Robinson, SRK, SAFT)
- Add activity coefficient models (NRTL, UNIQUAC, UNIFAC)
- Add enthalpy/entropy calculations
- Support three-phase flash
- Add adiabatic flash
- Add T-P flash (specify T, find P and compositions)

---

### Dimensional Analysis Module (`src.dimanal`)

#### Architecture Overview

```python
# Prefix System
@dataclass(frozen=True)
class Prefix:
    name: str
    symbol: str
    factor: float
    base: int
    exponent: int

# SI Prefixes (quecto to quetta)
KILO, MEGA, GIGA, MILLI, MICRO, NANO, ...

# Dimension System
@dataclass(frozen=True)
class Dimension:
    length: int
    mass: int
    time: int
    temperature: int
    amount: int
    current: int
    luminosity: int
    angle: int
    solid_angle: int
    information: int
    
    def __mul__(other) -> Dimension
    def __truediv__(other) -> Dimension
    def __pow__(power) -> Dimension

# Predefined Dimensions
LENGTH, MASS, TIME, TEMPERATURE, AMOUNT, ...
AREA, VOLUME, VELOCITY, FORCE, ENERGY, POWER, ...

# Unit System
@dataclass
class Unit:
    name: str
    symbol: str
    dimension: Dimension
    to_si: float
    offset: float
    
    def with_prefix(prefix: Prefix) -> Unit
    def convert_to(value, target: Unit) -> float
    def __mul__(other: Unit) -> Unit
    def __truediv__(other: Unit) -> Unit

# Quantity System
@dataclass
class Quantity:
    value: float
    unit: Unit
    
    def to(target: Unit) -> Quantity
    def __add__(other: Quantity) -> Quantity
    def __mul__(other: Union[Quantity, float]) -> Quantity
    # ... arithmetic operations

# Unit Registry
class UnitRegistry:
    def register(unit: Unit)
    def get(identifier: str) -> Unit
    def units_for_dimension(dim: Dimension) -> List[Unit]
```

**Design Decisions:**
- ✅ Immutable dimensions and prefixes (frozen dataclass)
- ✅ Operator overloading for natural syntax
- ✅ Type-safe dimensional arithmetic
- ✅ Comprehensive unit library (500+ units)
- ✅ Automatic conversion with dimension checking

**Key Features:**
- Dimensional analysis enforcement
- Automatic unit conversion
- Physical constants library
- Support for compound units
- SI and non-SI units

---

## 🔄 Data Flow

### Component Property Calculation Flow

```
User Request
    ↓
Component.vapor_pressure(T)
    ↓
Check antoine coefficients exist
    ↓
Validate temperature range (warning if outside)
    ↓
Calculate: log10(P) = A - B/(T+C)
    ↓
Return pressure in Pa
```

### Stream Mixing Flow

```
stream1.mix_with(stream2)
    ↓
Validate inputs (both streams valid)
    ↓
Calculate total molar flow: n_out = n1 + n2
    ↓
Calculate component flows for each component:
    n_i,out = n_i,1 + n_i,2
    ↓
Calculate outlet composition:
    x_i,out = n_i,out / n_out
    ↓
Calculate outlet pressure: P_out = min(P1, P2)
    ↓
Calculate outlet temperature (mass-weighted):
    T_out = (m1*T1 + m2*T2) / (m1 + m2)
    ↓
Create and return new Stream
```

### Flash Calculation Flow

```
Flash.isothermal_flash(T, P, feed, components)
    ↓
Calculate K-values: Ki = Pi_sat(T) / P
    ↓
Check if single phase:
    - If all Ki ≤ 1: all liquid (V=0)
    - If all Ki ≥ 1: all vapor (V=1)
    ↓
If two-phase, solve Rachford-Rice:
    f(V) = Σ[zi(Ki-1)/(1+V(Ki-1))] = 0
    ↓
Newton-Raphson iteration:
    V_new = V - f(V)/f'(V)
    ↓
Check convergence: |f(V)| < tolerance
    ↓
Calculate phase compositions:
    xi = zi/[1+V(Ki-1)]
    yi = Ki·xi
    ↓
Return FlashResult with all information
```

### Future: Flowsheet Solving Flow (Phase 4)

```
Flowsheet.solve()
    ↓
Analyze topology (graph)
    ↓
Identify recycle loops
    ↓
Select tear streams
    ↓
Determine calculation order (topological sort)
    ↓
Initialize tear stream guesses
    ↓
Iteration loop:
    │
    ├→ Calculate each unit in order
    │   ↓
    │   Update stream properties
    │   ↓
    │   Check material/energy balance
    │
    ├→ Check convergence:
    │   |tear_new - tear_old| < tolerance
    │
    └→ Update tear streams (with acceleration)
    ↓
Return converged flowsheet
```

---

## 📊 Class Diagrams

### Foundation Layer Class Diagram

```
┌─────────────────────┐
│    Component        │
├─────────────────────┤
│ + name: str         │
│ + formula: str      │
│ + molecular_weight  │
│ + Tc, Pc, Vc, ω    │
│ + antoine_a,b,c     │
├─────────────────────┤
│ + vapor_pressure()  │
│ + cp_ideal_gas()    │
│ + to_dict()         │
└─────────────────────┘
          △
          │ contains
          │ 0..*
          │
┌─────────────────────┐
│      Stream         │
├─────────────────────┤
│ + temperature       │
│ + pressure          │
│ + molar_flow        │
│ + components: Dict  │
│ + mole_fractions    │
├─────────────────────┤
│ + mix_with()        │
│ + split()           │
│ + mass_flow()       │
└─────────────────────┘
          │
          │ uses
          ▼
┌─────────────────────┐     ┌─────────────────────┐
│  ThermodynamicModel │────▶│    FlashResult      │
├─────────────────────┤     ├─────────────────────┤
│ IdealGas            │     │ + vapor_fraction    │
│ VanDerWaalsEOS      │     │ + vapor_comp        │
│ RedlichKwongEOS     │     │ + liquid_comp       │
│ VLE                 │     │ + converged         │
│ Flash               │     └─────────────────────┘
└─────────────────────┘
```

### Future: Unit Operations Class Diagram

```
┌─────────────────────────────┐
│     UnitOperation           │  (Abstract Base)
├─────────────────────────────┤
│ + name: str                 │
│ + inlets: List[Stream]      │
│ + outlets: List[Stream]     │
├─────────────────────────────┤
│ + calculate() (abstract)    │
│ + validate()                │
│ + material_balance()        │
│ + energy_balance()          │
└─────────────────────────────┘
              △
              │
     ┌────────┴────────┬────────────────┐
     │                 │                │
┌─────────┐      ┌──────────┐    ┌─────────────┐
│  Mixer  │      │ Splitter │    │ HeatExchngr │
├─────────┤      ├──────────┤    ├─────────────┤
│ N→1     │      │ 1→M      │    │ 2→2         │
└─────────┘      └──────────┘    └─────────────┘
```

---

## 🎨 Design Patterns

### 1. **Strategy Pattern** (Thermodynamic Models)

**Problem:** Multiple ways to calculate properties (Ideal, vdW, RK, PR, etc.)

**Solution:** Each model is a separate class with same interface

```python
# All EOS have same interface
class EquationOfState(ABC):
    @abstractmethod
    def molar_volume(T, P, component, phase) -> float:
        pass
    
    @abstractmethod
    def compressibility_factor(T, P, component, phase) -> float:
        pass

# User can choose model
eos = VanDerWaalsEOS()  # or RedlichKwongEOS() or PengRobinsonEOS()
V = eos.molar_volume(T, P, component, 'vapor')
```

**Benefits:**
- Easy to add new models
- Models are independent
- User controls selection

### 2. **Factory Pattern** (Component Creation)

**Problem:** Complex component initialization with many parameters

**Solution:** Factory functions for common components

```python
# Factory functions
def create_water() -> Component:
    return Component(
        name="Water",
        formula="H2O",
        molecular_weight=18.015,
        critical_temperature=647.1,
        # ... many parameters ...
    )

# User can use factories or create custom
water = create_water()  # Easy
custom = Component(...)  # Still possible
```

**Benefits:**
- Simplified component creation
- Pre-validated common components
- Still allows custom components

### 3. **Immutable Data Pattern** (Component)

**Problem:** Components should not change after creation

**Solution:** Frozen dataclass

```python
@dataclass(frozen=True)
class Component:
    name: str
    molecular_weight: float
    # ...

# Cannot modify
water = create_water()
water.name = "Steam"  # FrozenInstanceError
```

**Benefits:**
- Thread-safe
- No accidental modification
- Cache-friendly

### 4. **Builder Pattern** (Future: Flowsheet)

**Problem:** Complex flowsheet construction with many units and connections

**Solution:** Fluent API for building

```python
# Future implementation
flowsheet = (FlowsheetBuilder()
    .add_feed_stream("feed", composition={...})
    .add_mixer("M-101", inlets=["S1", "S2"])
    .add_flash("V-101", temperature=320, pressure=500000)
    .add_splitter("SP-101", fractions=[0.7, 0.3])
    .connect("M-101", "out", "V-101", "in")
    .build()
)
```

### 5. **Observer Pattern** (Future: Flowsheet Events)

**Problem:** Track calculation progress, convergence, errors

**Solution:** Event system

```python
# Future implementation
flowsheet.on_unit_calculated += log_calculation
flowsheet.on_convergence += update_gui
flowsheet.on_error += handle_error
```

### 6. **Template Method Pattern** (Future: Unit Operations)

**Problem:** All units follow same pattern but have different calculations

**Solution:** Base class with template method

```python
class UnitOperation(ABC):
    def calculate(self):
        """Template method"""
        self.validate_inputs()
        self._calculate()  # Subclass implements
        self.validate_outputs()
        self.check_balances()
    
    @abstractmethod
    def _calculate(self):
        """Subclass implements specific calculation"""
        pass
```

---

## 🔌 API Design

### Public API Surface

#### Component API

```python
# Creation
from src.core.component import Component, create_water, create_methane

water = create_water()
custom = Component(name="Custom", formula="C2H6", ...)

# Properties
p_sat = water.vapor_pressure(373.15)  # Pa
cp = water.cp_ideal_gas(300)  # J/(kmol·K)
Tr = water.reduced_temperature(400)  # dimensionless

# Serialization
data = water.to_dict()
restored = Component.from_dict(data)
```

#### Stream API

```python
# Creation
from src.core.stream import Stream, UnitConversion

stream = Stream(
    name="Feed",
    temperature=UnitConversion.celsius_to_kelvin(25),
    pressure=UnitConversion.bar_to_pascal(10),
    components={'Water': water},
    mole_fractions={'Water': 1.0},
    molar_flow=100.0
)

# Properties
mw = stream.molecular_weight()  # kg/kmol
m_dot = stream.mass_flow()  # kg/s
rho = stream.ideal_gas_density()  # kg/m³

# Operations
mixed = stream1.mix_with(stream2)
split1 = stream.split(0.7)
copy = stream.copy()

# Display
print(stream.summary())
```

#### Thermodynamics API

```python
from src.thermo.thermo import (
    IdealGas, VanDerWaalsEOS, RedlichKwongEOS,
    VLE, Flash
)

# EOS
V_ideal = IdealGas.molar_volume(T, P)
V_vdw = VanDerWaalsEOS.molar_volume(T, P, component, 'vapor')
Z = RedlichKwongEOS.compressibility_factor(T, P, component, 'vapor')

# VLE
k_values = VLE.raoult_law_k_values(T, P, components)
P_bubble = VLE.bubble_point_pressure(T, x, components)
P_dew = VLE.dew_point_pressure(T, y, components)

# Flash
result = Flash.isothermal_flash(T, P, feed, components)
print(f"Vapor fraction: {result.vapor_fraction}")
print(f"Vapor: {result.vapor_mole_fractions}")
print(f"Liquid: {result.liquid_mole_fractions}")
```

#### Unit Conversion API

```python
from src.core.stream import UnitConversion

# Temperature
T_k = UnitConversion.celsius_to_kelvin(25)
T_c = UnitConversion.kelvin_to_celsius(373.15)

# Pressure
P_pa = UnitConversion.bar_to_pascal(10)
P_bar = UnitConversion.pascal_to_bar(101325)

# Flow
flow_h = UnitConversion.kmol_s_to_kmol_h(10)
```

#### Dimensional Analysis API

```python
from src.dimanal.dim import Q, convert, METER, FOOT, CELSIUS, KELVIN

# Create quantities
length = Q(5, METER)
temp = Q(25, CELSIUS)

# Convert
length_ft = length.to(FOOT)
temp_k = temp.to(KELVIN)

# Arithmetic with dimension checking
area = length * length  # Dimension: L²
velocity = length / Q(2, SECOND)  # Dimension: L/T

# Simple conversion
meters = convert(100, FOOT, METER)
```

### API Design Principles

1. **Explicit is better than implicit**
   - Always specify units
   - No hidden conversions
   - Clear parameter names

2. **Consistent naming**
   - `calculate_*` for calculations
   - `get_*` for retrieval
   - `to_*` for conversions

3. **Type hints everywhere**
   - All parameters typed
   - All returns typed
   - Use Optional, Union, Dict as needed

4. **Validation at boundaries**
   - Validate in `__init__` or `__post_init__`
   - Raise ValueError for invalid inputs
   - Clear error messages

5. **Return structured data**
   - Use dataclasses for complex results
   - Avoid long tuples
   - Document return values

---

## 🔧 Extension Points

### Adding New Components

**Location:** `src/core/component.py`

**Steps:**
1. Create factory function following pattern
2. Gather property data from DIPPR, NIST, or literature
3. Validate against known values
4. Add tests

**Example:**
```python
def create_ethane() -> Component:
    return Component(
        name="Ethane",
        formula="C2H6",
        cas_number="74-84-0",
        molecular_weight=30.07,
        critical_temperature=305.3,
        critical_pressure=4.872e6,
        acentric_factor=0.099,
        # ... more properties
    )
```

### Adding New Equations of State

**Location:** `src/thermo/thermo.py` or new file

**Steps:**
1. Create class following pattern (static methods)
2. Implement `calculate_parameters`
3. Implement `molar_volume`
4. Implement `compressibility_factor`
5. Add tests comparing to literature

**Example:**
```python
class PengRobinsonEOS:
    @staticmethod
    def calculate_parameters(component: Component) -> Tuple[float, float]:
        # Calculate a and b from Tc, Pc, ω
        ...
    
    @staticmethod
    def molar_volume(T, P, component, phase='vapor') -> float:
        # Solve cubic equation
        ...
```

### Adding New Unit Operations (Phase 2)

**Location:** `src/units/`

**Steps:**
1. Create class inheriting from `UnitOperation` (base class)
2. Define inlets and outlets
3. Implement `calculate()` method
4. Implement material balance
5. Implement energy balance
6. Add tests with known solutions

**Pattern:**
```python
class Mixer(UnitOperation):
    def __init__(self, name: str):
        super().__init__(name)
        self.inlets: List[Stream] = []
        self.outlet: Optional[Stream] = None
    
    def add_inlet(self, stream: Stream):
        self.inlets.append(stream)
    
    def calculate(self):
        # Mix all inlets
        result = self.inlets[0].copy()
        for inlet in self.inlets[1:]:
            result = result.mix_with(inlet)
        self.outlet = result
    
    def material_balance(self) -> bool:
        # Verify sum(inlets) = outlet
        ...
```

### Adding New Thermodynamic Properties

**Location:** `src/thermo/thermo.py` or `src/thermo/properties.py`

**Examples:**
- Enthalpy
- Entropy
- Gibbs free energy
- Fugacity
- Activity coefficients

**Pattern:**
```python
class EnthalpyCalculator:
    @staticmethod
    def ideal_gas_enthalpy(T, component, ref_temp=298.15) -> float:
        """Calculate ideal gas enthalpy."""
        # H = ∫Cp dT
        ...
    
    @staticmethod
    def residual_enthalpy(T, P, component, eos) -> float:
        """Calculate departure from ideal."""
        ...
```

### Adding New Solvers (Phase 4)

**Location:** `src/solver/`

**Types:**
- Sequential modular
- Equation-oriented
- Hybrid approaches

**Pattern:**
```python
class SequentialModularSolver:
    def solve(self, flowsheet):
        # 1. Analyze topology
        # 2. Identify tears
        # 3. Iterate until convergence
        ...
```

---

## ⚡ Performance Considerations

### Current Performance Characteristics

#### Component Operations
- Property lookups: O(1)
- Vapor pressure calc: O(1) - simple formula
- Heat capacity: O(1) - polynomial evaluation

#### Stream Operations
- Property calculations: O(n) where n = number of components
- Mixing: O(n) - iterate through components
- Splitting: O(n) - copy operation

#### Thermodynamic Calculations
- EOS molar volume: O(1) - cubic equation solve (NumPy)
- K-values: O(n) - calculate for each component
- Flash calculation: O(m×n) where m = iterations, n = components
  - Typically m = 3-10 iterations
  - Typically n = 2-20 components

### Optimization Strategies (Future)

#### 1. **Property Caching**

```python
class Stream:
    def __init__(self, ...):
        self._molecular_weight_cache = None
    
    def molecular_weight(self):
        if self._molecular_weight_cache is None:
            self._molecular_weight_cache = self._calculate_mw()
        return self._molecular_weight_cache
    
    def invalidate_cache(self):
        self._molecular_weight_cache = None
```

**When to apply:** After profiling shows property recalculation is bottleneck

#### 2. **Vectorization**

```python
# Instead of loop
for i, component in enumerate(components):
    result[i] = component.vapor_pressure(T)

# Vectorize
temperatures = np.full(n_components, T)
results = np.array([comp.vapor_pressure(T) for comp in components])
```

**When to apply:** When calculating many properties simultaneously

#### 3. **Lazy Evaluation**

```python
class Stream:
    @property
    def mass_flow(self):
        """Calculate only when accessed"""
        return self.molar_flow * self.molecular_weight
```

**Current approach:** Already using this pattern

#### 4. **Parallel Processing** (Future)

For independent unit operations in flowsheet:
```python
from multiprocessing import Pool

with Pool() as pool:
    results = pool.map(calculate_unit, independent_units)
```

**When to apply:** Phase 4+ when solving large flowsheets

#### 5. **Compilation** (Future)

Consider Numba JIT for critical loops:
```python
from numba import jit

@jit(nopython=True)
def rachford_rice(V, z, K):
    # Pure NumPy operations, compiled to machine code
    ...
```

**When to apply:** Only if profiling shows bottlenecks

### Current Performance Targets

- Flash calculation: < 0.1 seconds for 10 components
- Stream mixing: < 0.001 seconds
- Property calculation: < 0.0001 seconds
- 100-unit flowsheet: < 30 seconds (Phase 4 target)

### Profiling Approach

```python
# Use cProfile for profiling
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run code to profile
result = Flash.isothermal_flash(...)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**Rule:** Always profile before optimizing!

---

## 🚀 Future Architecture

### Phase 2: Unit Operations

**New Components:**
- Base class `UnitOperation`
- Concrete units: Mixer, Splitter, HeatExchanger, etc.
- Unit specification system
- Material/energy balance verification

**Architecture Impact:**
- Domain layer expands significantly
- New interfaces between units and streams
- Need for unit configuration/specification

### Phase 3: Advanced Thermodynamics

**New Components:**
- Peng-Robinson EOS
- Activity coefficient models (NRTL, UNIQUAC, UNIFAC)
- Property packages
- Enthalpy/entropy calculations

**Architecture Impact:**
- Property calculation abstraction layer
- Model selection framework
- Parameter database

### Phase 4: Flowsheet Solver

**New Components:**
- Flowsheet graph representation
- Topological analysis
- Convergence algorithms (Wegstein, Newton, Broyden)
- Tear stream management

**Architecture Impact:**
- New application layer
- Orchestration between units
- State management for iterations

### Phase 5: User Interface

**New Components:**
- GUI framework (PyQt or web-based)
- Flowsheet editor (drag-drop)
- Property input forms
- Results visualization

**Architecture Impact:**
- Complete interface layer
- Event system
- Model-View-Controller pattern

### Phase 6: Dynamic Simulation

**New Components:**
- ODE solver integration
- Dynamic unit models
- PID controllers
- Time integration

**Architecture Impact:**
- Parallel architecture (steady-state vs dynamic)
- State history management
- Real-time calculations

### Modularity Goals

Each phase should:
- ✅ Not break previous phases
- ✅ Be independently testable
- ✅ Have clear interfaces
- ✅ Be optionally enabled
- ✅ Support both programmatic and GUI use

---

## 📐 Architectural Decisions

### Decision Log

#### AD-001: Use Python Dataclasses

**Status:** Accepted  
**Date:** November 2025  
**Context:** Need clean syntax for data structures  
**Decision:** Use `@dataclass` for Component, Stream, etc.  
**Consequences:**
- ✅ Clean, readable code
- ✅ Automatic `__init__`, `__repr__`
- ✅ Type hints integrated
- ❌ Slightly slower than `__slots__` (acceptable)

#### AD-002: Immutable Components

**Status:** Accepted  
**Date:** November 2025  
**Context:** Components should not change after creation  
**Decision:** Use `@dataclass(frozen=True)` for Component  
**Consequences:**
- ✅ Thread-safe
- ✅ Prevents bugs from modification
- ❌ Cannot update properties (rarely needed)

#### AD-003: Stateless Thermodynamic Calculations

**Status:** Accepted  
**Date:** November 2025  
**Context:** Thermodynamic calculations are pure functions  
**Decision:** Use static methods, no class state  
**Consequences:**
- ✅ Easy to test
- ✅ Thread-safe
- ✅ Clear data flow
- ❌ Cannot cache intermediate results easily

#### AD-004: Dict-Based Composition

**Status:** Accepted  
**Date:** November 2025  
**Context:** Need flexible composition representation  
**Decision:** Use `Dict[str, Component]` and `Dict[str, float]`  
**Consequences:**
- ✅ Easy to add/remove components
- ✅ Clear component names
- ❌ Slower than array-based (acceptable for < 100 components)

#### AD-005: Units Always Specified

**Status:** Accepted  
**Date:** November 2025  
**Context:** Unit confusion is common source of errors  
**Decision:** All quantities in code have explicit units  
**Consequences:**
- ✅ No ambiguity
- ✅ Clear in code
- ❌ Verbose (acceptable for clarity)

#### AD-006: Separate Dimensional Analysis Module

**Status:** Accepted  
**Date:** November 2025  
**Context:** Need comprehensive unit system  
**Decision:** Create separate `dimanal` module  
**Consequences:**
- ✅ Reusable
- ✅ Type-safe conversions
- ✅ Comprehensive (500+ units)
- ❌ Extra complexity (worth it)

---

## 🧪 Testing Architecture

### Test Organization

```
tests/
├── unit/                  # Unit tests
│   ├── test_component.py
│   ├── test_stream.py
│   └── test_thermo.py
│
├── integration/           # Integration tests (future)
│   ├── test_simple_flowsheet.py
│   └── test_recycle_loop.py
│
├── validation/            # Validation tests (future)
│   ├── test_literature_cases.py
│   └── test_benchmark_problems.py
│
└── performance/           # Performance tests (future)
    └── test_flash_performance.py
```

### Test Principles

1. **Unit tests for all public APIs**
2. **Test edge cases and error conditions**
3. **Integration tests for workflows**
4. **Validation against literature data**
5. **Performance benchmarks for critical paths**

### Test Coverage Target

- Overall: > 80%
- Core modules: > 90%
- UI modules: > 70%

---

## 📚 References

### Chemical Engineering
- Smith, Van Ness & Abbott - "Introduction to Chemical Engineering Thermodynamics"
- Perry's Chemical Engineers' Handbook
- Seider et al. - "Product and Process Design Principles"

### Software Architecture
- Martin - "Clean Architecture"
- Gamma et al. - "Design Patterns"
- Python docs - Dataclasses, Type Hints

### Similar Projects
- DWSIM (open source process simulator)
- Cantera (chemical kinetics)
- CoolProp (thermophysical properties)

---

## 📝 Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1.0 | Nov 2025 | Initial architecture documentation | Project Team |

---

## 🎯 Summary

This architecture provides:

✅ **Clear separation of concerns** - Foundation, Domain, Application, Interface layers  
✅ **Extensibility** - Easy to add components, units, models, solvers  
✅ **Modularity** - Independent, testable components  
✅ **Type safety** - Comprehensive type hints  
✅ **Performance** - Optimizable without redesign  
✅ **Maintainability** - Well-documented, clean code  

The architecture is designed to grow from simple thermodynamic calculations (Phase 1) to full process simulation (Phases 2-10) while maintaining code quality and architectural integrity.

---

*Last Updated: November 2025*  
*Phase 1 Complete - Foundation established*  
*Next: Phase 2 - Unit Operations*
