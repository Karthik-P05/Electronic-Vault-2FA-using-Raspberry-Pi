# 🔐 Electronic Vault with Two-Factor Authentication (2FA) using Raspberry Pi

This project implements a secure **Electronic Vault** that uses **biometric-based two-factor authentication** for access control. It combines **fingerprint recognition** and **facial recognition** to ensure that only authorized users can access the system.

---

## 🚀 Features

- ✅ **Fingerprint Recognition** using `pyfingerprint`
- ✅ **Facial Recognition** using `face_recognition` and OpenCV
- ✅ **Two-Factor Authentication** for enhanced security
- ✅ **User Enrollment, Authentication, and Deletion**
- ✅ **Data Storage in MySQL Database**
- ✅ Runs on **Raspberry Pi** with camera and fingerprint sensor

---

## 🛠️ Tech Stack

| Component          | Technology Used                             |
|-------------------|----------------------------------------------|
| Hardware           | Raspberry Pi, Fingerprint Sensor, Pi Camera |
| Fingerprint        | PyFingerprint                               |
| Facial Recognition | face_recognition, OpenCV                    |
| Database           | MySQL (`pymysql`)                           |
| Image Processing   | imutils, OpenCV                             |
| Language           | Python                                      |

---

## 📁 Project Structure

├── enroll_data.py # Registers new user (fingerprint + face)
├── authentication.py # Authenticates using 2FA (fingerprint + face)
├── delete_data.py # Deletes biometric and database records
├── encodings.pickle # Stores facial encodings
├── dataset/ # Contains facial image folders by user ID


---

## 🧪 How It Works

1. **Enroll User**
   - Captures fingerprint and facial images
   - Stores fingerprint hash and facial encodings in MySQL

2. **Authenticate**
   - Scans fingerprint → Matches in DB
   - Loads corresponding face encoding → Compares with live webcam feed
   - Access granted only if both match

3. **Delete User**
   - Deletes fingerprint template from sensor
   - Deletes face image folder and database record

---

## ⚙️ Setup Instructions

### Prerequisites

- Raspberry Pi (with Raspbian OS)
- Fingerprint Sensor (e.g., R305)
- Pi Camera or USB Webcam
- MySQL Server
- Python 3 with required libraries

### Install Required Libraries

```bash
  pip install pyfingerprint pymysql opencv-python face_recognition imutils
```

## Database Setup
```bash
CREATE DATABASE authentication;
USE authentication;

CREATE TABLE data11 (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    fing_encod TEXT,
    temp_pos INT,
    img_encod LONGBLOB
);
```

## 📸 Sample Output
```bash
Waiting for finger...
Fingerprint found for ID : 101
Name : Karthik
Access granted
```

## 🧠 Future Enhancements

- GUI interface for enrollment and authentication

- Add voice recognition as an additional factor

- Real-time cloud backup of biometric logs

- Logging system for access events

## 👨‍💻 Author
Karthik P
📧 [karthikp0511@gmail.com]
