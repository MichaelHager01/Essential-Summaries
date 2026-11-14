# Essential Summaries

A bilingual Flask site that lets a client upload deposition, medical-record, discovery, and miscellaneous PDFs into a Google Drive folder named with their email.

## What it does

- The page toggles between English and Spanish.
- On submit, the app creates a subfolder under a parent Drive folder and uploads each PDF with a type prefix.
- Drive access uses a service-account JSON file. That file is not in the repository. `src/flask_app.py` currently points at the PythonAnywhere path `/home/essentialsummaries/mysite/client_secret_EssentialSummaries.json`, and the parent folder id is the placeholder `FOLDER_ID_SECRET`. Set both before a real upload will succeed.

## Layout

- `src/flask_app.py` — routes, folder creation, and uploads
- `src/Google.py` — builds the Drive service from the service account
- `templates/index.html` — the upload form and the language toggle
- `static/css/styles.css` — page styles

## Run

From the repository root:

```bash
pip install -r requirements.txt
python src/flask_app.py
```

Templates and static files stay at the repository root because that is where Flask serves them.

## Stack

Python, Flask, and the Google Drive API.
