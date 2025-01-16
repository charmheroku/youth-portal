## 📖 Book Club Project – Browse, review, and discuss books.

**Interactive portal for teenage reading enthusiasts where they can:**
- Register (name, email, etc.).
- Manage personal profiles (user info, groups, messages).
- Build a book library (create, read, update, delete books, search/filter).
- Vote for books to read in a group setting.
- Split reading into sprints (chapters/sections).
- Leave reviews, share ideas, and comment.

**Main page**
![image](https://github.com/user-attachments/assets/0542d8e6-d011-4ed6-875d-f1ec106480a7)

**Login screen**
![image](https://github.com/user-attachments/assets/7d9e0fba-6d8f-48e1-a274-1f14bc5d4d90)

**Signup screen**
![image](https://github.com/user-attachments/assets/da75645b-f03d-4bc8-966a-56957337931b)

**User profile**
![image](https://github.com/user-attachments/assets/34d0a11a-7691-4cfa-8225-b4484844dd60)

**Books list**
![image](https://github.com/user-attachments/assets/89099781-6264-4d9b-b042-8cd3bb1380f8)

**Book detail**
![image](https://github.com/user-attachments/assets/89462206-9832-4e94-b7c1-d20222ffbc19)

**Reading groups list**
![image](https://github.com/user-attachments/assets/fc4e80bd-d6df-4627-939f-1202ccb57261)

**Reading group detail**
![image](https://github.com/user-attachments/assets/b8545545-9bf6-4a07-9154-42b8ba85f1df)

**Sprint detail**
![image](https://github.com/user-attachments/assets/18cf1ef7-5347-4365-ae68-5d9ba58f1952)

**Global search**
![image](https://github.com/user-attachments/assets/1758f5d3-225d-4295-bc65-b27445c8b384)


## Architecture & Core Modules


**DB architecture**
![books_club](https://github.com/user-attachments/assets/015d7bf9-f8eb-4311-96e7-7ec9a39bde2d)



1. **Custom User Model**  
   - Email-based login (roles: admin/user).  
   - Profile includes personal information, groups, messages.

2. **Library Module**  
   - CRUD operations for books (cover, description).
   - Search and filtering.
   - Reviews (comments), with editing rights only for admins.

3. **Book Voting Module**  
   - One like/vote per user per book.
   - Admin finalizes by marking a chosen book as “reading.”

4. **Reading Groups (ReadingGroup)**  
   - Automatically created when a book is marked as “reading.”
   - Users can join or leave the group.

5. **Sprints (ReadingSprint)**  
   - Break reading into stages (e.g., “Chapters 1–3”).
   - Only admins can create and edit sprints.

6. **Progress Tracker (SprintProgress)**  
   - Users can mark a sprint as “Read.”
   - (Optional) Check: ensure a user has shared at least one idea/review.

7. **Ideas & Discussions (SprintIdea, IdeaDiscussion)**  
   - Users share insights and comments.

8. **User Profile**  
   - Displays personal info, joined groups, messages, and shared ideas.

9. **Admin Panel**  
   - Manage books, groups, sprints, users.

10. **Future Plans**  
   - AI-powered idea analysis.
   - A habit-tracking module inspired by the books.

---



## 🚀 Technology Stack

- **Backend**: Django, SQLite  
- **Frontend (MVP)**: Django Templates with Bootstrap 
- **Git Flow**: Branches `main`, `develop`, use pull requests. 


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
