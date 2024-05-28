from model.user import UserInDB
from model.error import MissingUser
from data.init_db import curs

# curs.execute("""create table if not exists employees(
#                     username text primary key,                    
#                     salary text,
#                     promotion_date text,
#                     disabled text,
#                     hashed_password text,)""")

def row_to_model(row: tuple) -> UserInDB:
    
    """Запоняет форму UserInDB данными из кортежа"""

    username, salary, promotion_date, disabled, hashed_password = row
    get_bool = lambda val: True if val == 'True' else False
    return UserInDB(username=username, 
                    salary=salary, 
                    promotion_date=promotion_date, 
                    disabled=get_bool(disabled),
                    hashed_password=hashed_password)

def get_user(username: str) -> UserInDB:

    """Поиск строки в базе данных по username, возвращает объект UserInDB"""

    qry = "select * from employees where username=:username"
    params = {"username": username}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise MissingUser(msg=f'User {username} not found')
