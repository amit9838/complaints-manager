#!/bin/bash

# Get the path of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the project directory as the current directory
PROJECT_DIR="$SCRIPT_DIR"

# Set the virtual environment directory
VENV_DIR="PYTHON_ENV"

# Create a virtual environment
echo "Creating environment"
python -m venv "$VENV_DIR"
echo "Successfull"

# Activate the virtual environment based on the operating system
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  # Windows
  echo "Windows detected"
  source "$VENV_DIR/Scripts/activate"
  echo "Environment activated"

else
  # Linux/Mac
  echo "Unix Based system detected"
  source "$VENV_DIR/bin/activate"
  echo "Environment activated"
fi

# Install requirements
echo "Installing required packages"
pip install -r requirements.txt

# Run database migrations (if needed)
echo "Running migrations\n"
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
echo ""
echo "You are set-up, Thanks for using Complaints-Manager"
echo ""
echo "Now run RUN.sh to start."
