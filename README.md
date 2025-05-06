This supporting materials repository contains three folders:

* code - implementation code

* data gathering questionnaire - ethics approval document, consent form, participant information sheet

* deployment test data - test data that was used to deploy EduSource using OpenShift, and can replicate test conditions

There is no executable file because EduSource is a web application. However, the frontend and backend can be configured as described below, allowing EduSource to be run on a browser.

The steps below outline how to run the code, where the use of a virtual environment is recommended:
1. Open the terminal
2. Ensure ports 8000 (backend) and 5173 (frontend) are free
3. Clone this GitHub repository using `git clone https://github.com/faridaa1/EduSource.git` or select Code -> Download ZIP and unzip the file
4. Once inside the root folder, enter the code directory: `cd code`
5. Run `pip install -r requirements.txt`
6. Run `python manage.py makemigrations`
7. Run `python manage.py migrate`
8. Run  `python manage.py update_rates`

If an error occurs related to torch installation, run Windows Powershell as admin and run `Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\FileSystem\' -Name LongPathsEnabled -Value 1`

9. Run `python manage.py runserver`
10. In an additional terminal, enter the code directory and run `cd frontend`
11. Run `npm install`
12. Run  `npm run dev`
13. On a browser of your choice, enter the URL `http://localhost:8000/signup/` to signup or `http://localhost:5173/` for the home page
