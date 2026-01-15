# Django Assessment Solutions

This repository contains the solutions for the AccuKnox technical assessment. The project is structured as a standard Django application, with all logic encapsulated in the `answers` app.

## Project Structure
* App Name: `answers`
* Logic Location: `answers/views.py` (Contains all proofs and custom classes)
* URL Configuration: `answers/urls.py`

## Setup Instructions

1.  Clone the repository
    ```bash
    git clone https://github.com/acaff-real/accuknoxassesment/
    cd accuknox-django-assessment
    ```

2.  Create and Activate Virtual Environment
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

4.  Run Migrations (Required for Question 3 database transaction proof)
    ```bash
    python manage.py migrate
    ```

5.  Run the Server
    ```bash
    python manage.py runserver
    ```

## Solutions & Verification
Each question has a dedicated URL endpoint that executes the proof and returns the results in JSON format.

| Question | Topic | Endpoint | Expected Result |
| :--- | :--- | :--- | :--- |
| Q1 | Signals: Sync vs Async | `http://localhost:8000/thread-proof/` | Synchronous. The View and Receiver run on the same thread. |
| Q2 | Signals: Threading | `http://localhost:8000/question-2/` | Same Thread. The Thread IDs are identical. |
| Q3 | Signals: Transactions | `http://localhost:8000/question-3/` | Same Transaction. The Signal's DB entry is rolled back along with the Caller's. |
| Q4 | Python Custom Class | `http://localhost:8000/question-4/` | `Rectangle` class iterates correctly yielding `length` then `width`. |

## Implementation Details

### Questions 1-3: Django Signals
All signal logic is implemented in `answers/views.py`.
* Q1 & Q2: Use `threading.current_thread()` and `threading.get_native_id()` to prove execution context.
* Q3: Uses `transaction.atomic()` and a custom model (`AuditEntry`) to demonstrate transaction rollback sharing.

### Question 4: Custom Python Class
The `Rectangle` class is defined in `answers/views.py` with a custom `__iter__` method that yields dictionaries in the required format:
```python
yield {'length': self.length}
yield {'width': self.width}
