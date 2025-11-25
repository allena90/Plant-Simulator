# Phase 1 - Week 3: Component System Implementation

## 🎯 What We're Building

The **Component class** is the foundation of our simulation software. It represents chemical compounds with all their thermodynamic and physical properties needed for process calculations.

## 📦 Files Created

1. **component.py** - The main Component class
2. **test_component.py** - Unit tests for the Component class

## 🚀 Next Steps

### 1. Copy Files to Your Project

Copy the two files I created to your project:

```cmd
# Copy component.py to src/core/
copy component.py "G:\Other computers\My Computer\Projects\Plant Simulator\src\core\"

# Copy test_component.py to tests/
copy test_component.py "G:\Other computers\My Computer\Projects\Plant Simulator\tests\"
```

### 2. Run the Component Demo

```cmd
cd "G:\Other computers\My Computer\Projects\Plant Simulator"
venv\Scripts\activate.bat

# Run the component module to see it in action
python src\core\component.py
```

You should see output like:
```
=== Component Module Demo ===

Water (H2O)
Molecular Weight: 18.015 kg/kmol
Critical Temperature: 647.1 K
Critical Pressure: 22.064 MPa

Vapor pressure at 373.15K: 1.013 bar
Ideal gas Cp at 373.15K: 33577.0 J/(kmol·K)
...
```

### 3. Run the Tests

```cmd
# Run the unit tests
pytest tests/test_component.py -v

# Or run with coverage
pytest tests/test_component.py -v --cov=src.core.component
```

You should see all tests passing! ✅

### 4. Experiment with the Component Class

Try creating your own components in Python:

```python
from src.core.component import Component, create_water, create_methane

# Use pre-defined components
water = create_water()
print(f"Water boiling point: {water.normal_boiling_point} K")

# Create your own component
nitrogen = Component(
    name="Nitrogen",
    formula="N2",
    cas_number="7727-37-9",
    molecular_weight=28.014,
    critical_temperature=126.2,
    critical_pressure=3.39e6,
    acentric_factor=0.037,
    normal_boiling_point=77.35,
    phase_at_stp="gas"
)

# Calculate properties
Tr = nitrogen.reduced_temperature(100)  # Reduced temperature at 100K
print(f"Nitrogen reduced temperature at 100K: {Tr:.3f}")
```

## 📚 What You've Learned

### Key Concepts Implemented:

1. **Component Properties:**
   - Critical temperature, pressure, volume
   - Acentric factor (Pitzer)
   - Molecular weight
   - Normal boiling/melting points

2. **Property Calculations:**
   - Vapor pressure (Antoine equation)
   - Ideal gas heat capacity (polynomial)
   - Reduced temperature and pressure

3. **Software Engineering:**
   - Python dataclasses for clean data structures
   - Type hints for better code quality
   - Documentation strings (docstrings)
   - Error handling and validation
   - Unit testing with pytest
   - Serialization (to_dict/from_dict)

## 🎓 Learning Resources

To understand the thermodynamics better:

1. **Antoine Equation:**
   - log₁₀(P) = A - B/(T + C)
   - Used to calculate vapor pressure
   - Different coefficients for each substance

2. **Heat Capacity Correlation:**
   - Cp = A + B·T + C·T² + D·T³
   - Temperature-dependent property
   - Important for energy balances

3. **Reduced Properties:**
   - Tr = T/Tc (reduced temperature)
   - Pr = P/Pc (reduced pressure)
   - Used in corresponding states theory

## ✅ Phase 1 Week 3 Checklist

- [ ] Files copied to correct directories
- [ ] Component demo runs successfully
- [ ] All unit tests pass
- [ ] Experimented with creating custom components
- [ ] Understand Antoine equation
- [ ] Understand heat capacity correlations
- [ ] Ready to move to Week 4 (Stream class)

## 🐛 Troubleshooting

**Import errors?**
- Make sure `__init__.py` exists in `src/core/`
- Make sure your virtual environment is activated
- Try: `pip install -e .` to install the project in development mode

**Tests not running?**
- Make sure pytest is installed: `pip install pytest pytest-cov`
- Check that you're in the project root directory

**Module not found?**
- Make sure you ran `pip install -e .` from the project root
- Check your PYTHONPATH or add project to path

## 🔜 Next Week: Stream Class

Next, we'll build the **Stream class** which represents material flows between unit operations. This will include:
- Mass and energy balances
- Phase calculations
- Mixture properties
- Unit conversions

## 💡 Tips

- Read through the component.py code carefully - it's well-documented
- Try adding more pre-defined components (ethane, propane, CO2, etc.)
- Experiment with property calculations
- Look up real thermodynamic data to validate calculations

---

**Great job completing Week 3!** 🎉

When you're ready, let me know and we'll move on to Week 4: Stream & Material Balance Framework!
