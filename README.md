 Duolingo Tracker Backend  
![GitHub Repo Stars](https://img.shields.io/github/stars/bryankurtzdev/duolingo-tracker-backend?style=social)  
![GitHub License](https://img.shields.io/github/license/bryankurtzdev/duolingo-tracker-backend)  
![GitHub Last Commit](https://img.shields.io/github/last-commit/bryankurtzdev/duolingo-tracker-backend)  
![Flask](https://img.shields.io/badge/Made%20with-Flask-blue)  

📊 A **Flask API** that fetches Duolingo users' total XP and generates Excel reports.  

## 🔗 Backend URL  
🚀 **Live API on Render:** [Duolingo Tracker Backend](https://duolingo-tracker-backend.onrender.com)  

## 📂 Project Structure  
/duolingo-tracker-backend │── app.py # Main Flask server code │── requirements.txt # Dependencies │── /static # Static files (if needed) │── duolingo_xp.xlsx # Generated report file

## ⚙️ How to Run Locally  
1. **Clone the repository:**  
   ```sh
   git clone https://github.com/bryankurtzdev/duolingo-tracker-backend.git

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt

3. **Run the server:**
   ```sh
   python app.py

4. **The backend will be available at http://127.0.0.1:5000/.**

## 📡 Available Endpoints
| Method  | Endpoint | Description |
| ------- | -------- | ----------- |
| GET  | / | Home page  |
| POST  | /processar  | Receives user data, fetches XP, and generates a report |
| GET  | /download  | Downloads the generated report  |

## 🛠️ Technologies Used
- ✅ Python (Flask)
- ✅ Pandas (Data Processing)
- ✅ Requests (Duolingo API Requests)
- ✅ Render (Cloud Hosting)

## 📜 License
This project is licensed under the **MIT License.**
