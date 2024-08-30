import requests
from faker import Faker
from bs4 import BeautifulSoup
import time
import random

# Hàm tạo mật khẩu ngẫu nhiên từ 1 đến 9
def generate_password(length=8):
    characters = '123456789'
    return ''.join(random.choice(characters) for _ in range(length))

# Hàm tạo số điện thoại ngẫu nhiên
def generate_phone():
    return '098' + ''.join(random.choice('0123456789') for _ in range(8))

# Khởi tạo Faker
fake = Faker()

# URL của trang đăng ký
url = "https://hoangducanh.com/register"

# Số lượng đăng ký mong muốn
start_username = 8888
end_username = 81237912
current_username = start_username

while True:
    # Tạo dữ liệu ngẫu nhiên
    username = f"caovanvu{current_username:02}"
    phone = generate_phone()
    password = generate_password()
    confirm_password = password  # Xác nhận mật khẩu (phải giống mật khẩu)

    # Tạo dữ liệu POST
    data = {
        "username": username,
        "phone": phone,
        "password": password,
        "password_confirmation": confirm_password,
        "_token": ""  # CSRF token sẽ được cập nhật sau
    }

    # Lấy CSRF token
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '_token'})['value']

    if not csrf_token:
        print("CSRF token không tìm thấy!")
        continue

    # Cập nhật dữ liệu để bao gồm CSRF token
    data['_token'] = csrf_token

    # Gửi yêu cầu POST để đăng ký
    response = session.post(url, data=data)

    # Kiểm tra kết quả
    if response.status_code == 200:
        print(f"Đăng ký thành công! Username: {username}, Phone: {phone}, Password: {password}")
        # Ghi thông tin vào file hoangducanh.txt
        with open('hoangducanh.txt', 'a') as f:
            f.write(f"Username: {username}\nPhone: {phone}\nPassword: {password}\n\n")
    else:
        print(f"Đăng ký thất bại: {response.status_code}")

    # Cập nhật username cho lần đăng ký tiếp theo
    current_username += 1
    if current_username > end_username:
        current_username = start_username

    # Đợi một khoảng thời gian giữa các lần đăng ký để tránh bị chặn
