# Phase 1 - Week 5: Basic Thermodynamic Models

## 🎯 What We Built

**Thermodynamic models** are the heart of process simulation! We've implemented:
- **Ideal Gas Law** - Simple PVT behavior
- **Van der Waals EOS** - Accounts for molecular size and attraction
- **Redlich-Kwong EOS** - Improved accuracy for real gases
- **Vapor-Liquid Equilibrium (VLE)** - Phase behavior using Raoult's Law
- **Flash Calculations** - Separation into vapor and liquid phases

## 📦 Files Created

1. **thermo.py** - All thermodynamic models and calculations
2. **test_thermo.py** - Comprehensive unit tests

## 🚀 Installation Instructions

### 1. Copy Files to Your Project

```cmd
# Copy thermo.py to src/thermo/
copy thermo.py "G:\Other computers\My Computer\Projects\Plant Simulator\src\thermo\"

# Copy test_thermo.py to tests/
copy test_thermo.py "G:\Other computers\My Computer\Projects\Plant Simulator\tests\"
```

### 2. Run the Thermodynamics Demo

```cmd
cd "G:\Other computers\My Computer\Projects\Plant Simulator"
venv\Scripts\activate.bat

# Run the thermo module
python -m src.thermo.thermo
```

You should see calculations for all the different models!

### 3. Run the Tests

```cmd
# Run thermodynamics tests
pytest tests/test_thermo.py -v

# Run with coverage
pytest tests/test_thermo.py -v --cov=src.thermo

# Run all tests so far
pytest tests/ -v
```

All tests should pass! ✅

## 📚 Key Concepts Implemented

### 1. Equations of State (EOS)

**Ideal Gas Law:**
```python
from src.thermo.thermo import IdealGas

T = 300  # K
P = 101325  # Pa (1 atm)

# Calculate molar volume
V = IdealGas.molar_volume(T, P)
print(f"Molar volume: {V:.4f} m³/kmol")

# Calculate pressure
P_calc = IdealGas.pressure(T, V)
print(f"Pressure: {P_calc/1e5:.4f} bar")
```

**Van der Waals EOS:**
```python
from src.thermo.thermo import VanDerWaalsEOS
from src.core.component import create_methane

methane = create_methane()

# Get parameters
a, b = VanDerWaalsEOS.calculate_parameters(methane)
print(f"a = {a:.4e}, b = {b:.4e}")

# Calculate molar volume
V_vapor = VanDerWaalsEOS.molar_volume(T, P, methane, phase='vapor')
V_liquid = VanDerWaalsEOS.molar_volume(T, P, methane, phase='liquid')

# Compressibility factor
Z = VanDerWaalsEOS.compressibility_factor(T, P, methane, phase='vapor')
print(f"Z = {Z:.4f}")
```

**Redlich-Kwong EOS:**
```python
from src.thermo.thermo import RedlichKwongEOS

# Similar to van der Waals, but more accurate
a, b = RedlichKwongEOS.calculate_parameters(methane)
V = RedlichKwongEOS.molar_volume(T, P, methane, phase='vapor')
Z = RedlichKwongEOS.compressibility_factor(T, P, methane, phase='vapor')
```

### 2. Vapor-Liquid Equilibrium

