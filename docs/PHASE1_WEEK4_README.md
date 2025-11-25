# Phase 1 - Week 4: Stream & Material Balance Framework

## 🎯 What We Built

The **Stream class** represents material flows between unit operations - this is the lifeblood of process simulation! It handles:
- Mass and energy balances
- Mixture properties
- Stream mixing and splitting
- Unit conversions

## 📦 Files Created

1. **stream.py** - The Stream class and UnitConversion utilities
2. **test_stream.py** - Comprehensive unit tests

## 🚀 Installation Instructions

### 1. Copy Files to Your Project

```cmd
# Copy stream.py to src/core/
copy stream.py "G:\Other computers\My Computer\Projects\Plant Simulator\src\core\"

# Copy test_stream.py to tests/
copy test_stream.py "G:\Other computers\My Computer\Projects\Plant Simulator\tests\"
```

### 2. Run the Stream Demo

```cmd
cd "G:\Other computers\My Computer\Projects\Plant Simulator"
venv\Scripts\activate.bat

# Run the stream module to see it in action
python src\core\stream.py
```

You should see detailed stream summaries with composition, flow rates, and properties!

### 3. Run the Tests

```cmd
# Run all stream tests
pytest tests/test_stream.py -v

# Run with coverage
pytest tests/test_stream.py -v --cov=src.core.stream

# Run all tests (component + stream)
pytest tests/ -v --cov=src.core
```

All tests should pass! ✅

## 📚 Key Concepts Implemented

### 1. Stream Properties

```python
from src.core.stream import Stream, UnitConversion
from src.core.component import create_water, create_methane

water = create_water()
methane = create_methane()

# Create a stream
stream = Stream(
    name="Feed",
    temperature=UnitConversion.celsius_to_kelvin(25),  # 298.15 K
    pressure=UnitConversion.bar_to_pascal(10),  # 1e6 Pa
    components={'Water': water, 'Methane': methane},
    mole_fractions={'Water': 0.6, 'Methane': 0.4},
    molar_flow=100.0,  # kmol/s
    phase="liquid"
)

# Calculate properties
print(f"Molecular weight: {stream.molecular_weight()} kg/kmol")
print(f"Mass flow: {stream.mass_flow()} kg/s")
print(f"Density (ideal gas): {stream.ideal_gas_density()} kg/m³")

# Get component flows
comp_flows = stream.component_molar_flows()
print(f"Water flow: {comp_flows['Water']} kmol/s")
print(f"Methane flow: {comp_flows['Methane']} kmol/s")

# Mass fractions
mass_fracs = stream.mass_fractions()
print(f"Water mass fraction: {mass_fracs['Water']}")
```

### 2. Stream Operations

**Mixing Streams:**
```python
# Two streams with different compositions
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

# Mix them
mixed = stream1.mix_with(stream2)
print(mixed.summary())
```

**Splitting Streams:**
```python
# Split 70-30
top = stream.split(0.7, "_top")
bottom = stream.split(0.3, "_bottom")

print(f"Original: {stream.molar_flow} kmol/s")
print(f"Top: {top.molar_flow} kmol/s")
print(f"Bottom: {bottom.molar_flow} kmol/s")
```

### 3. Unit Conversions

```python
# Temperature
temp_k = UnitConversion.celsius_to_kelvin(25)  # 298.15 K
temp_c = UnitConversion.kelvin_to_celsius(373.15)  # 100 °C
temp_k2 = UnitConversion.fahrenheit_to_kelvin(77)  # 298.15 K

# Pressure
p_pa = UnitConversion.bar_to_pascal(10)  # 1e6 Pa
p_bar = UnitConversion.pascal_to_bar(101325)  # 1.01325 bar
p_pa2 = UnitConversion.atm_to_pascal(1)  # 101325 Pa
p_psi = UnitConversion.pascal_to_psi(101325)  # ~14.7 psi

# Flow rates
flow_h = UnitConversion.kmol_s_to_kmol_h(10)  # 36000 kmol/h
flow_s = UnitConversion.kmol_h_to_kmol_s(3600)  # 1 kmol/s
```

