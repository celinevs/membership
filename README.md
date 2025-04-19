# 🧾 Membership App

A simple Flask-based membership management system that allows users to register, record attendance, and handle membership fee payments automatically based on attendance milestones.

---

## 📌 Features

- 📝 Member Registration  
- 🕒 Attendance Check-in (with 2-minute cooldown)  
- 💰 Automatic Fee Calculation (every 5 attendances)  
- ✅ Payment Confirmation  
- 📋 View Members, Attendance, and Payments  

---

## ⚙️ Tech Stack

- Python 3.x  
- Flask  
- Flask-SQLAlchemy  
- SQLite (default) or MySQL (for deployment)  
- HTML / Jinja2 Templates  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/membership.git
cd membership
```
### 2. Create a Virtual Environment (optional but recommended) and Install Required Dependencies

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Run the App and Copy Paste the link

```bash
python app.py
```

## 📝 Notes
- ⏱ Members cannot check-in again within 2 minutes of their last attendance.
- 🎯 After every 5 attendances, a payment is triggered automatically:
  - Bus Membership → Rp100,000
  - Others (e.g., train) → Rp50,000
- ✅ Payment status updates can be made through /payment_confirm/<id>.

## 👤 Author
Made with ❤️ by **Celine Vania Setiadi**, **Joanna Gracia Tan**, **Brygitta Josephine Makarawung**  
GitHub: 
- Celine: [@celinevs](https://github.com/celinevs)
- Joanna: [@joanna00329](https://github.com/joanna00329)
- Brygitta: [@brygittajosefien](https://github.com/brygittaa)


