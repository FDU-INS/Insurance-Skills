# PolicyPulse — Technology Stack Document

**Version:** 1.0  
**Last Updated:** January 2025  
**Status:** Architecture Specification

---

## 1. Executive Summary

PolicyPulse is built on a **Python-centric, serverless-friendly architecture** that prioritizes rapid development, easy deployment, and the unique requirements of hybrid AI (LLM + neural network) workloads.

**Stack at a Glance:**

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Runtime** | Python 3.10+ | AI/ML ecosystem, type hints, dataclasses |
| **Web Framework** | Streamlit | Rapid prototyping, built-in state, easy deployment |
| **LLM Provider** | Google Gemini | Free tier, fast inference, structured output |
| **ML Framework** | Scikit-learn | Simple MLP, no GPU required, stable |
| **Data Processing** | Pandas + NumPy | Industry standard, performant |
| **Visualization** | Plotly | Interactive charts, Streamlit integration |
| **Persistence** | File-based (CSV, Joblib) | Simple, portable, no database setup |
| **Deployment** | Streamlit Cloud | Zero-config, free tier available |

---

## 2. Language Choice: Python 3.10+

### Why Python?

1. **AI/ML Ecosystem Dominance**: Google Generative AI SDK, Scikit-learn, NumPy, Pandas are all Python-native
2. **Rapid Prototyping**: Dynamic typing + rich standard library accelerates development
3. **Streamlit Requirement**: Streamlit is Python-only
4. **Type Safety with Flexibility**: Python 3.10+ dataclasses and type hints provide structure without boilerplate

### Why 3.10+?

| Feature | Benefit |
|---------|---------|
| Dataclasses | Clean data model definitions without boilerplate |
| Type hints | Better IDE support, self-documenting code |
| Pattern matching | Cleaner conditional logic (switch-like) |
| Union types (`X | None`) | Cleaner optional type syntax |
| Performance improvements | Faster startup, better memory |

### Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **JavaScript/TypeScript** | Would require building React frontend + Python backend for ML; doubles complexity |
| **Go** | Limited ML ecosystem; would need Python subprocess for AI anyway |
| **Rust** | Same ML ecosystem issue; overkill for this use case |

---

## 3. Web Framework: Streamlit

### Why Streamlit?

| Benefit | Explanation |
|---------|-------------|
| **Rapid Development** | Build complete UI in Python, no HTML/CSS/JS required |
| **Built-in State Management** | `st.session_state` handles complex simulation state |
| **Reactive Model** | Automatic re-runs on input change |
| **Deployment** | Streamlit Cloud provides free hosting with zero config |
| **Data-Native** | First-class support for DataFrames, charts, tables |
| **Active Community** | Extensive component ecosystem, frequent updates |

### Streamlit Constraints (Accepted)

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| **Single-threaded** | No true parallelism | Use async where possible; accept sequential LLM calls |
| **Session-based** | Data lost on reload | Persist models/data to files |
| **Limited customization** | Can't do pixel-perfect design | Accept Streamlit's design language |
| **No SEO** | Not a concern for app | Not relevant for internal tool |

### Configuration

```toml
# .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
base = "light"
primaryColor = "#667EEA"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F8FF"
textColor = "#262730"
```

### Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **Gradio** | Less flexible layout; more focused on ML demos than full apps |
| **Flask + React** | 10x more development time; separate frontend/backend |
| **Dash (Plotly)** | More verbose than Streamlit; less intuitive state management |
| **Panel (HoloViz)** | Smaller community; less mature |
| **Reflex** | Newer, less proven at scale |

---

## 4. LLM Provider: Google Gemini

### Why Gemini?

| Benefit | Details |
|---------|---------|
| **Free Tier** | 15 requests/minute, 200 requests/day at no cost |
| **Fast Inference** | Gemini Flash model optimized for speed |
| **Structured Output** | Good at following JSON output instructions |
| **Simple SDK** | `google-generativeai` package is straightforward |
| **Reliability** | Google infrastructure; high uptime |

### API Configuration

```python
# LLM client initialization
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')
```