## 🎓 What You've Learned

### Material Balance Equations

1. **Conservation of Mass:**
   - Total mass in = Total mass out
   - `Σ m_in = Σ m_out`

2. **Component Balance:**
   - For each component: `n_i,in = n_i,out`
   - Molar flow of component i: `n_i = n_total × x_i`

3. **Mixing:**
   - `n_out = n_1 + n_2`
   - `x_i,out = (n_1×x_i,1 + n_2×x_i,2) / n_out`

4. **Splitting:**
   - Same composition as feed
   - Different flow rates

### Property Calculations

1. **Average Molecular Weight:**
   - `MW_avg = Σ(x_i × MW_i)`

2. **Mass Flow:**
   - `m_dot = n_dot × MW_avg`

3. **Mass Fractions:**
   - `w_i = (x_i × MW_i) / MW_avg`

4. **Ideal Gas Density:**
   - `ρ = (P × MW) / (R × T)`
   - R = 8314.46 J/(kmol·K)

## ✅ Phase 1 Week 4 Checklist

- [ ] Files copied to correct directories
- [ ] Stream demo runs successfully
- [ ] All unit tests pass
- [ ] Experimented with stream operations
- [ ] Understand material balance equations
- [ ] Understand mixing and splitting
- [ ] Practiced unit conversions
- [ ] Ready for Week 5 (Thermodynamic models)

## 💡 Practice Exercises

### Exercise 1: Binary Mixture
Create a stream with 50-50 ethane-propane mixture at 300K and 10 bar. Calculate:
- Molecular weight
- Mass flow rate
- Mass fractions

### Exercise 2: Mixing
Mix two streams:
- Stream 1: Pure water, 300K, 5 bar, 10 kmol/s
- Stream 2: Pure methane, 320K, 5 bar, 20 kmol/s

What is the outlet composition and temperature?

### Exercise 3: Unit Conversions
Convert:
- 100°F to Kelvin
- 50 psi to bar
- 1000 kg/h to kmol/s (for water)

## 🐛 Troubleshooting

**Import errors?**
```cmd
# Make sure you're in the right directory and venv is active
cd "G:\Other computers\My Computer\Projects\Plant Simulator"
venv\Scripts\activate.bat

# Reinstall in development mode if needed
pip install -e .
```

**Tests failing?**
- Check that component.py is in src/core/
- Verify that __init__.py exists in src/core/
- Make sure all mole fractions sum to 1.0

**Numerical precision errors?**
- Tests use tolerances (e.g., `< 0.001`) for floating point comparison
- This is normal and expected in engineering calculations

## 🔜 Next Week: Basic Thermodynamic Models

In Week 5, we'll implement:
- Ideal gas law
- Equations of state (van der Waals, Redlich-Kwong)
- Vapor-liquid equilibrium (Raoult's Law)
- Flash calculations
- Property prediction methods

This will enable us to predict phase behavior and equilibrium compositions!

## 📊 Your Progress So Far

### Completed:
- ✅ **Phase 0:** Project setup, Git, virtual environment
- ✅ **Week 3:** Component system with thermodynamic properties
- ✅ **Week 4:** Stream class with material balances

### What You Can Do Now:
- Create chemical components with properties
- Calculate vapor pressures and heat capacities
- Create process streams
- Mix and split streams
- Perform material balances
- Convert units

### Coming Soon:
- Thermodynamic calculations (VLE, flash)
- Unit operations (heat exchangers, separators, reactors)
- Flowsheet solving with recycles
- Dynamic simulation
- User interface

---

## 💪 Commit Your Work

```cmd
git add .
git commit -m "Phase 1 Week 4: Implement Stream class with material balance framework"
git push
```

---

**Excellent progress! 🎉** You've now built the two fundamental data structures (Components and Streams) that everything else will build upon!

When you're ready for Week 5, let me know! 🚀
