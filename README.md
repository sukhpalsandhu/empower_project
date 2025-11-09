# Empower Project

This project provides tools to retrieve financial data from Empower Personal Capital. It includes a command-line interface (`main.py`) and a Flask-based API (`api.py`).

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd empower_project
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the project root directory with your Empower Personal Capital credentials:
    ```
    EMPOWER_EMAIL="your_email@example.com"
    EMPOWER_PASSWORD="your_empower_password"
    ```
    **Important:** Replace `"your_email@example.com"` and `"your_empower_password"` with your actual login credentials.

## Usage

### Command-Line Interface (CLI) - `main.py`

The `main.py` script fetches your financial data and prints it to the console as JSON. This script also handles Two-Factor Authentication (2FA) interactively. Running this script and completing any 2FA prompts will establish a persistent session, which is beneficial for the API.

To run the CLI:
```bash
python main.py
```

### API - `api.py`

The `api.py` script starts a Flask web server that exposes an endpoint to retrieve financial data. This API now internally calls `main.py` to fetch the data, leveraging `main.py`'s ability to handle 2FA and session management.

To run the API server:
```bash
python api.py
```

The API will be available at `http://127.0.0.1:5000`. You can access the financial data by navigating to `http://127.0.0.1:5000/get_financial_data` in your web browser or by making an HTTP GET request to this endpoint.

## Important Notes

*   **Two-Factor Authentication (2FA):** If your Empower Personal Capital account has 2FA enabled, it is highly recommended to run `main.py` first and complete the 2FA process. This will create a `session.json` file that helps establish a persistent session, allowing `api.py` to retrieve data without requiring interactive 2FA.
*   **`session.json`:** A `session.json` file will be created in the project root after a successful login via `main.py`. This file stores your session cookies to avoid repeated logins. It is ignored by `.gitignore` for security reasons.
*   **Security:** Never commit your `.env` file or `session.json` to version control. These files contain sensitive credentials.
*   **Performance (API):** The current implementation of `api.py` calls `main.py` as a subprocess for each request. While this addresses the 2FA challenge, it is not the most performant solution for a high-traffic API. For better performance, consider refactoring the common Personal Capital interaction logic into a shared module that both `main.py` and `api.py` can import directly.
