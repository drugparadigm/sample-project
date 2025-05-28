set -e

# Change the packages to your requirement

# Add the packages that are difficult to install from the conda environment

# Do not remove flask

echo "Installing Flask..."
pip install flask

echo "Installing gunicorn..."
pip install gunicorn

# Add packages like torch, torch-scatter, etc., that are installed using direct links or wheels
# Remove them from environment.yml if they are already included there