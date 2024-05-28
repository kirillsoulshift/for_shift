import pytest
import sys
import os
os.environ["UNIT_TEST"]= "true"
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_dir)

from fastapi.security import OAuth2PasswordRequestForm
from model.user import  User
from model.error import WrongPasswordException
from service import employee
from passlib.context import CryptContext
from web import employee
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

@pytest.fixture
def sample_user() -> User:
    return User(username = 'user1',
                    salary = '60000',
                    promotion_date = '12.12.2024',        
                    disabled = False)

@pytest.fixture
def sample_form() -> OAuth2PasswordRequestForm:
    return OAuth2PasswordRequestForm(username = 'user1',
                                    password = 'secret1')

@pytest.fixture
def sample_form_wrong_username() -> OAuth2PasswordRequestForm:
    return OAuth2PasswordRequestForm(username = 'user3',
                                    password = 'secret1')

@pytest.fixture
def sample_form_wrong_password() -> OAuth2PasswordRequestForm:
    return OAuth2PasswordRequestForm(username = 'user1',
                                    password = 'secret3')

def test_login_for_access_token(sample_form):
    res = employee.login_for_access_token(sample_form)
    assert type(res.access_token) is str
    assert len(res.access_token) != 0
    assert type(res.token_type) is str
    assert len(res.token_type) != 0

def test_login_for_access_token_wrong_username(sample_form_wrong_username):
    with pytest.raises(WrongPasswordException):
        _ = employee.login_for_access_token(sample_form_wrong_username)

def test_login_for_access_token_wrong_password(sample_form_wrong_password):
    with pytest.raises(WrongPasswordException):
        _ = employee.login_for_access_token(sample_form_wrong_password)

def test_read_users_me(sample_user):
    res = employee.read_users_me(sample_user)
    assert res.username == sample_user.username
    assert res.salary == sample_user.salary
    assert res.promotion_date == sample_user.promotion_date
    assert res.disabled == sample_user.disabled
    