### Rate Limiting Strategy

```python
# Enforce free tier limits
min_request_interval = 4.5  # seconds (60s / 15 requests = 4s + buffer)

# Before each request
elapsed = current_time - last_request_time
if elapsed < min_request_interval:
    time.sleep(min_request_interval - elapsed)
```

### Key Rotation for Extended Quotas

```python
# Support multiple API keys for higher throughput
api_keys = [primary_key] + backup_keys
current_key_index = 0

# On quota exhaustion, rotate to next key
if "quota exceeded" in error:
    current_key_index = (current_key_index + 1) % len(api_keys)
    genai.configure(api_key=api_keys[current_key_index])
```

### Fallback Chain

```
LLM Call Attempt
    │
    ├─ Success → Return LLM response
    │
    └─ Failure (quota/error)
           │
           ├─ Rotate to backup key → Retry
           │
           └─ All keys exhausted
                  │
                  └─ Fall back to Neural Network
                         │
                         ├─ NN trained → Return NN prediction
                         │
                         └─ NN not trained → Use rule-based logic
```

### Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **OpenAI GPT-4** | Paid only; $0.03/1K tokens adds up quickly |
| **Anthropic Claude** | Paid only; no free tier |
| **Llama (local)** | Requires GPU; complex setup |
| **Mistral API** | Smaller ecosystem; less tested |
| **Cohere** | Free tier more limited |

---

## 5. ML Framework: Scikit-learn

### Why Scikit-learn?

| Benefit | Explanation |
|---------|-------------|
| **Simplicity** | MLPRegressor in ~10 lines of code |
| **No GPU Required** | CPU inference is fast enough for our scale |
| **Mature & Stable** | 15+ years of development; extremely reliable |
| **Easy Serialization** | Joblib integration for model persistence |
| **Good Documentation** | Extensive examples and tutorials |

### Neural Network Architecture

```python
from sklearn.neural_network import MLPRegressor

model = MLPRegressor(
    hidden_layer_sizes=(64, 32),  # Two hidden layers
    activation='relu',
    max_iter=500,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1,
    n_iter_no_change=10
)
```

**Architecture Rationale:**
- **(64, 32)**: Sufficient capacity for 24-dim input → 3-dim output mapping
- **ReLU**: Standard activation, fast and effective
- **Early stopping**: Prevents overfitting on small datasets
- **Validation split**: 10% held out for generalization monitoring

### Feature Engineering

```python
# 24-dimensional feature vector
features = [
    age / 100,                           # Normalized age (1)
    *one_hot(income_level, 3),           # Income level (3)
    *one_hot(city_zone, 4),              # City zone (4)
    *one_hot(political_view, 3),         # Political view (3)
    risk_tolerance,                       # Personality (1)
    openness_to_change,                   # Personality (1)
    family_size / 10,                     # Normalized (1)
    prev_happiness,                       # Previous state (1)
    prev_support,                         # Previous state (1)
    log1p(prev_income) / 10,              # Log-scaled income (1)
    *one_hot(policy_domain, 4)            # Policy context (4)
]
# Total: 1+3+4+3+1+1+1+1+1+1+4 = 21 (some additional encoding may vary)
```

### Model Persistence

```python
import joblib

# Save
joblib.dump(model, 'models/citizen_reaction_model.joblib')

# Load
model = joblib.load('models/citizen_reaction_model.joblib')
```

### Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **PyTorch** | Overkill for simple MLP; adds complexity |
| **TensorFlow/Keras** | Same as PyTorch; unnecessary for this scale |
| **XGBoost** | Tree-based; less suitable for this regression task |
| **Custom NumPy** | More work, no benefit |

---

## 6. Data Processing: Pandas + NumPy

### Pandas Usage

```python
import pandas as pd

# Convert citizens to DataFrame for analysis
df = pd.DataFrame([citizen_to_dict(c) for c in citizens])

# Aggregation
avg_happiness = df.groupby('income_level')['happiness'].mean()

# Export
df.to_csv('data/simulation_results.csv', index=False)
```

### NumPy Usage

