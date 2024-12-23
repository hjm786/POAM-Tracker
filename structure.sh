#!/bin/bash

# Create main files in the current directory
touch app.py
touch models.py
touch views.py
touch wsgi.py
touch requirements.txt
touch README.md

# Create templates directory structure
mkdir -p templates/fragments
touch templates/base.html
touch templates/dashboard.html
touch templates/scan_results.html
touch templates/poam_manager.html
touch templates/fragments/scan_dropdown.html
touch templates/fragments/scan_table.html
touch templates/fragments/poam_table.html

# Create static directory structure
mkdir -p static/css
mkdir -p static/js
touch static/css/styles.css
touch static/js/scripts.js

echo "Project structure created successfully in the current directory."
