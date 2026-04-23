# PolicyPulse

🎯 **AI-powered synthetic population simulator for stress-testing policies**

PolicyPulse enables organizations to stress-test policies, business strategies, and social initiatives against virtual citizen populations before real-world implementation.

## Overview

Transform how organizations make high-stakes decisions by providing a risk-free simulation environment where the impact of policies can be observed across diverse demographic segments, tracked over time, and analyzed from multiple stakeholder perspectives.

### Key Features

- **Synthetic Population Generation**: Create populations of 100 to 50,000 virtual citizens with realistic demographic distributions
- **Hybrid AI Simulation**: Three modes for different speed/quality tradeoffs
  - **Precision Mode**: LLM-powered reactions for maximum nuance
  - **Balanced Mode**: Hybrid LLM sampling + neural network scaling
  - **Speed Mode**: Trained neural network only (fast, offline-capable)
- **Analytics Dashboard**: Time-series visualizations, demographic breakdowns, inequality tracking
- **Expert Perspectives**: AI-generated analysis from economist, activist, and business viewpoints
- **Scenario Comparison**: Compare multiple policy simulations side-by-side

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key (for Precision/Balanced modes)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Vibecraft

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Running the Application

```bash
streamlit run src/app.py
```

The application will open in your browser at `http://localhost:8501`.

## Project Structure

```
Vibecraft/
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── data/
│   └── README.md            # Training data storage
├── models/
│   └── README.md            # Trained model storage
├── src/
│   ├── app.py               # Main Streamlit application
│   ├── config.py            # Environment configuration
│   ├── data_models.py       # Dataclass definitions
│   ├── llm_client.py        # Google Gemini API wrapper
│   ├── ml_data.py           # Training data management
│   ├── nn_model.py          # Neural network model
│   ├── population.py        # Population generation
│   ├── simulation.py        # Simulation orchestration
│   ├── stats.py             # Statistics and aggregation
│   ├── ui_sections.py       # UI component rendering
│   └── utils.py             # Utility functions
├── tests/
│   ├── test_data_models.py
│   ├── test_utils.py
│   └── ...
├── .env.example             # Environment template
├── .gitignore
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
├── PRD.md                   # Product Requirements Document
├── DESIGN_DOC.md            # UI/UX Design Specification
├── TECH_STACK.md            # Technology Architecture
└── SKILL.md                 # AI coding assistant guidelines
```

## Architecture

PolicyPulse follows a **modular monolith** pattern:

- **UI Layer** (`app.py`, `ui_sections.py`): Streamlit components
- **Simulation Engine** (`simulation.py`): Orchestrates the hybrid AI workflow
- **AI Modules** (`llm_client.py`, `nn_model.py`): LLM and neural network integration
- **Data Layer** (`data_models.py`, `ml_data.py`, `stats.py`): Data structures and persistence

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Type Checking

```bash
mypy src/
```

### Code Style

The project uses Python 3.10+ type hints throughout. All functions should have complete type annotations.

## Documentation

- [PRD.md](PRD.md) - Product Requirements Document
- [DESIGN_DOC.md](DESIGN_DOC.md) - UI/UX Design Specification
- [TECH_STACK.md](TECH_STACK.md) - Technology Architecture Decisions
- [SKILL.md](SKILL.md) - AI Coding Assistant Guidelines

## Disclaimer

⚠️ **Synthetic Simulation Disclaimer**

This tool creates fictional scenarios for exploratory purposes. Results do not predict real-world behavior. Use as a thought experiment to identify potential blind spots—not as a substitute for real data, surveys, or expert analysis.

## License

MIT License