```python
import numpy as np

# Feature vector construction
features = np.array([...], dtype=np.float32)

# Random generation
rng = np.random.default_rng(seed=42)
ages = rng.integers(18, 71, size=population_size)

# Statistics
mean = np.mean(happiness_values)
std = np.std(happiness_values)

# Clipping
happiness = np.clip(new_value, 0.0, 1.0)
```

### Why This Combination?

- **NumPy** for numerical operations (fast, vectorized)
- **Pandas** for structured data manipulation (filtering, grouping, export)
- **Seamless interop** between the two
- **Universal knowledge**: Any Python developer knows these

---

## 7. Visualization: Plotly

### Why Plotly?

| Benefit | Explanation |
|---------|-------------|
| **Interactive** | Hover, zoom, pan built-in |
| **Streamlit Integration** | `st.plotly_chart()` native support |
| **Rich Chart Types** | Line, bar, pie, scatter, heatmap, etc. |
| **Professional Appearance** | Publication-quality by default |
| **Client-Side Rendering** | No server processing for visualization |

### Chart Implementation Examples

```python
import plotly.express as px
import plotly.graph_objects as go

# Line chart
fig = px.line(
    df,
    x="Step",
    y="Happiness",
    title="Happiness Over Time",
    markers=True
)
fig.update_layout(yaxis_range=[0, 1])
st.plotly_chart(fig, use_container_width=True)

# Bar chart
fig = px.bar(
    df,
    x="income_level",
    y="avg_happiness",
    color="income_level",
    title="Happiness by Income Level"
)
st.plotly_chart(fig, use_container_width=True)

# Stacked bar (for method breakdown)
fig = go.Figure(data=[
    go.Bar(name='LLM', x=steps, y=llm_counts),
    go.Bar(name='NN', x=steps, y=nn_counts),
    go.Bar(name='Rule', x=steps, y=rule_counts)
])
fig.update_layout(barmode='stack')
```

### Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **Altair** | Less interactive; declarative style less flexible |
| **Matplotlib** | Static; requires extra work for interactivity |
| **Bokeh** | Less intuitive API; smaller community |
| **Streamlit native charts** | Limited customization |

---

## 8. Persistence Strategy: File-Based

### Why Not a Database?

| Reason | Explanation |
|--------|-------------|
| **Simplicity** | No database setup, no connection management |
| **Portability** | Works on any system, including Streamlit Cloud |
| **Scope** | Single-user app; no concurrent access needs |
| **Data Size** | Training data is small (thousands of rows max) |
| **Deployment** | Streamlit Cloud doesn't support persistent databases well |

### File Storage Schema

```
project_root/
├── data/
│   └── llm_training_samples.csv     # Training data
└── models/
    ├── citizen_reaction_model.joblib # Trained neural network
    └── feature_scaler.joblib         # Feature normalization
```

### CSV Format for Training Data

```csv
feature_0,feature_1,...,feature_23,delta_happiness,delta_support,delta_income
0.45,1,0,0,0,1,0,0,...,0.05,-0.1,15.0
0.32,0,1,0,1,0,0,0,...,-0.03,0.2,-25.0
```

### Session State for Runtime Data

```python
# Streamlit session state (in-memory)
st.session_state.scenarios = {}          # Simulation results
st.session_state.current_population = [] # Generated citizens
st.session_state.nn_model = None         # Loaded neural network
st.session_state.training_dataset = []   # Accumulated samples
```

### Persistence Lifecycle

```
Session Start
    │
    ├─ Load trained model (if exists)
    │
    ├─ Load training samples (if exist)
    │
    └─ Initialize empty session state

During Session
    │
    ├─ Simulations add to session state
    │
    ├─ LLM samples accumulate in training dataset
    │
    └─ User triggers model training

Session End (or explicit save)
    │
    ├─ Save training samples to CSV
    │
    └─ Save trained model to Joblib
```

---

## 9. Architecture Pattern

### Pattern: Modular Monolith

