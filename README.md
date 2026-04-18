# Privacy Checker Chrome Extension

The **Privacy Checker Chrome Extension** helps users analyze the privacy and security of websites in real-time. It evaluates cookies, trackers, permissions, and compliance with privacy laws (e.g., GDPR, CCPA). The extension provides a privacy score, compliance summary, and actionable tips to improve user awareness.

---

## 🛠️ Technologies Used

### Frontend:
- **HTML**: For the popup interface.
- **CSS**: For styling the popup and making it responsive.
- **JavaScript**: For dynamic interactions in the popup.

### Backend:
- **Python**: For server-side analysis.
- **Flask**: For creating the backend API.
- **Flask-CORS**: For enabling cross-origin requests.
- **BeautifulSoup**: For parsing and analyzing website HTML.
- **Requests**: For fetching website content.
- **TextStat**: For analyzing text (optional for advanced features).

### Chrome Extension:
- **Manifest V3**: For defining the extension's structure.
- **Service Worker**: For background tasks.

---

## 📂 Folder Structure

```
PrivacyChecker_Extension/
├── popup.html         # Popup interface
├── popup.js           # JavaScript for popup functionality
├── style.css          # Styling for the popup
├── manifest.json      # Chrome extension configuration
├── background.js      # Background script for handling events
├── app.py             # Backend logic for analyzing websites
├── flask_server.py    # Flask server for API endpoints
├── icon.png           # Default icon for the extension
```

---

## 🚀 How to Use

### Step 1: Install Python Dependencies
Ensure you have Python 3 installed. Then, install the required libraries:

```bash
pip install flask flask-cors requests beautifulsoup4 textstat
```

---

### Step 2: Start the Flask Server
Run the backend server to handle website analysis:

```bash
python flask_server.py
```

The server will run at `http://localhost:5000/analyze`.

---

### Step 3: Load the Chrome Extension
1. Open Chrome and navigate to: `chrome://extensions`.
2. Enable **Developer Mode** (toggle in the top-right corner).
3. Click **Load unpacked**.
4. Select the `PrivacyChecker_Extension/` folder.

---

### Step 4: Use the Extension
1. Visit any website in Chrome.
2. Click the **Privacy Checker** extension icon in the toolbar.
3. Click **Scan Current Site**.
4. View the results:
   - **Privacy Score**: A score out of 100.
   - **Breakdown**: Details about cookies, trackers, permissions, and security headers.
   - **Compliance Summary**: GDPR, CCPA compliance status.
   - **Tips**: Suggestions to improve privacy awareness.

---

## 🖥️ How to Use on Different Operating Systems

### Windows:
1. Install Python from [python.org](https://www.python.org/).
2. Open Command Prompt and navigate to the project folder.
3. Run the Flask server using `python flask_server.py`.
4. Load the extension in Chrome as described above.

### macOS:
1. Install Python using Homebrew:
   ```bash
   brew install python
   ```
2. Open Terminal and navigate to the project folder.
3. Run the Flask server using `python3 flask_server.py`.
4. Load the extension in Chrome as described above.

### Linux:
1. Install Python using your package manager (e.g., `apt` for Ubuntu):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
2. Open Terminal and navigate to the project folder.
3. Run the Flask server using `python3 flask_server.py`.
4. Load the extension in Chrome as described above.

---

## 🔍 Features

### Privacy Analysis:
- **Privacy Score**: Rates the website's privacy on a scale of 0–100.
- **Permissions**: Detects if the website requests camera, microphone, or other permissions.
- **Cookies**: Lists the cookies set by the website.
- **Trackers**: Identifies common trackers (e.g., Google Analytics, Facebook Pixel).
- **Security Headers**: Checks for headers like `Content-Security-Policy`, `Strict-Transport-Security`.

### Compliance Checks:
- **GDPR**: Checks for cookie consent banners.
- **CCPA**: Evaluates compliance with California privacy laws.

### User-Friendly Interface:
- **Dynamic Results**: Displays results in real-time.
- **Tips**: Provides actionable suggestions to improve privacy awareness.

---

## 🔧 File Descriptions

### Frontend:
- **popup.html**: The main interface for the extension.
- **popup.js**: Handles user interactions and fetches data from the backend.
- **style.css**: Styles the popup interface.

### Backend:
- **app.py**: Contains the logic for analyzing websites (e.g., detecting trackers, permissions).
- **flask_server.py**: Runs the Flask server and handles API requests.

### Chrome Extension:
- **manifest.json**: Defines the extension's structure and permissions.
- **background.js**: Handles background tasks like listening for messages.

---

## 🛡️ Security Notes

- **No Data Collection**: This tool does not collect or share user data.
- **Local Analysis**: All analysis is performed locally or on the user's machine.
- **Educational Use**: Designed for ethical auditing and educational purposes only.

---

## 🌐 Hosting the Backend on a Server

To make the extension publicly accessible:
1. Deploy the Flask server to a cloud platform (e.g., AWS, Heroku, or Google Cloud).
2. Update the `popup.js` file to point to the hosted server URL instead of `http://localhost:5000`.

---

## 🛠️ Customization

1. **Add More Trackers**:
   - Edit the `detect_trackers` function in `app.py` to include additional tracker domains.

2. **Change the Privacy Score Algorithm**:
   - Modify the `calculate_privacy_score` function in `app.py` to adjust scoring logic.

3. **Add More Compliance Checks**:
   - Expand the `check_compliance` function in `app.py` to include other privacy laws.

---

## 🧩 Troubleshooting

### Common Issues:
1. **Flask Server Not Running**:
   - Ensure Python dependencies are installed.
   - Check for errors in `flask_server.py`.

2. **Extension Not Loading**:
   - Verify the `manifest.json` file is correctly configured.
   - Ensure all required files (e.g., `popup.html`, `popup.js`) are present.

3. **CORS Errors**:
   - Ensure `Flask-CORS` is installed and enabled in `flask_server.py`.

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it for educational and ethical purposes.

---

## 💬 Feedback

If you encounter any issues or have suggestions, feel free to open an issue or contribute to the project.

---

## 👏 Credits

This project was developed with contributions and guidance from **Alok Dhetal Sharma**.  
GitHub: [hyperbro76](https://github.com/hyperbro76)

---

## © Copyright

**Privacy Checker Chrome Extension**  
Copyright © 2025  
Developed by **Alok Dhetal Sharma** and contributors.  
All rights reserved.
