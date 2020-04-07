from geosound.models import User
from geosound.models import Location
from geosound.models import City


# returns a valid city_id if the city passes, -1 if no valid city is found
def validate_location(city, state, zip_code):
    city_matches = list(City.objects.filter(city_state=state, city_name=city, city_zips__contains=zip_code))

    if len(city_matches) == 1:
        city_obj = city_matches[0]
        return city_obj.city_id
    else:
        return -1


# creates a new user object from the information provided, returns its user_id
def create_user(email, password, fname, lname, street, addr_num, zip_code, city_num):
    city_obj = City.objects.get(city_id=city_num)
    loc_obj = Location(loc_addr_num=addr_num, loc_zip=zip_code, loc_street=street, city=city_obj)
    loc_obj.save()
    new_user = User(user_email=email, user_password=password, user_fname=fname, user_lname=lname, loc=loc_obj)
    new_user.save()
    return new_user.user_id


def validate_user(email, password):
    user_matches = list(User.objects.filter(user_email=email, user_password=password))

    if len(user_matches) == 1:
        user_obj = user_matches[0]
        return user_obj.user_id
    else:
        return -1



