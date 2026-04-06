# PakWheels Price Prediction App

Minimal FastAPI + Streamlit app for predicting `High Price` vs `Low Price` using `pakwheels_svm_model.pkl`.

## Files
- `backend.py` - API server (`/predict`)
- `frontend.py` - Streamlit UI
- `pakwheels_svm_model.pkl` - pretrained model
- `requirements.txt` - dependencies

## Setup (Virtual Environment + Requirements)
From project folder:

```bash
python -m venv env
```

Activate:

```bash
env\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

## Run
Open **two terminals** in this folder.

1) Backend:
```bash
python backend.py
```

2) Frontend:
```bash
streamlit run frontend.py
```

## Open
- Frontend: `http://localhost:8501`
- API docs: `http://localhost:8000/docs`

```

