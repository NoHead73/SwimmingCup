# 🏊‍♂️ Armed Forces Cup of Russia – Swimming Competition Results Calculator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![PDF](https://img.shields.io/badge/PDF-ReportLab-red)

**A professional desktop application for calculating and ranking team results in swimming competitions.**

</div>

## 📋 About The Project

This application automates the scoring process for the **Armed Forces Cup of Russia swimming competition (men's events)**. It guides the user through inputting competition details, team names, and results, automatically calculates the sum of the **15 best scores out of 20** for each team, ranks them, and generates a polished, official PDF report.

### ✨ Key Features
- **✅ Step-by-Step Wizard**: Intuitive GUI built with Tkinter for easy data entry.
- **✅ Smart Scoring Logic**: Automatically sorts 20 scores and sums the top 15 for each team.
- **✅ Live Results Table**: Displays intermediate rankings while entering new teams.
- **✅ Professional PDF Export**: Generates well-formatted result sheets using ReportLab.
- **✅ Data Validation**: Ensures all inputs are correct before proceeding.
- **✅ Single Executable**: Packaged into a standalone `.exe` file for easy distribution on Windows.

## 🚀 Getting Started

### Prerequisites
*   **For running the app**: Just Windows.
*   **For development**: Python 3.8+ and `pip`.

### Installation & Run
**Option A: Using the Pre-built Executable (Recommended for Users)**
1.  Download the latest `SwimmingCupApp.exe` from the [Releases](../../releases) page.
2.  Run the file – no installation required.

**Option B: From Source (For Developers)**
```bash
# Clone the repository
git clone https://github.com/NoHead73/SwimmingCup.git
cd SwimmingCup

# Install dependencies
pip install -r requirements.txt

# Run the application
python swimming_cup_app.py
🖥️ Usage
The application follows a simple linear workflow:

Competition Info: Enter location, dates, venue, and pool length.

Team Count: Set the number of participating teams (1-100).

Team Names: Enter names for each team. See a live ranking after each entry.

Enter Scores: For each team, input 20 scores (0-999).

Final Results: View the final ranking table.

Export to PDF: Generate and save a professional results sheet.

🛠️ Built With (Tech Stack)
Python – The core programming language.

Tkinter – Standard GUI library for the user interface.

ReportLab – Powerful library for creating PDF documents.

PyInstaller – Used to package the Python script into a standalone .exe file.

📁 Project Structure
text
SwimmingCup/
├── swimming_cup_app.py    # Main application source code
├── build_exe.py           # Script to build the executable
├── requirements.txt       # Python dependencies (ReportLab, PyInstaller)
├── icon.ico              # Application icon
├── LICENSE               # MIT License
└── README.md             # This file
📄 License
Distributed under the MIT License. See the LICENSE file for details.

👨‍💻 Author
NoHead73

GitHub: @NoHead73

