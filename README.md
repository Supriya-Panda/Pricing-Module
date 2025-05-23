# Pricing-Module

# Run the applications
cd Pricing-Module

1. Set Up Virtual Environment
python3 -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows

3. Install Dependencies
pip install django djangorestframework django-multiselectfield

4.  Inside Application folder ;already  Migrations done
cd pricing_module

5. Superuser credentials
  id :- admin
  password:- supriya@123

6. Run the Development Server
python3 manage.py runserver
Now visit: http://127.0.0.1:8000/admin/ to log in to the Django admin.
and for price calculation; http://127.0.0.1:8000/api/calculate-price/ 


request payload :-
{
  "distance_km": 5.5,
  "total_minutes": 75,
  "waiting_minutes": 6,
  "day_of_week": "Wednesday"
}


