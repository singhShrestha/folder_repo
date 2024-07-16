_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X

### Admin
- Create Admin account using command
******************************************
py manage.py createsuperuser
******************************************
- Can also click on forgot password in case if the admin forgets his/her password.
- After Login, can see Total Number Of Student, Teacher, Course, Programme, Department, Assignments and tests are created on Dashboard.
- Can View, Update, Delete, Approve Teacher.
- Can View, Update, Delete, Approve Student.
- Can View, Update, Delete Programme, Course, Department.
- Can Also See Student Marks.
- Can Logout.
------------------------------------------------------------------------------------------------------------------------------------------------

### Teacher
-                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Register and then Login. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- After registration the teacher can login to see whether he/she is approved by the admin or not. If approved the teacher is directed to the dashboard. If rejected then the teacher is shown that he/she has been rejected. During the time until the admin approves the request and if the teacher tries to login with his/her details teacher is redirected to the waiting page.
- Can also click on forgot password in case if the teacher forgets his/her password.
- After Login, can see Exams created by him/her on Dashboard and clicking on the particular exam he/she is redirected to modify the particular exam and to view the result of the students who gave that exam.
- Can view his/her profile can update username and contact number can even reset password.
- Can Create, Modify, View, Delete Assignments and tests.
- Can view the list of students belonging to a particular program.
- Can Logout.
------------------------------------------------------------------------------------------------------------------------------------------------

### Student
-                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Register and then Login. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
- After registration the sudent can login to see whether she is approved by the admin or not. If approved the student is directed to the dashboard. If rejected then the student is shown that she is rejected. During the time until the admin approves the request and if the student tries to login with her details student is redirected to the waiting page.
- Can also click on forgot password in case if the student forgets her password.
- After Login can view all the Assignments assigned by which teacher and the time and date at which the test was assigned and can click on any test left to attempt.
- On clicking on any unattempted test opens up the page displaying the test details which include the programme and course for which the test has been created along with the CourseID , Test Duration in minutes , Total Test marks and the instructions for that particular exam.
- Can Give the test Any Time, can attempt the test only once after attempting the test disappears from the dashboard.
- Can attempt the test in a given amount of time as assigned by the teacher after the time limit is over the test is automatically submitted and the result is displayed.
- Can view her profile can update username and contact number can even reset password.
- Can view the detailed report of each attempted exam Question wise.
- Can View the result of each attempted test.
- -------------------[Question Pattern Is MCQ With 4 Options And 1 Correct Answer.]--------------------------
- Can Logout.
------------------------------------------------------------------------------------------------------------------------------------------------

## HOW TO RUN THIS PROJECT
- Install Python(3.7.6) (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :

pip install Django==3.0.5
pip install --user django-import_export
pip install passlib

- Move to project folder in Terminal. Then run following Commands :
~~~~~~~~~~~~~~~~ py manage.py makemigrations~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~ py manage.py migrate ~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~ py manage.py runserver ~~~~~~~~~~~~~~~~~~

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

- Now enter the following URL In Your Browser Installed On Your Pc
~~~~~~~~~~~~~~~[ http://127.0.0.1:8000/ ]~~~~~~~~~~~~~~~~~~~


_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X_X