PolicyPulse follows a **modular monolith** architecture—a single deployable unit with clear internal module boundaries.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PolicyPulse Application                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│   │  UI Layer    │  │  UI Layer    │  │  UI Layer    │             │
│   │  (app.py)    │  │ (ui_sections)│  │              │             │
│   └──────┬───────┘  └──────┬───────┘  └──────────────┘             │
│          │                 │                                        │
│          ▼                 ▼                                        │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                    Simulation Engine                         │  │
│   │                    (simulation.py)                          │  │
│   └────────┬────────────────┬────────────────┬──────────────────┘  │
│            │                │                │                      │
│            ▼                ▼                ▼                      │
│   ┌──────────────┐  ┌──────��───────┐  ┌──────────────┐             │
│   │ LLM Client   │  │ NN Model     │  │ Population   │             │
│   │ (llm_client) │  │ (nn_model)   │  │ (population) │             │
│   └──────────────┘  └──────────────┘  └──────────────┘             │
│            │                │                                       │
│            ▼                ▼                                       │
│   ┌──────────────┐  ┌──────────────┐                               │
│   │ External API │  │ File Storage │                               │
│   │ (Gemini)     │  │ (CSV/Joblib) │                               │
│   └──────────────┘  └──────────────┘                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|----------------|--------------|
| `app.py` | Entry point, session management, main flow | All modules |
| `ui_sections.py` | UI component rendering | data_models, utils |
| `simulation.py` | Simulation loop orchestration | llm_client, nn_model, population |
| `llm_client.py` | Gemini API wrapper | google-generativeai |
| `nn_model.py` | Neural network training/inference | scikit-learn |
| `population.py` | Synthetic citizen generation | numpy |
| `stats.py` | Aggregation and statistics | pandas, numpy |
| `data_models.py` | Dataclass definitions | stdlib only |
| `utils.py` | Helper functions | numpy |
| `config.py` | Environment loading | python-dotenv |
| `ml_data.py` | Training dataset management | numpy, pandas |

### Dependency Flow

```
config.py ←── app.py ──→ ui_sections.py
                │
                ▼
         simulation.py
          │   │   │
          ▼   ▼   ▼
    llm  nn_model population
     │      │
     ▼      ▼
   genai  sklearn
```

---

## 10. Scalability Philosophy

### Current Scale Targets

| Dimension | Target | Rationale |
|-----------|--------|-----------|
| Population size | 50,000 citizens | Upper limit for reasonable memory usage |
| Simulation steps | 10 | Sufficient for trend analysis |
| LLM calls per step | 300 | Balance sampling quality vs. time |
| Total training samples | 10,000+ | Enough for NN generalization |
| Concurrent users | 1 | Single-user application by design |

### Scaling Strategies (Future)

| Strategy | When Needed | Implementation |
|----------|-------------|----------------|
| **Async LLM calls** | Faster simulations | `asyncio` with concurrent API calls |
| **Batch NN inference** | Larger populations | Vectorized NumPy operations |
| **Redis caching** | Repeated similar queries | Cache LLM responses by prompt hash |
| **Background jobs** | Long simulations | Celery or similar task queue |
| **Multi-user** | Production deployment | Add database, authentication |

### What We Explicitly Don't Scale For (MVP)

| Not Supported | Why |
|---------------|-----|
| Millions of citizens | Would require distributed computing |
| Real-time streaming | Batch-oriented by design |
| Multi-tenant | Single-user, session-based |
| Persistent history | File-based, ephemeral storage |

---

## 11. Security Considerations

### Threat Model (Minimal)

| Threat | Risk Level | Mitigation |
|--------|------------|------------|
| API key exposure | Medium | Environment variables, `.gitignore` |
| Data breach | Low | No real user data; all synthetic |
| Injection attacks | Low | Streamlit handles input sanitization |
| Unauthorized access | Low | No authentication needed for demo |

### API Key Management

```python
# Load from environment (not hardcoded)
api_key = os.getenv("GEMINI_API_KEY")

# Mask in logs
masked = f"{key[:8]}...{key[-4:]}"
logger.info(f"Using API key: {masked}")
```

### Production Hardening (Future)

| Improvement | Implementation |
|-------------|----------------|
| Secrets