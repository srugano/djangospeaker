# Django speaker Recognition System

This Django project implements a speaker recognition system using the (`speechbrain`)[https://github.com/speechbrain/speechbrain] library.


## Features

- **voice Encoding**: Encodes voices from a training dataset and stores the encodings in a database.
- **voice Recognition**: Compares new face encodings against stored encodings to recognize individuals.
- **Asynchronous Task Processing**: Utilizes Celery for handling time-consuming tasks like face encoding and recognition.
- **Scalable Architecture**: Designed to handle a growing number of face recognition requests efficiently.

## Getting Started

### Prerequisites

- Python 4.x
- Django
- Celery

### Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/djangospeaker.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd djangospeaker
   ```
3. Install packages
   ```bash
   pip install requirements.txt
   ```

### Configuration

1. Run migrations to set up your database:
  ```python 
    python manage.py migrate
  ```

### Running the Project

1. Start the Django development server:
  ```python 
  python manage.py runserver
  ```
2. From the admin site
3. Add individuals from the admin website.
