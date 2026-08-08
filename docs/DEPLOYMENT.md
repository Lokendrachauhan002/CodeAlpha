# Installation and Deployment Guide

## Localhost

Follow the README setup, then run `python run.py`. Development mode runs on `http://127.0.0.1:5000`. Do not expose Flask's debug server publicly.

## GitHub

Create a repository, then from this project folder run:

```powershell
git init
git add .
git commit -m "Initial offline FAQ chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/campusassist.git
git push -u origin main
```

Never commit `.venv`, logs, or secrets. This project has no API keys.

## Render

1. Push the project to GitHub and create a new Render Web Service.
2. Choose Python, set Build Command to `pip install -r requirements.txt && python -m spacy download en_core_web_sm`.
3. Set Start Command to `gunicorn 'backend.app:create_app()'` and add `gunicorn` to your production requirements if you use this command.
4. Select the free or paid plan, deploy, and use the generated HTTPS URL.

For a minimal platform build, the app falls back to blank spaCy tokenization if the model download is omitted.

## Railway

1. Create a Railway project and deploy the linked GitHub repository.
2. Use the same build command as Render.
3. Set the start command to `gunicorn 'backend.app:create_app()'`.
4. Add the domain in Railway's networking settings.

For production, set `debug=False`, use a production WSGI server, and ensure the platform preserves or redirects logs as appropriate.
