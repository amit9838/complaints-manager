#!/bin/bash

# Set the virtual environment directory
VENV_DIR="PYTHON_ENV"

# Activate the virtual environment based on the operating system
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  # Windows
  source "$VENV_DIR/Scripts/activate"
  echo "Environment activated"

else
  # Linux/Mac
  source "$VENV_DIR/bin/activate"
  echo "Environment activated"
fi

# Variable to store IP addresses
ip_address=""

# Function to get IP addresses on Linux
get_ip_linux() {
  ip_address=$(ip addr | awk '/inet / {print $2}' | cut -f1 -d'/' | sed -n '2p')
}

# Function to get IP addresses on Windows
get_ip_windows() {
  ip_address=$(ipconfig | awk '/IPv4 Address/ {print $NF}')
}

# Check the operating system and call the appropriate function
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
  # Linux
  get_ip_linux
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
  # Windows
  echo "Win"
  get_ip_windows
else
  echo "Unsupported operating system."
  exit 1
fi

# Print the IP addresses
echo "Network ip addresses:"
echo $ip_address

# Run the project
python manage.py runserver "$ip_address:8000"