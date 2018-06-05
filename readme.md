## Handle Swachh toilets ##

### Prerequisites ###

    *  Python >= 3.6
    *  pipenv >= 11.10
    *  MongoDB >= 3.6

### Installation ###

    * run `git clone https://github.com/samayamnag/swachh-toilets.git <projectname>` to clone the repository
    * run `cd <projectname> && cd import_swachh_toilets`
    * run `cp .env.example .env`
    * configure .env
    * run `pipenv shell --python=3.6` to set up environment. --python argument is optional. This is to       specify specific python version 
    * run `pipenv install` to install dependencies

## Generate secret key ##

    * Before generating secret key, Django should be installed
    * run `pipenv shell --python=3.6` if environment not set up
    * run `python`
    ```python
      from django.utils.crypto import get_random_string


      chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
       print(get_random_string(50, chars))
    ```
    *  Assign generated value to `APP_SECRET_KEY` in .env

    - [For more info](https://gist.github.com/nagsamayam/8afe9ea59b6c8ed044211982ed6dcbd8)

## Import Swachh toilets from CSV  to MongoDB ##

    * run `pipenv run python manage.py import_toiles_from_csv chirala_toilet_locator_data.csv` to import toilets from CSV
