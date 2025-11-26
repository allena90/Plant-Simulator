# Python Formatting Guide
## Industrial Plant Simulation Software Project

**Last Updated:** November 2025  
**Python Version:** 3.10+

---

## Table of Contents

1. [General Principles](#general-principles)
2. [File Structure](#file-structure)
3. [Import Organization](#import-organization)
4. [Naming Conventions](#naming-conventions)
5. [Documentation Standards](#documentation-standards)
6. [Code Style](#code-style)
7. [Type Hints](#type-hints)
8. [Error Handling](#error-handling)
9. [Testing Conventions](#testing-conventions)
10. [Module-Specific Guidelines](#module-specific-guidelines)

---

## General Principles

### PEP 8 Compliance
This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines with the following specific conventions:

- **Line Length:** Maximum 100 characters (not the PEP 8 default of 79)
- **Indentation:** Tabs
- **Encoding:** UTF-8
- **Blank Lines:** 2 blank lines between top-level functions/classes, 1 blank line between methods

### Code Quality Tools
- **Formatter:** `black` (line length: 100)
- **Linter:** `flake8`
- **Type Checker:** `mypy` (recommended but not enforced)

---

## File Structure

### Module Header Template

Every Python module should start with a comprehensive header:

```python
"""
Module Name
===========

Brief description of what this module does.

This module implements [major functionality]. It includes:
- Feature 1
- Feature 2
- Feature 3

Author: Plant Simulation Software Project (if not owner, then contributor's name)
Date: MMMM YYYY
"""
```

### Standard Import Order

```python
# 1. Future imports (if any)
from __future__ import annotations

# 2. Standard library imports
import math
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

# 3. Third-party imports
import numpy as np
import pandas as pd
from scipy.optimize import fsolve

# 4. Local application imports
from src.core.component import Component
from src.core.stream import Stream
```

### Module Structure Order

1. Module docstring
2. Imports
3. Constants (ALL_CAPS)
4. Exception classes
5. Helper functions/utilities
6. Main classes
7. Module-level functions
8. `if __name__ == "__main__":` demo section

---

## Import Organization

### Grouping and Sorting

- Group imports by category (stdlib, third-party, local)
- Sort alphabetically within each group
- One import per line for clarity
- Use absolute imports from `src/` root

### Examples

**Good:**
```python
from typing import Dict, List, Optional
import numpy as np
from src.core.component import Component
from src.core.stream import Stream
```

**Bad:**
```python
from src.core.component import Component, Stream  # Wrong grouping
import numpy as np, pandas as pd  # Multiple on one line
from ..core import Component  # Relative import
```

---

## Naming Conventions

### Variables and Functions

```python
# Variables: snake_case
temperature = 298.15
molar_flow_rate = 100.0
component_list = []

# Functions: snake_case
def calculate_pressure():
    pass

def get_vapor_fraction():
    pass

# Private functions/variables: leading underscore
def _internal_helper():
    pass

_private_constant = 42
```

### Classes

```python
# Classes: PascalCase
class Component:
    pass

class VanDerWaalsEOS:
    pass

class FlashResult:
    pass
```

### Constants

```python
# Constants: ALL_CAPS with underscores
UNIVERSAL_GAS_CONSTANT = 8.314462  # J/(mol·K)
R_KMOL = 8314.462  # J/(kmol·K)
STANDARD_PRESSURE = 101325  # Pa
MAX_ITERATIONS = 100
TOLERANCE = 1e-6
```

### Special Names

```python
# Protected (internal use): single leading underscore
_internal_cache = {}

# Strongly private (name mangling): double leading underscore
__private_data = None

# Magic methods: double underscores on both sides
def __init__(self):
    pass

def __repr__(self):
    pass
```

---

## Documentation Standards

### Module Docstrings

```python
"""
Module Name
===========

Brief one-line summary.

Detailed description of the module's purpose and functionality.
Can span multiple paragraphs.

This module implements:
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

Example:
    >>> from src.module import SomeClass
    >>> obj = SomeClass()
    >>> result = obj.method()

Author: Plant Simulation Software Project (or contributor's name)
Date: MMMM YYYY
"""
```

### Class Docstrings

```python
class MyClass:
    """
    Represents a [brief description of the class].

    Attributes:
        attribute_one (type): Description of attribute one.
        attribute_two (type): Description of attribute two.
        ...

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
```

### Function/Method Docstrings

```python
def foo(arg1:type, arg2:type, ...) -> type:
    """
    Brief description of what the function does.
    
    Args:
        arg1 (type): Description of arg1
        arg2 (type): Description of arg2
        ...
    
    Returns:
        type: Description of the return value
        
    Raises:
        ValueError: Condition of Value Error
        Warning: Condition of Warning

    Note:
        Any additional notes about the function.
    """
```

### Inline Comments

```python
# Good: Explain WHY, not WHAT
# Calculate reduced temperature for corresponding states
Tr = temperature / critical_temperature

# Bad: States the obvious
# Divide temperature by critical temperature
Tr = temperature / critical_temperature

# Good: Complex logic explanation
# Use Newton-Raphson to solve Rachford-Rice equation
# because direct methods are unstable for this system
for iteration in range(max_iterations):
    f = rachford_rice(V)
    df = rachford_rice_derivative(V)
    V_new = V - f / df
```

---

## Code Style

### Line Breaks and Wrapping

```python
# Function definitions
def long_function_name(
    var_one: float,
    var_two: float,
    var_three: float,
    var_four: float
) -> float:
    pass

# Function calls
result = some_function(
    argument_one=value_one,
    argument_two=value_two,
    argument_three=value_three,
    argument_four=value_four
)

# Lists, dicts, etc.
my_list = [
    item_one,
    item_two,
    item_three,
]

my_dict = {
    'key_one': value_one,
    'key_two': value_two,
    'key_three': value_three,
}

# Long strings
message = (
    "This is a very long message that spans multiple lines "
    "and needs to be broken up for readability."
)
```

### Whitespace

```python
# Around operators
x = 5 + 3  # Good
x=5+3  # Bad

# After commas
my_list = [1, 2, 3]  # Good
my_list = [1,2,3]  # Bad

# Function arguments
def func(a, b, c):  # Good
def func(a,b,c):  # Bad

# No space before colon in type hints
def func(x: int) -> float:  # Good
def func(x : int) -> float:  # Bad

# No trailing whitespace
temperature = 300.0  # Good
temperature = 300.0   # Bad (trailing spaces)
```

### String Formatting

```python
# Prefer f-strings for formatting
name = "Water"
temp = 373.15
message = f"{name} boils at {temp:.2f} K"

# Use raw strings for regex
pattern = r'\d{3}-\d{4}'

# Use triple quotes for multi-line strings
docstring = """
This is a multi-line
string that spans several
lines.
"""
```

---

## Type Hints

### Basic Type Hints

```python
# Simple types
def calculate_volume(length: float, width: float, height: float) -> float:
    return length * width * height

# Optional types
def get_component(name: str) -> Optional[Component]:
    pass

# Union types
def process_input(value: Union[int, float, str]) -> str:
    pass

# Collection types
def get_components() -> List[Component]:
    pass

def get_properties() -> Dict[str, float]:
    pass

def get_pair() -> Tuple[float, float]:
    pass
```

### Complex Type Hints

```python
from typing import Dict, List, Optional, Tuple, Callable

# Nested collections
def get_data() -> Dict[str, List[float]]:
    pass

# Callable types
def apply_function(func: Callable[[float], float], value: float) -> float:
    pass

# Class method type hints
class Component:
    def __init__(self, name: str, molecular_weight: float) -> None:
        self.name = name
        self.molecular_weight = molecular_weight
    
    def get_info(self) -> Dict[str, Union[str, float]]:
        return {'name': self.name, 'mw': self.molecular_weight}
```

### Dataclass Type Hints

```python
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Component:
    """Component with full type hints."""
    name: str
    formula: str
    molecular_weight: float
    critical_temperature: float = 0.0
    critical_pressure: float = 0.0
    properties: Dict[str, float] = field(default_factory=dict)
    description: Optional[str] = None
```

---

## Error Handling

### Exception Guidelines

```python
# Define custom exceptions at module level
class DimensionError(Exception):
    """Raised for dimensional mismatches."""
    pass

class ConvergenceError(Exception):
    """Raised when iterative solver fails to converge."""
    pass

# Use specific exceptions
def validate_temperature(temp: float) -> None:
    if temp <= 0:
        raise ValueError("Temperature must be positive (in Kelvin)")
    if temp > 10000:
        raise ValueError("Temperature exceeds reasonable range")

# Provide helpful error messages
def convert_units(value: float, from_unit: Unit, to_unit: Unit) -> float:
    if from_unit.dimension != to_unit.dimension:
        raise DimensionError(
            f"Cannot convert {from_unit.name} ({from_unit.dimension}) to "
            f"{to_unit.name} ({to_unit.dimension})"
        )
    return to_unit.from_si_value(from_unit.to_si_value(value))
```

### Try-Except Blocks

```python
# Be specific about exceptions
try:
    result = risky_operation()
except ValueError as e:
    print(f"Invalid value: {e}")
except KeyError as e:
    print(f"Missing key: {e}")

# Use else clause when appropriate
try:
    value = get_value()
except KeyError:
    print("Key not found")
else:
    process_value(value)
finally:
    cleanup()

# Avoid bare except
try:
    operation()
except:  # Bad - too broad
    pass

# Better
try:
    operation()
except Exception as e:  # Good - still catches most, but explicit
    logging.error(f"Operation failed: {e}")
```

---

## Testing Conventions

### Test File Naming

```
tests/
├── test_component.py      # Tests for src/core/component.py
├── test_stream.py         # Tests for src/core/stream.py
├── test_thermo.py         # Tests for src/thermo/thermo.py
└── test_dim.py            # Tests for src/dimanal/dim.py
```

### Test Class Organization

```python
"""
Unit Tests for Component Module
================================

Tests for the Component class and related functions.

Author: Plant Simulation Software Project (or contributor's name)
Date: MMMM YYYY
"""

import pytest
from src.core.component import Component, create_water


class TestComponentBasics:
    """Test basic component creation and validation."""
    
    def test_create_valid_component(self):
        """Test creating a valid component."""
        comp = Component(
            name="Nitrogen",
            formula="N2",
            molecular_weight=28.014
        )
        assert comp.name == "Nitrogen"
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Component(name="", formula="N2", molecular_weight=28.014)


class TestComponentProperties:
    """Test component property calculations."""
    
    def test_reduced_temperature(self):
        """Test reduced temperature calculation."""
        water = create_water()
        Tr = water.reduced_temperature(373.15)
        assert Tr > 0
```

### Test Method Naming

```python
# Pattern: test_<function>_<scenario>
def test_calculate_pressure_ideal_gas():
    pass

def test_calculate_pressure_with_zero_volume_raises_error():
    pass

def test_mix_streams_preserves_mass_balance():
    pass
```

### Assertions

```python
# Use descriptive assertions
assert result > 0, "Result must be positive"
assert abs(result - expected) < tolerance, f"Result {result} not close to {expected}"

# Prefer pytest assertions
assert component.name == "Water"  # Good
self.assertEqual(component.name, "Water")  # Avoid unittest style

# Use pytest.approx for floating point
assert value == pytest.approx(expected, rel=1e-6)
assert abs(value - expected) < 1e-6  # Also acceptable
```

---

## Module-Specific Guidelines

### Component Module (`src/core/component.py`)

```python
# Use dataclass for data containers
@dataclass
class Component:
    """Represents a chemical component."""
    name: str
    formula: str
    molecular_weight: float
    critical_temperature: float = 0.0
    
    def __post_init__(self):
        """Validate data after initialization."""
        if not self.name:
            raise ValueError("Component name cannot be empty")

# Provide factory functions for common components
def create_water() -> Component:
    """Create water component with standard properties."""
    return Component(
        name="Water",
        formula="H2O",
        molecular_weight=18.015,
        critical_temperature=647.1
    )
```

### Stream Module (`src/core/stream.py`)

```python
# Clear physical units in docstrings
def molar_volume(temperature: float, pressure: float) -> float:
    """
    Calculate molar volume.
    
    Args:
        temperature (float): Temperature in K
        pressure (float): Pressure in Pa
        
    Returns:
        float: Molar volume in m³/kmol
    """
```

### Thermodynamic Module (`src/thermo/thermo.py`)

```python
# Use descriptive variable names matching equations
def van_der_waals_eos(T: float, P: float, a: float, b: float) -> float:
    """
    Van der Waals equation: (P + a/V²)(V - b) = RT
    
    Args:
        T: Temperature in K
        P: Pressure in Pa
        a: Attraction parameter in Pa·m⁶/kmol²
        b: Volume parameter in m³/kmol
    """
    # Variable names match equation terms
    R = 8314.462  # J/(kmol·K)
    # ... implementation
```

### Dimensional Analysis Module (`src/dimanal/dim.py`)

```python
# Use frozen dataclasses for immutable units
@dataclass(frozen=True)
class Unit:
    """Represents a unit of measurement."""
    name: str
    symbol: str
    dimension: Dimension
    to_si: float = 1.0

# Define constants at module level
METER = Unit("meter", "m", LENGTH, 1.0)
KILOGRAM = Unit("kilogram", "kg", MASS, 1.0)
```

---

## Examples of Good vs. Bad Code

### Example 1: Function Definition

**Good:**
```python
def calculate_flash_point(
    temperature: float,
    pressure: float,
    composition: Dict[str, float],
    max_iterations: int = 100,
    tolerance: float = 1e-6
) -> FlashResult:
    """
    Calculate flash separation results.
    
    Args:
        temperature: Temperature in K
        pressure: Pressure in Pa
        composition: Component mole fractions
        max_iterations: Maximum solver iterations
        tolerance: Convergence tolerance
        
    Returns:
        FlashResult with vapor fraction and compositions
    """
    # Implementation
```

**Bad:**
```python
def flash(T,P,comp,iter=100,tol=1e-6):  # No type hints, unclear names
    # Implementation
```

### Example 2: Class Definition

**Good:**
```python
@dataclass
class Stream:
    """
    Represents a process stream.
    
    Attributes:
        name: Stream identifier
        temperature: Temperature in K
        pressure: Pressure in Pa
    """
    name: str
    temperature: float
    pressure: float
    
    def __post_init__(self):
        """Validate stream data."""
        if self.temperature <= 0:
            raise ValueError("Temperature must be positive")
```

**Bad:**
```python
class Stream:
    def __init__(self, n, t, p):  # Unclear variable names
        self.n = n
        self.t = t
        self.p = p
        # No validation
```

### Example 3: Error Handling

**Good:**
```python
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between units."""
    if from_unit not in ["K", "C", "F"]:
        raise ValueError(
            f"Unknown source unit '{from_unit}'. "
            f"Must be one of: K, C, F"
        )
    # Conversion logic
```

**Bad:**
```python
def convert_temperature(value, from_unit, to_unit):
    try:
        # Conversion logic
    except:  # Bare except
        return None  # Silent failure
```

---

## Pre-Commit Checklist

Before committing code, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] All functions/classes have docstrings
- [ ] Type hints are included
- [ ] Tests are written and passing
- [ ] No commented-out code (use git history instead)
- [ ] No debug print statements
- [ ] Module has demonstration in `if __name__ == "__main__":`
- [ ] Imports are organized correctly
- [ ] Constants are at module level in ALL_CAPS
- [ ] Line length ≤ 100 characters

---

## Tools Configuration

### Black Configuration (pyproject.toml)
```toml
[tool.black]
line-length = 100
target-version = ['py310']
```

### Flake8 Configuration (.flake8)
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = .git,__pycache__,venv
```

### Pytest Configuration (pytest.ini)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

## Additional Resources

- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)

---

**Remember:** Consistent style makes code easier to read, maintain, and collaborate on. When in doubt, favor clarity over cleverness.