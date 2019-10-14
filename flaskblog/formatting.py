from flaskblog import db
from flaskblog.models import *

def parse_value(value):
    str_value = str(value)[::-1]
    len_str_value = len(str_value)
    more_than_thousand = (len_str_value > 3)
    parsed_value = ''
    for i in range(len_str_value):
        if more_than_thousand and not i%3 and i:
            parsed_value = '.' + parsed_value
        parsed_value = str_value[i] + parsed_value        
    return parsed_value

def divide_value_by_thousand(value):
    return str(value//1000) + 'k'
          
def user_generator(user, line_name):            
    tmp_user = nata_user.query.filter_by(id=str(user)).first()
    if not isinstance(tmp_user, nata_user):
        new_user = nata_user(id=str(user), user_line=line_name)
        db.session.add(new_user)
        db.session.commit()
        tmp_user = nata_user.query.filter_by(id=str(user)).first()

    return tmp_user

