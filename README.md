# Youth Portal 🛠️✨
A web platform for Ukrainian youth groups to discuss, manage events, and grow. Built with Django & best development practices.

## 📌 Features
- 📖 **Book Library** – Browse, review, and discuss books.
- 📜 **Study & Discussions** – Share insights.
- 🎉 **Event Management** – Organize and register for activities.
- 🤝 **Mentorship & Challenges** – Tasks and growth tracking.

## 🚀 Tech Stack
- **Backend**: Django, PostgreSQL
- **Frontend**: Django Templates

## 🔧 Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/charmheroku/youth-portal.git
   cd youth-portal
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```