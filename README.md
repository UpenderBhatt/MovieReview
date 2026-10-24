# Movie Reviews Website

A movie review website built with Flask that pulls live film data from [The Movie Database (TMDB)](https://www.themoviedb.org/) API. Users can browse popular, highest-grossing and most-rated films, search for a movie, and view its details, cast, trailers and reviews.

> **Team project:** this was built as a university group project at Cardiff University, so it is **not solely my own work**. To protect my teammates' privacy, their names and the original commit history are not included in this repository. The "My contributions" section below describes the parts I worked on.

## Features

- Home page with lists of popular, highest-grossing and most-rated movies
- Movie search
- Movie pages with details, cast, trailers and reviews
- Leave-a-review page and a prototype login page

## My contributions

- Set up the initial project structure, files and folders
- Built the first layout of the movie review page
- Styled the site for a consistent design across all pages
- Built the login page and connected its form to the Flask server

## Tech stack

Python 3.12 · Flask · Jinja2 templates · HTML / CSS / JavaScript · TMDB API

## Getting started

### Prerequisites

- Python 3.12 or newer
- A free TMDB account and its **API Read Access Token**: sign up at themoviedb.org, then go to *Settings → API*

### 1. Clone and install

```bash
git clone <this-repo-url>
cd <repo-folder>
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your TMDB token

The token is never stored in the code. It is read from the `TMDB_API_TOKEN` environment variable (see [`.env.example`](.env.example)):

```bash
export TMDB_API_TOKEN="your-read-access-token"      # macOS / Linux
$env:TMDB_API_TOKEN="your-read-access-token"       # Windows PowerShell
```

### 3. Run

```bash
python JinjaServer.py
```

Then open <http://127.0.0.1:5000/Base>. To turn on Flask's debug mode while developing, set `FLASK_DEBUG=1`. Never turn it on for a public deployment.

## Notes

The login page is a prototype and does not authenticate users. It saves the submitted email and a **hashed** (never plain-text) password to a local `loginDetails.txt` file, which is excluded from Git.
