import pytest
import sys
import os
os.environ["UNIT_TEST"]= "true"
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from model.user import UserInDB
from model.error import MissingUser, UnathenticatedUser, CredentialsException
from service import employee
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

@pytest.fixture
def sample() -> UserInDB:
    return UserInDB(username = 'user1',
                    salary = '60000',
                    promotion_date = '12.12.2024',        
                    disabled = False,
                    hashed_password = pwd_context.hash('secret1'))

@pytest.fixture
def sample_token() -> str:
    return employee.create_access_token({"sub": 'user1'})

@pytest.fixture
def no_sub_sample_token() -> str:
    return employee.create_access_token({"sub1": 'user1'})

@pytest.fixture
def user_missing_sample_token() -> str:
    return employee.create_access_token({"sub": 'missing_user'})

def test_authenticate_user(sample):
    res = employee.authenticate_user(sample.username, 'secret1')
    assert res.username == sample.username
    assert res.salary == sample.salary
    assert res.promotion_date == sample.promotion_date
    assert res.disabled == sample.disabled
    assert pwd_context.verify('secret1', res.hashed_password)

def test_authenticate_user_not_found():
    with pytest.raises(MissingUser):
        _ = employee.authenticate_user('user3', 'secret1')

def test_authenticate_user_unauthed():
    with pytest.raises(UnathenticatedUser):
        _ = employee.authenticate_user('user1', 'secret2')
    
def test_create_access_token(sample):    
    res = employee.create_access_token({"sub": sample.username})
    assert type(res) is str

def test_get_current_user(sample, sample_token):
    res = employee.get_current_user(sample_token)    
    assert res.username == sample.username
    assert res.salary == sample.salary
    assert res.promotion_date == sample.promotion_date
    assert res.disabled == sample.disabled
    assert pwd_context.verify('secret1', res.hashed_password)

def test_get_current_user_no_sub(no_sub_sample_token):
    with pytest.raises(CredentialsException):
        _ = employee.get_current_user(no_sub_sample_token)

def test_get_current_missing_user(user_missing_sample_token):
    with pytest.raises(MissingUser):
        _ = employee.get_current_user(user_missing_sample_token)
