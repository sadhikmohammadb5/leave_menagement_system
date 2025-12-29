 Leave Management System

A web-based Leave Management System developed using Flask (Python) that allows employees to apply for leave and administrators to manage, approve, or reject leave requests through a secure and user-friendly interface.

---

##  Features

###  Employee:
- Register and login securely
- Apply for leave
- View leave status and leave history
- Check remaining leave balance

###  Admin:
- Secure admin login
- View all employee leave requests
- Approve or reject leave applications
- Create new admin accounts
- Role-based access control

---

##  Tech Stack:

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, Bootstrap, Jinja Templates  
- **Database:** SQLite  
- **Authentication:** Flask Sessions  

---

## Project Structure:

```
leave-management-system/
│── app.py
│── database.db
│── requirements.txt
│── README.md
│── .gitignore
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── apply_leave.html
│ ├── employee_dashboard.html
│ ├── admin_dashboard.html
│ ├── create_admin.html
│ └── access_denied.html
│
└── static/
└── css/
```



## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash

git clone https://github.com/sadhikmohammadb5/leave_menagement_system.git
```



2️⃣ Install Dependencies
```bash
pip install flask
```
3️⃣ Run the Application:
```bash
python app.py
```
4️⃣ Initialize Admin Account:
```bash

Open the following URL once in your browser:

http://127.0.0.1:5000/

```


Default Admin Credentials:

Username: admin
Password: admin_password

 Role-Based Access Control

Admins can manage leave requests and create new admin users

Employees can apply for leave and view their leave history

Unauthorized users are redirected or shown access-denied messages

Use Case:

This project is suitable for:

College mini / major projects,

Learning Flask & role-based authentication,

HR management system demonstrations,

Web development practice

Future Enhancements:

Password hashing,

Email notifications,

Monthly leave limits,

File upload for medical documents,

Deployment on cloud platforms

License:

This project is developed for educational purposes.

👨‍💻 Author

Sadhik mohammad
Computer Science Student

 Technologies Used:

Backend: Python, Flask

Frontend: HTML, CSS, Bootstrap, Jinja Templates

Database: SQLite

Authentication: Flask Sessions

 Advantages:

Time-efficient and paperless system,

Easy to use and maintain,

Secure and scalable,

Improves transparency in leave management

Conclusion:

The Leave Management System provides a reliable and efficient solution for managing employee leave requests in an organization. By using modern web technologies and a user-friendly interface, the system enhances productivity, improves administrative efficiency, and ensures a structured leave approval process.