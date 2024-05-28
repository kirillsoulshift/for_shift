from init_db import curs

def get_one(username: str):
    qry = "select * from employees where username=:username"
    params = {"username": username}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row
    else:
        return None
    
def get_all():
    qry = "select * from employees"
    res = curs.execute(qry)
    print(res.fetchall())

# res = curs.execute("SELECT name FROM sqlite_master")
# print(res.fetchone())
get_all()