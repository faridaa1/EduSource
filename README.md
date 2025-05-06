This supporting materials repository contains three folders:

* code - implementation code

* data gathering questionnaire - ethics approval document, consent form, participant information sheet

* deployment test data - test data that was used to deploy EduSource using OpenShift, and can replicate test conditions


The steps below outline how to run the code, where the use of a virtual environment is recommended:
1. Open the terminal
2. Ensure ports 8000 (backend) and 5173 (frontend) are free
3. Clone this GitHub repository using `git clone https://github.com/faridaa1/EduSource.git` or select Code -> Download ZIP and unzip the file
4. Enter the code directory: `cd code`
6. Run `pip install -r requirements.txt`
7. Run `python manage.py makemigrations`
8. Run `python manage.py migrate`
9. Run  `python manage.py update_rates`

If an error occurs related to torch installation, run Windows Powershell as admin and run `Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\FileSystem\' -Name LongPathsEnabled -Value 1`

8. Run `python manage.py runserver`
9. In an additional terminal, enter the code directory and run `cd frontend`
10. Run `npm install`
11. Run  `npm run dev`
12. On a browser of your choice, enter the URL `http://localhost:8000/signup/` to signup or `http://localhost:5173/` for the home page
