# Miel-IA 🧠💡

Miel-IA is an intelligent medical diagnostic support system designed to analyze electromyography (EMG) data and determine the potential presence of Guillain-Barré Syndrome (GBS). Using multiple machine learning models and a microservices-based architecture (or simplified monolithic setup as needed), Miel-IA offers binary results and risk classification in an orchestrated and precise manner.

---

## 🏗 Architecture

The system follows a **SAGA orchestration pattern**, running sequentially to prevent server overload and facilitate scaling. It includes:

- **REST API** built with **FastAPI**
- **Binary ML models** to predict the presence of GBS:
  - Random Forest
  - XGBoost
  - Linear Regression
- **Decision service** that aggregates binary results to determine a possible POSITIVE match
- **Classification ML models** to assess risk level:
  - HIGH, MEDIUM, or LOW
- **Classification service** that combines the classification model outputs
- **PostgreSQL database in Docker** managed with SQLAlchemy

### 📊 Mermaid Diagram
```mermaid
---
config:
  theme: dark
  look: classic
---
flowchart TD
 subgraph subGraph0["🧩 API REST (FastAPI)"]
        A1["Entrada: Datos EMG"]
        A2["Salida: Resultado diagnóstico"]
  end
 subgraph subGraph1["🧠 Orquestador (Caso de uso principal)"]
        ORQ["Orquestador"]
  end
 subgraph subGraph2["🤖 Modelos de Detección Binaria"]
        B1["Random Forest Binario"]
        B2["XGBoost Binario"]
        B3["Logistic Regression Binario"]
  end
 subgraph subGraph3["🧪 Modelos de Clasificación"]
        C1["Random Forest Clasificación"]
        C2["XGBoost Clasificación"]
        C3["Logistic Regression Clasificación"]
  end
 subgraph subGraph4["🗃️ Base de Datos de Pacientes"]
        DB["DB MySQL (consultar/guardar)"]
  end
    A1 --> ORQ
    ORQ --> B1 & B2 & B3 & C1 & C2 & C3 & DB & A2

```

---

## 🧪 User Stories (Kanban ToDo)

- **US-01**: As a researcher, I want to use the EMG dataset to train the model, to improve the accuracy in detecting GBS.
- **US-02**: As a developer, I want to train a machine learning model to provide a compatibility score with GBS.
- **US-03**: As a developer, I want to integrate the REST API with the AI model, to process EMG data and return analysis results.
- **US-04**: As a doctor, I want to visualize the analysis results in a graphical and intuitive way, to facilitate interpretation of the automated diagnosis.

---

## 🧬 General Workflow

1. The user (doctor or system) uploads a labeled CSV file.
2. The REST API starts a **synchronous sequential saga**:
   - The three binary models are executed one by one.
   - If at least 2 models agree (based on a threshold), the result is considered **POSITIVE**.
3. If the result is POSITIVE, the same CSV is sent to the three classification models.
4. The **classification service** evaluates and reports the risk level (HIGH/MEDIUM/LOW).
5. The final response is returned to the REST API.

---

## 📦 Installation & Execution

### Requirements
- Python 3.10+
- Docker (optional for PostgreSQL)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configuration
Create a `.env` file at the root with the following content:
```
DATABASE_URL=postgresql://user:password@localhost:5432/mielia_db
THRESHOLD_BINARY=0.6
THRESHOLD_CLASSIFY=0.5
```

### Run API
```bash
uvicorn main:app --reload
```

### Train models
```bash
python train.py
```

---

## 🔎 Project Structure
```
miel_ia/
├── .env
├── main.py
├── train.py
├── saga.py
├── decision_service.py
├── classification_service.py
├── requirements.txt
├── models/
│   ├── binary_random_forest.py
│   ├── binary_xgboost.py
│   ├── binary_linear_regression.py
│   ├── classify_random_forest.py
│   ├── classify_xgboost.py
│   ├── classify_linear_regression.py
└── db/
    └── models.py
```

---

## 💡 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Scikit-learn](https://scikit-learn.org/)
- [XGBoost](https://xgboost.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🚀 Project Status

Currently under development. Initial model training implementation in progress (US-01 and US-02).

---

## 📌 Additional Notes

- The architecture may scale toward full microservices if justified in a production environment. For now, it remains monolithic to simplify early development.
- The project is run locally. No cloud deployment is planned yet.

---

## 👨‍🔬 Author

Developed by [Pablo Mirazo](https://x.com/iamD3XTRO) - Computer Engineering student.

This project was created to provide intelligent diagnostic tools for healthcare professionals, particularly for early detection of Guillain-Barré Syndrome.

---

> "The best diagnosis is the one that comes in time." 🧠⚕️

