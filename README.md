# Quest Master 🏆

Quest Master is a gamified backend-driven system for achievement generation and validation. It leverages the power of the Django ORM to handle complex relationships between players and game objectives.

## 🚀 Technical Milestones
* **Complex Data Modeling**: Implemented Many-to-Many relationships between Users, Quests, and Rewards.
* **Identity Management**: Custom User Model implementation for extended player profiles.
* **Event-Driven Logic**: Django Signals for automatic achievement assignment and XP calculation.
* **Game Design Tooling**: Customized Admin Dashboard for Quest Building without code.
* **API Excellence**: Automated documentation with Swagger/OpenAPI.

## 🛠 Tech Stack
* **Backend**: Django 5.0 + Django REST Framework (DRF).
* **Frontend**: Vue.js 3 (Vite) + Tailwind CSS.
* **Database**: SQLite (Development).
* **Communication**: Axios for RESTful API consumption.

## 📦 Installation & Setup

1. **Backend**:
   ```bash
   python -m venv venv
   source venv/bin/activate # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
