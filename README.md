# Industrial Plant Simulation Software

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: In Development](https://img.shields.io/badge/status-in%20development-orange.svg)]()

> **Educational Project Notice**: This is a learning/educational project aimed at understanding chemical process simulation software architecture. Not intended for commercial or production use.

## 🎯 Project Overview

An open-source industrial plant simulation software for chemical process engineering, similar to Aspen HYSYS/Plus but designed for educational purposes. This project implements steady-state and dynamic modeling capabilities for chemical processes.

### Key Features (Planned)

- **Thermodynamic Models**: Ideal gas, van der Waals, Peng-Robinson, SRK, activity coefficient models
- **Unit Operations**: Mixers, separators, heat exchangers, distillation columns, reactors, compressors, and more
- **Flowsheet Solver**: Sequential modular and equation-oriented solving with convergence algorithms
- **Dynamic Simulation**: Time-dependent process simulation with control systems
- **User Interface**: Intuitive GUI for flowsheet creation and visualization
- **Property Database**: Comprehensive component property database

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.10 or higher
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/plant-simulation-software.git
cd plant-simulation-software

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (once available)
pip install -r requirements.txt
```

## 📁 Project Structure

```
Plant Simulator/
│
├──data/                            # Data
│   └──components/                  # Component Property Database 
│
├──docs/                            # Documentation
│
├──examples/                        # Mockups and Example Flowsheets
│
├──notebooks/                       # Jupyter Notebooks for specific testing and application
│
├──sandbox/                         # Python Scripts for specific testing and applications
│
├──src/                             # Main Source Code
│   ├──core/                        # Core data structures (streams, components)
│   ├──dimanal/                     # Dimensional analysis utilities
│   ├──dynamics/                    # Dynamic simulation engine
│   ├──gui/                         # User Interface (planned)
│   ├──solver/                      # Flowsheet solver algorithms
│   ├──thermo/                      # Thermodynamic models and calculations
│   └──units/                       # Unit operation modules
│
├──tests/                           # Unit and integration tests
│
├──README.md                        # Project overview and setup instructions
│
├──requirements.txt                 # Project dependencies
│
└──setup.py                          # Installation script

```

## 🛠️ Technology Stack

- **Core**: Python 3.10+
- **Scientific Computing**: NumPy, SciPy, Pandas
- **Thermodynamics**: CoolProp, Thermo
- **Visualization**: Matplotlib, Plotly
- **GUI**: PyQt6/PySide6 (planned)
- **Testing**: pytest
- **Documentation**: Sphinx

## 📚 Development Roadmap

### Phase 0: Setup (Weeks 1-2) ✅ *Current Phase*
- [x] Project planning and architecture
- [x] Version control setup
- [x] Development environment configuration
- [x] Initial documentation

### Phase 1: Foundation (Weeks 3-6)
- [x] Component database
- [x] Stream calculations
- [x] Basic thermodynamic models
- [x] Dimensional analysis utilities

### Phase 2: Unit Operations (Weeks 7-14)
- [ ] Basic unit operations (mixer, splitter, heat exchanger, etc.)
- [ ] Advanced unit operations (distillation, reactors, compressors)

### Phase 3-10: Advanced Features
See [Project Timeline](docs/TIMELINE.md) for detailed roadmap.

## 🧪 Current Status

**Version**: 0.1.0-dev  
**Phase**: Project Setup  
**Progress**: Foundation phase

This project is in very early development. The architecture is being designed and core components are not yet implemented.

## 🤝 Contributing

This is primarily a solo learning project, but feedback and suggestions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📖 Documentation
- [Project Overview](README.md) - This file
- [Project Timeline](docs/TIMELINE.md) - Detailed 52-week development plan
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and architecture (coming soon)
- [User Manual](docs/USER-MANUAL.md) - User documentation (coming soon)
- [API Reference](docs/API-REFERENCE.md) - Developer API documentation (coming soon)
- [Formating Guide](docs/FORMATING_GUIDE.md) - Code style and contribution guidelines

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by commercial software: Aspen HYSYS, Aspen Plus, DWSIM, COCO
- Thermodynamic references: Smith, Van Ness & Abbott
- Educational resources: AIChE DIPPR, NIST Chemistry WebBook

## 📧 Contact

Project Creator: Allen Aguillard
Project Link: [https://github.com/allena90/Plant-Simulator](https://github.com/allena90/Plant-Simulator)

---

**⚠️ Disclaimer**: This is an educational project for learning purposes. Not suitable for industrial design or safety-critical applications. Always verify results with established commercial software for real-world applications.
