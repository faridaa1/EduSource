This supporting materials repository contains three folders:

* code - implementation code

* data gathering questionnaire - ethics approval document, consent form, participant information sheet

* deployment test data - test data that was used to deploy EduSource using OpenShift, and can replicate test conditions


The steps below outline how to run the code:
1. Ensure ports 8000 (backend) and 5173 (frontend) are free
2. Enter the code directory: `cd code`
3. Run `pip install -r requirements.txt `
4. Run  `python manage.py update_rates`
5. Run `python manage.py runserver `
6. Within the code directory, enter the frontend directory: `cd frontend`
7. Run `npm install`
8. Run  `npm run dev`
9. On a browser of your choice, enter the URL `http://localhost:8000/signup/` to signup or `http://localhost:5173/` for the home page
