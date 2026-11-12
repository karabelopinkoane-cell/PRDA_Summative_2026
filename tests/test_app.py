import pytest
import app as application

@pytest.fixture()
def client(tmp_path, monkeypatch):
    test_file = tmp_path / 'users.json'
    test_file.write_text('{}', encoding='utf-8')
    monkeypatch.setattr(application, 'DATA_FILE', test_file)
    application.app.config.update(TESTING=True, SECRET_KEY='test-secret')
    with application.app.test_client() as client:
        yield client

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'PRDA Practice' in response.data

def test_valid_registration_creates_profile(client):
    response = client.post('/register', data={'full_name':'Test Student','username':'test_student','email':'student@example.com','phone':'0821234567','bio':'Practice profile'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Student' in response.data
    assert b'Profile created successfully' in response.data

def test_invalid_email_is_rejected(client):
    response = client.post('/register', data={'full_name':'Test Student','username':'test_student','email':'invalid-email','phone':'0821234567','bio':''}, follow_redirects=True)
    assert b'Enter a valid email address' in response.data

def test_phone_with_letters_is_rejected(client):
    response = client.post('/register', data={'full_name':'Test Student','username':'test_student','email':'student@example.com','phone':'082ABC4567','bio':''}, follow_redirects=True)
    assert b'Phone number must contain 7' in response.data

def test_profile_can_be_updated_after_registration(client):
    client.post('/register', data={'full_name':'Test Student','username':'test_student','email':'student@example.com','phone':'0821234567','bio':'First bio'}, follow_redirects=True)
    response = client.post('/profile/test_student/edit', data={'full_name':'Updated Student','email':'updated@example.com','phone':'0837654321','bio':'Updated bio'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Student' in response.data
    assert b'updated@example.com' in response.data
    assert b'Profile updated successfully' in response.data

def test_unknown_login_fails(client):
    response = client.post('/login', data={'username':'missing_user'}, follow_redirects=True)
    assert b'No profile was found for that username' in response.data
