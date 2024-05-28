import pytest
import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from model.user import UserInDB
from model.error import MissingUser
from data import employee
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

@pytest.fixture
def sample() -> UserInDB:
    return UserInDB(username = 'user1',
                    salary = '60000',
                    promotion_date = '12.12.2024',        
                    disabled = False,
                    hashed_password = pwd_context.hash('secret1'))

def test_get_user(sample):
    res = employee.get_user(sample.username)    
    assert res.username == sample.username
    assert res.salary == sample.salary
    assert res.promotion_date == sample.promotion_date
    assert res.disabled == sample.disabled
    assert pwd_context.verify('secret1', res.hashed_password)

def test_get_user_missing():    
    with pytest.raises(MissingUser):
        _ = employee.get_user('user3')

