🔐 Secure Vault

Secure Vault is a secure file storage system built with Django that encrypts uploaded files using a custom-designed 256‑bit block cipher implemented in C. The project focuses on understanding cryptographic design, key derivation, and system integration, rather than relying solely on standard libraries.

> ⚠️ Educational Project: This project is intended for academic and learning purposes. Some cryptographic choices (e.g., ECB mode) are not recommended for real‑world production systems.




---

✨ Features

🔑 User Authentication (Register & Login)

📁 Secure File Upload & Download

🔐 Custom 256‑bit Block Cipher (MULTISBOX) implemented in C

🧂 Password‑based Key Derivation using SHA‑256

⚙️ Django ↔ C integration via shared library (DLL)

🗄️ Encrypted file storage on the server



---

🧠 Cryptographic Design Overview

🔒 Cipher

Block size: 256 bits

Structure: MULTISBOX‑based substitution design

Mode of operation: ECB (Electronic Codebook)


🔑 Key Derivation

User password is hashed using SHA‑256

Resulting 32‑byte hash is used directly as the encryption key


User Password → SHA‑256 → 256‑bit Key → Block Cipher

> ℹ️ In future versions, a dedicated KDF such as PBKDF2, bcrypt, or Argon2 is recommended.




---

🛠️ Tech Stack

Backend: Django (Python)

Cryptography Core: C (compiled as DLL)

Database: PostgreSQL / SQLite (configurable)

Frontend: HTML, CSS



---

📂 Project Structure

Secure-Vault/
│
├── secureVault/        # Django project settings
├── vault/              # Main Django app
│   ├── aes.dll         # Compiled encryption library
│   ├── encryption.py   # Python ↔ C interface
│   ├── models.py
│   ├── views.py
│   └── templates/
├── media/              # Encrypted uploaded files
├── manage.py
└── README.md


---

🚀 Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/pushkar192003/Secure-Vault.git
cd Secure-Vault

2️⃣ Create virtual environment

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Run migrations

python manage.py makemigrations
python manage.py migrate

5️⃣ Start the server

python manage.py runserver


---

🧪 Example Workflow

1. User registers and logs in


2. Uploads a file


3. File is encrypted using the custom C cipher


4. Encrypted file is stored on the server


5. On download, file is decrypted using the same password‑derived key




---

🔐 Security Notes

ECB mode does not hide data patterns — it is insecure for production

No salting or iteration is used in key derivation

Intended strictly for learning and experimentation


Planned Improvements

Replace ECB with CBC or GCM

Introduce PBKDF2 / Argon2 for key derivation

Add file integrity checks (HMAC)

Add unit tests for cipher correctness



---

📌 Motivation

This project was built to:

Understand how block ciphers work internally

Learn low‑level cryptography implementation

Explore Django–C integration

Bridge theory from cryptography courses with real systems



---

👤 Author

Pushkar
B.Tech CSE Student | Cryptography Enthusiast
GitHub: https://github.com/pushkar192003


---

📜 License

This project is released for educational use only.
