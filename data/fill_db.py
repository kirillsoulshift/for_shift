from init_db import conn, curs
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def create(user: dict) -> None:
    qry = """insert into employees values
            (:username, :salary, :promotion_date, :disabled, :hashed_password)"""
    params = user    
    curs.execute(qry, params)
    conn.commit()
    print('User Created', user)


example_users_db = {
    'user1': {
        'username': 'user1',
        'salary': '60000',
        'promotion_date': '12.12.2024',        
        'disabled': 'False',
        'hashed_password': pwd_context.hash('secret1'),
    },
    'user2': {
        'username': 'user2',
        'salary': '80000',
        'promotion_date': '12.11.2024',        
        'disabled': 'True',
        'hashed_password': pwd_context.hash('secret2'),
    }
}

curs.execute("""create table if not exists employees(
                    username text primary key,
                    salary text,
                    promotion_date text,
                    disabled text,
                    hashed_password text)""")

create(example_users_db.get('user1'))
create(example_users_db.get('user2'))
