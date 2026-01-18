FinShield – Backend (README.md)
📌 Project Overview

FinShield is an AI-powered fraud detection system designed to identify suspicious financial transactions in real time using behavioral biometrics, risk scoring, and tampering detection.

The backend handles secure authentication, transaction analysis, fraud risk calculation, and decision-making.

🚀 Key Features

Secure authentication (JWT + password hashing)

Behavioral fraud detection (typing speed, click intervals, hesitation time)

Bot & script detection

Transaction risk scoring (0–100)

Data tampering detection (hash verification)

Rule-based + configurable risk engine

Scalable API architecture

🧠 Fraud Detection Parameters

Typing speed (WPM / WPS)

Key press interval (variance-based)

Mouse / click interval

Hesitation before submit

Error rate (backspaces, corrections)

Transaction context (amount, merchant, frequency)

🏗️ Tech Stack

Backend: Node.js / Express (or Python FastAPI if applicable)

Authentication: JWT

Security: bcrypt

Database: MongoDB (or any NoSQL/SQL)

API: REST

⚙️ Installation & Setup
git clone https://github.com/<username>/finshield-backend.git
cd finshield-backend
npm install
npm run dev


Backend runs on:

http://localhost:5000

🔐 Security Measures

Password hashing using bcrypt

Token-based authentication (JWT)

Server-side fraud scoring

Rate limiting for bot protection

Integrity checks for tampering detection

📈 Future Enhancements

Camera-based identity verification

AI-powered face matching

Device fingerprinting

ML-based anomaly detection

👨‍💻 Team

Built as a hackathon project to demonstrate secure and scalable fintech solutions.