# formulaq_challenge


This project is built as part of the FormulaQ Solutions Python Developer Evaluation.  
It includes:

✔ Google OAuth login (Phase 1)  
✔ Centered Rhombus Pattern Generator (Phase 2)  
✔ Current Indian Time display  
✔ Clean Flask UI with templates  

---

## 🚀 How to Run the Project

### 1️⃣ Create a virtual environment
```bash
python -m venv venv
```

### 2️⃣ Activate the environment  
Windows:
```bash
venv\Scripts\activate
```

### 3️⃣ Install the dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create a `.env` file  

Paste this into `.env`:

```
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
SECRET_KEY=your_secret_key_here
OAUTHLIB_INSECURE_TRANSPORT=1
```

Replace values with your own.

### 5️⃣ Run the application
```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

### Login Page

### Home Page (after Google Login)

### Pattern Output (Centered Rhombus)

---

## 📁 Project Structure

```
formulaq_challenge/
│── app.py
│── requirements.txt
│── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── home.html
│
└── screenshots/
    ├── login.png
    ├── home.png
    └── output.png
```


## ✔ Status  
This project is successfuly completed and ready for FormulaQ submission.