**K-Values (Raoult's Law):**
```python
from src.thermo.thermo import VLE
from src.core.component import create_water, create_methane

water = create_water()
methane = create_methane()
components = {'Water': water, 'Methane': methane}

T = 320  # K
P = 500000  # Pa (5 bar)

# Calculate K-values: K_i = P_sat_i / P
k_values = VLE.raoult_law_k_values(T, P, components)
print(f"K(Water) = {k_values['Water']:.4f}")
print(f"K(Methane) = {k_values['Methane']:.4f}")
```

**Bubble Point Pressure:**
```python
# At what pressure does the first bubble form?
liquid_comp = {'Water': 0.6, 'Methane': 0.4}
P_bubble = VLE.bubble_point_pressure(T, liquid_comp, components)
print(f"Bubble point: {P_bubble/1e5:.4f} bar")
```

**Dew Point Pressure:**
```python
# At what pressure does the first drop form?
vapor_comp = {'Water': 0.3, 'Methane': 0.7}
P_dew = VLE.dew_point_pressure(T, vapor_comp, components)
print(f"Dew point: {P_dew/1e5:.4f} bar")
```

### 3. Flash Calculations

**Isothermal Flash:**
```python
from src.thermo.thermo import Flash

# Feed composition
feed = {'Water': 0.5, 'Methane': 0.5}

# Perform flash at specified T and P
result = Flash.isothermal_flash(T, P, feed, components)

print(f"Vapor fraction: {result.vapor_fraction:.4f}")
print(f"Converged: {result.converged}")
print(f"Iterations: {result.iterations}")

print("\nVapor composition:")
for name, y in result.vapor_mole_fractions.items():
    print(f"  {name}: {y:.4f}")

print("\nLiquid composition:")
for name, x in result.liquid_mole_fractions.items():
    print(f"  {name}: {x:.4f}")
```

## 🎓 Thermodynamic Theory

### Equations of State

**1. Ideal Gas Law:**
```
PV = nRT
```
- Assumes no molecular interactions
- Works well at low pressure and high temperature

**2. Van der Waals EOS:**
```
(P + a/V²)(V - b) = RT
```
- `a`: accounts for intermolecular attractions
- `b`: accounts for molecular volume
- Parameters from critical properties

**3. Redlich-Kwong EOS:**
```
P = RT/(V-b) - a/(√T·V(V+b))
```
- Improved accuracy over van der Waals
- Better for vapor phase
- Temperature-dependent attraction term

### Vapor-Liquid Equilibrium

**Raoult's Law (Ideal Mixtures):**
```
y_i·P = x_i·P_sat_i
```

Where:
- `y_i` = vapor mole fraction of component i
- `x_i` = liquid mole fraction of component i
- `P` = system pressure
- `P_sat_i` = vapor pressure of pure component i

**K-Value:**
```
K_i = y_i/x_i = P_sat_i/P
```

- K > 1: Component prefers vapor phase (volatile)
- K < 1: Component prefers liquid phase (heavy)
- K = 1: No preference (at boiling point)

**Bubble Point:**
```
P_bubble = Σ(x_i·P_sat_i)
```
Pressure at which first vapor bubble forms.

**Dew Point:**
```
P_dew = 1/Σ(y_i/P_sat_i)
```
Pressure at which first liquid drop forms.

### Flash Calculations

**Rachford-Rice Equation:**
```
Σ[z_i(K_i-1)/(1+V(K_i-1))] = 0
```

Where:
- `z_i` = feed mole fraction
- `K_i` = K-value
- `V` = vapor fraction

**Phase Compositions:**
```
x_i = z_i/[1 + V(K_i - 1)]
y_i = K_i·x_i
```

**Material Balance:**
```
z_i = V·y_i + (1-V)·x_i
```

## ✅ Phase 1 Week 5 Checklist

- [ ] Files copied to correct directories
- [ ] Thermo demo runs successfully
- [ ] All unit tests pass
- [ ] Understand ideal gas law
- [ ] Understand van der Waals equation
- [ ] Understand Raoult's Law and K-values
- [ ] Understand flash calculations
- [ ] Experimented with different conditions
- [ ] Ready for Week 6 (Testing & Documentation)

## 💡 Practice Exercises

### Exercise 1: Compare EOS
Calculate molar volume of methane at 200K and 50 bar using:
- Ideal gas law
- Van der Waals EOS
- Redlich-Kwong EOS

Compare the results. Which deviates most from ideal?

### Exercise 2: Phase Diagram
For a 50-50 water-methane mixture at 300K:
- Calculate bubble point pressure
- Calculate dew point pressure
- Perform flash at intermediate pressure
- Plot how vapor fraction changes with pressure

### Exercise 3: K-Value Trends
For water at constant pressure (1 bar):
- Calculate K-values from 300K to 400K
- Plot K vs T
- At what temperature does K = 1?

## 🐛 Troubleshooting

**Import errors?**
```cmd
# Make sure all __init__.py files exist
# Reinstall package
pip install -e .
```

**Numerical issues in EOS?**
- Some conditions may not have real roots
- Try different temperature/pressure ranges
- Use try-except blocks for robustness

**Flash not converging?**
- Check that components have vapor pressure data
- Verify temperature range is valid for Antoine equation
- Try different initial guesses

**Tests failing with "No valid roots"?**
- This can happen at extreme conditions
- Tests are designed to use reasonable conditions
- If issues persist, check component critical properties

## 🔬 Physical Insights

**When to use each model:**

1. **Ideal Gas:**
   - Low pressure (< 1 bar)
   - High temperature (> 2×Tc)
   - Simple, fast calculations
   - Good for initial estimates

2. **Van der Waals:**
   - Moderate pressures
   - Qualitative behavior
   - Educational purposes
   - Historical significance

3. **Redlich-Kwong:**
   - Better for real gases
   - Good for vapor phase
   - More accurate than vdW
   - Industry use (older standard)

4. **Flash Calculations:**
   - Separators, drums, vessels
   - Distillation (stage equilibrium)
   - Any vapor-liquid separation
   - Process design

## 🔜 Next Week: Testing & Documentation

In Week 6, we'll:
- Write comprehensive tests for all modules
- Validate against literature data
- Create example calculations
- Document the API
- Benchmark performance

This completes the foundation! We now have:
- ✅ Components with properties
- ✅ Streams with material balances
- ✅ Thermodynamic models

Next, we'll ensure everything is robust and well-documented before moving to unit operations!

## 📊 Your Progress

### Phase 1 Complete (50% Done!):
- ✅ **Week 3:** Component system
- ✅ **Week 4:** Stream & material balances
- ✅ **Week 5:** Thermodynamic models
- ⏳ **Week 6:** Testing & validation

### What You Can Do Now:
- Create chemical components
- Calculate thermodynamic properties
- Model process streams
- Predict phase behavior
- Calculate equilibrium compositions
- Perform flash separations

### Coming in Phase 2:
- Unit operations (mixers, heat exchangers, reactors)
- Flowsheet connections
- Sequential calculations
- More complex separations

---

## 💪 Commit Your Work

```cmd
git add .
git commit -m "Phase 1 Week 5: Implement thermodynamic models (EOS, VLE, Flash)"
git push
```

---

**Fantastic work! 🎉** You've now built the core thermodynamic engine! This is the foundation that makes accurate process simulation possible!

When you're ready for Week 6 (final week of Phase 1), let me know! 🚀
