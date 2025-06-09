# Social Media Backend (Django + DRF)

This project is a full-featured social media platform built using **Django** and **Django REST Framework (DRF)**.  
It offers functionalities such as:
- User registration & authentication (JWT)
- Profile management
- Posting content, commenting, and liking posts
- Follow/Unfollow functionality
- Real-time **one-to-one** and **group chat** features

> **Note:** Live Admin Panel hosted — (link not shared publicly)

### 🔗 Links:
- **GitHub Repository:** [https://github.com/Choudhary-jii/social-media](https://github.com/Choudhary-jii/social-media)
- **Postman Documentation:** [https://documenter.getpostman.com/view/39033838/2sB2qfBfHH](https://documenter.getpostman.com/view/39033838/2sB2qfBfHH)

---

## 🚀 Features

### 👤 User Management:
- **Registration:** Users can register by providing necessary details.
- **Authentication:** JWT-based authentication using `TokenObtainPairView` and `TokenRefreshView`.

### 🙍‍♂️ Profile Management:
- **Retrieve Profile:** Fetch user details using their UUID.
- **Update Profile:** Authenticated users can update their profile information.
- **Delete Profile:** Authenticated users can delete their profile.

### ➕ Follow / Unfollow:
- **Follow User:** Authenticated users can follow others.
- **Unfollow User:** Authenticated users can unfollow others.
- **List Followers:** Get followers of a specific user.
- **List Following:** Get list of users followed by a specific user.

---

### 📝 Posts:
- **Create Post:** Authenticated users can create new posts.
- **Retrieve Posts:**
  - Admins can view all posts.
  - Regular users can view their own posts.
- **Retrieve Specific Post:** Fetch post by ID.
- **Update/Delete Post:** Authenticated users can update or delete their own posts.
- **Like/Unlike Post:** Toggle like status.

---

### 💬 Comments:
- **Create Comment:** Authenticated users can comment on posts.
- **Retrieve Comments:**
  - View all comments.
  - Fetch a specific comment by ID.
- **Update/Delete Comment:** Authenticated users can manage their own comments.

---

### 💬 Chat & Group Chat:
- **Private Chat:** Real-time messaging between two users.

#### Group Chat:
- **Create Group**
- **Add/Remove Members**
- **Send Messages**
- **List Messages**

---


## 🧰 Technologies Used

| Area                  | Technology                                    |
|-----------------------|-----------------------------------------------|
| **Backend**           | [Django](https://www.djangoproject.com/), [Django REST Framework](https://www.django-rest-framework.org/) |
| **Authentication**    | [JWT](https://jwt.io/) via `djangorestframework-simplejwt` |
| **Database**          | SQLite (default) – Easily swappable with PostgreSQL or MySQL |
| **Real-time Chat**    | Implemented using custom models for one-on-one and group messaging |
| **API Documentation** | [Postman](https://www.postman.com/) |


---

## ⚙️ Setup & Installation

### 🔁 Clone the Repository:
```bash
git clone https://github.com/Choudhary-jii/social-media.git
cd social-media



### ➕ Create a Virtual Environment:
- **python -m venv venv**
- **source venv/bin/activate**

---


### Install Dependencies:
- pip install -r requirements.txt


---

### Apply Migrations:
-python manage.py migrate

---

### Run the Development Server:
-python manage.py runserver

---
