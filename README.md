# BuildBridge — Construction & Property Broker Platform

A runnable Flask + SQLite starter marketplace for people seeking construction services, contractors, material suppliers, and property brokers.

## Features
- Home dashboard with search and category filters
- Browse service listings
- Add a new listing through a form
- SQLite database created automatically
- Listing detail page and contact information
- Responsive layout
- Demo seed data on first run

## Requirements
- Python 3.10+
- No external API key required

## Run on Windows (VS Code / CMD)
```bash
cd buildbridge_broker
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`

On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Demo credentials
There is no login/authentication in this starter version. Do not publish it as a production service without adding authentication, validation, CSRF protection, rate limiting, secure configuration, and privacy controls.

## Database
The app creates `buildbridge.db` in the project folder automatically.

## Suggested next steps
- Add user registration/login and role-based access (buyer, broker, contractor, supplier)
- Add image uploads and document verification
- Add enquiry/booking workflows and email/SMS notifications
- Add maps, reviews, admin moderation, and deployment configuration
