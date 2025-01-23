# Learning Management System (LMS)

## Overview
This is a comprehensive Learning Management System (LMS) built using **FastAPI** for the backend, **React.js** for the frontend, and **MySQL** as the database. The system supports four types of users: **Students**, **Teachers**, **Parents**, and **Admins**, each with their own dedicated portal and features. 

---

## Features

### **Student Portal**
- **Profile**: View student details.
- **Dashboard**:
  - View all purchased courses.
  - Access attendance records (view only).
  - View announcements created by the Admin.
- **Course Assessment**: Access lesson-wise assessments for purchased courses.

---

### **Teacher Portal**
- **Profile**: Manage teacher details.
- **Course Management**:
  - Add, view, and delete course content (for courses assigned by the Admin).
- **Attendance Management**:
  - Mark attendance for students.
- **Test Management**:
  - Create lesson-wise test papers.
  - View and manage test results.
- **Announcements**:
  - Create announcements for assigned courses.

---

### **Admin Portal**
- **Dashboard**:
  - View details of all users (students, teachers, and parents).
  - View all enrolled students and teachers.
- **Content Management**:
  - Manage demo videos.
  - Handle queries and admission information.
  - Manage fees details.
  - Create and manage announcements.
  - Manage branch and course details.
- **Payment Management**:
  - View and manage payment details.

---

### **Parent Portal**
- View their child’s profile and performance.
- View announcements and updates.

---

## Technology Stack
### **Backend**
- **Framework**: FastAPI
- **Database**: MySQL

### **Frontend**
- **Library**: React.js
- **Styling**: Tailwind CSS

---

## Installation Instructions

### **Backend**
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   - Create a MySQL database.
   - Update the database connection string in the `settings.py` or `.env` file.
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
5. Access the API docs at `http://localhost:8000/docs`.

### **Frontend**
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Access the application at `http://localhost:3000`.

---

## Database Structure
### **Tables**
- **Users**: Stores details of students, teachers, parents, and admins.
- **Courses**: Stores course details.
- **Enrollments**: Tracks course purchases by students.
- **Attendance**: Tracks attendance records.
- **Announcements**: Stores announcements created by the admin or teacher.
- **Tests**: Stores test papers and results.
- **Payments**: Manages payment details.

---

## API Endpoints
### **Student APIs**
- Get student profile
- Fetch purchased courses
- Fetch attendance records

### **Teacher APIs**
- Add, view, and delete course content
- Mark attendance
- Create test papers
- Fetch test results

### **Admin APIs**
- Manage user details
- Manage courses
- Handle payments
- Create announcements

---

## Future Enhancements
- Integration with third-party video conferencing tools.
- Enhanced reporting and analytics.
- Mobile app support.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author
- ** 9004173181 **
- Vinay Kumar

