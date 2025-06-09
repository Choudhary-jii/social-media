Overview

This project is a full-featured social media platform built using Django and Django REST Framework (DRF). It offers functionalities such as user registration (multiple users), authentication, profile management, posting content, commenting, liking posts, following/unfollowing users, and real-time chat features including one-one and group chats as well.

Live Admin Panel: (not sharing the link here!)

GitHub Repository: https://github.com/Choudhary-jii/social-media

Postman Documentation: https://documenter.getpostman.com/view/39033838/2sB2qfBfHH

-----------------------------------------------------------------------------------------------

Features 

User Management : 

Registration: Users can register by providing necessary details.

Authentication: JWT-based authentication using TokenObtainPairView and TokenRefreshView.

Profile Management:

Retrieve Profile: Fetch user details using their UUID.
Update Profile: Authenticated users can update their profile information.
Delete Profile: Authenticated users can delete their profile.

Follow/Unfollow:

Follow User: Authenticated users can follow other users.
Unfollow User: Authenticated users can unfollow other users.
List Followers: Retrieve a list of followers for a specific user.
List Following: Retrieve a list of users that a specific user is following.

Posts :

Create Post: Authenticated users can create new posts.

Retrieve Posts:

List Posts: Admins can view all posts; Regular users can view their own posts.
Retrieve Specific Post: Fetch details of a specific post using its ID.

Update/Delete Post: Authenticated users can update or delete their own posts.

Like/Unlike Post: Toggle like status on a post.

Comments :

Create Comment: Authenticated users can comment on posts.

Retrieve Comments:

List Comments: View all comments.
Retrieve Specific Comment: Fetch details of a specific comment using its ID.

Update/Delete Comment: Authenticated users can update or delete their own comments.

Chat & Group Chat :

Private Chat: Real-time messaging between two users.

Group Chat:

Create Group: Users can create chat groups.
Add/Remove Members: Manage group members.
Send Messages: Send messages within a group.
List Messages: Retrieve all messages from a group.

-----------------------------------------------------------------------------------------------

Setup & Installation

Clone the Repository:

git clone https://github.com/Choudhary-jii/social-media.git
cd social-media

Create a Virtual Environment:

python -m venv venv
source venv/bin/activate

Install Dependencies:

pip install -r requirements.txt

Apply Migrations:

python manage.py migrate

Run the Development Server:

python manage.py runserver

-----------------------------------------------------------------------------------------------

Technologies Used

Backend: Django, Django REST Framework

Authentication: JWT (JSON Web Tokens) via djangorestframework-simplejwt

Database: SQLite (default, can be changed to PostgreSQL/MySQL)

Real-time Communication: A Separate Model (Tables)

API Documentation: Postman

-----------------------------------------------------------------------------------------------

NOTE 

User Management In Postman Documentation : Update the base URL from LocalHost to 'https://socialmediacodenicely.pythonanywhere.com'.
