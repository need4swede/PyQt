# Aeries2Google

Aeries2Google is a PyQt-based GUI application that processes student report exports from Aeries, an online student information system, and generates CSV files suitable for bulk uploads to Google Workspace or Google Classroom.

## Features

- GUI-based drag and drop functionality for easy file handling
- Processes Aeries student report exports
- Generates CSV files suitable for bulk uploads to Google Workspace or Google Classroom
- Customizable themes
- Built-in file browser

## Installation & Usage

Aeries2Google requires Python and a few dependencies to run.

### Dependencies:

- n4s
- openpyxl
- PyQt6

You can install these packages using pip:

```sh
pip install n4s openpyxl PyQt6
```

### Running the Application:

To run the application, navigate to the directory where `main.py` is located and use the following command:

```sh
python main.py
```

A GUI will appear, allowing you to drag and drop the Aeries student report export file into the application. The application will then process the file and generate a CSV suitable for bulk uploads to Google Workspace or Google Classroom.

## License

This project is licensed under the terms of the MIT license.
