# Skill Gap Analyzer

Skill Gap Analyzer is a Flask web app that helps students identify weak academic areas from an uploaded Excel marksheet. It reads subject-wise marks, highlights subjects below the configured threshold, and recommends starter courses for those subjects.

## Features

- User signup, login, logout, and session-based access
- Excel upload for subject and marks analysis
- Skill gap detection for subjects scoring below 60
- Course recommendations from the local SQLite database
- Important insights page with average, highest, lowest, and weak-subject summaries
- Personal notes section with save and download support
- Sample Excel files included for quick testing

## Tech Stack

- Python
- Flask
- SQLite
- pandas
- openpyxl
- Bootstrap 4

## Project Structure

```text
.
+-- README.md
`-- skillgap/
    +-- App.py
    +-- requirements.txt
    +-- skillgap.db
    +-- templates/
    |   +-- important.html
    |   +-- index.html
    |   +-- login.html
    |   `-- signup.html
    +-- static/
    |   +-- background.jpg
    |   +-- style.css
    |   `-- images/
    `-- uploads/
        `-- sample Excel files
```

## Getting Started

### Prerequisites

- Python 3.10 or newer recommended
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/kushal040511/skill-gap-.git
cd skill-gap-
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r skillgap/requirements.txt
```

Run the app:

```bash
python skillgap/App.py
```

Open the app in your browser:

```text
http://127.0.0.1:5002
```

## Excel Upload Format

Uploaded Excel files must include these columns:

| Subject | Marks |
| ------- | ----- |
| Mathematics | 55 |
| Physics | 72 |
| English | 48 |

Subjects with marks below `60` are treated as skill gaps. The app then looks up matching course recommendations from the `skill_courses` table in `skillgap.db`.

## Usage

1. Start the Flask app.
2. Create an account from the signup page.
3. Log in with your username and password.
4. Upload an Excel file containing `Subject` and `Marks` columns.
5. Review recommended courses for weak subjects.
6. Visit the Important Insights page to view average marks, highest subject, lowest subject, and weak subjects.
7. Save notes for later reference from the notes section.

## Database

The app uses SQLite through `skillgap/skillgap.db`. On startup, `init_db()` creates these tables if they do not already exist:

- `users`
- `skill_courses`
- `user_notes`

If the course table is empty, the app inserts sample subject-to-course recommendations.

## Development Notes

- The Flask app entrypoint is `skillgap/App.py`.
- The app runs on port `5002` by default.
- User passwords are currently stored in plain text, so this project should be treated as a learning/demo app unless password hashing is added.
- There is a `/recommended-books` route in `App.py`, but the corresponding `recommended_books.html` template is not currently present.

## License

No license file is currently included. Add a license before using or distributing this project publicly.
