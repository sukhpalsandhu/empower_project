I have created the following files for your Python project:

1.  `c:\code\empower\empower_project\requirements.txt`
2.  `c:\code\empower\empower_project\main.py`
3.  `c:\code\empower\empower_project\.env` (for storing credentials, added to .gitignore)

Due to limitations in the current environment, I cannot directly execute shell commands to set up the virtual environment or install dependencies. Please follow these manual steps to complete the project setup and run the script:

**Manual Setup Instructions:**

1.  **Create the project directory (if it doesn't exist):**
    If the directory `c:\code\empower\empower_project` does not exist, please create it manually.

2.  **Ensure files are in place:**
    Make sure `requirements.txt`, `main.py`, and `.env` are located inside `c:\code\empower\empower_project`.

3.  **Open a terminal or command prompt:**
    Navigate to the `c:\code\empower\empower_project` directory in your terminal.

4.  **Create a virtual environment:**
    Run the following command:
    ```bash
    python -m venv venv
    ```

5.  **Activate the virtual environment:**
    *   **On Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

6.  **Install dependencies:**
    While the virtual environment is active, run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `empower-personal-capital` and `python-dotenv`.

7.  **Set credentials in .env file:**
    Open the `.env` file in `c:\code\empower\empower_project` and add your Empower Personal Capital credentials in the following format:

    ```
    EMPOWER_EMAIL="your_email@example.com"
    EMPOWER_PASSWORD="your_password"
    ```
    The `main.py` script will now load these credentials from the `.env` file.

8.  **Run the script:**
    While the virtual environment is active, run:
    ```bash
    python main.py
    ```

This will execute the `main.py` script, which attempts to connect to Empower Personal Capital and fetch your net worth and account information.