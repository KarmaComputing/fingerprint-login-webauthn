# Fingerprint Website Login - Webauthn

## Setup

Set .env
```
cp .env.example .env
```

Then

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
## Run locally
```
uvicorn --reload app:app
```

Visit: http://localhost:8000/
