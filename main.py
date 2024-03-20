from database import execute
import requests
import hashlib


API_KEY = "3eef92f0711c5de6597a3a17adef4954"

create_table_users_stmt = """
CREATE TABLE users(id INTEGER PRIMARY KEY, nickname varchar (50), password varchar (25))
"""
# execute(create_table_users_stmt, is_commitable=True)


def register(nickname, password):
    print("РЕГИСТРАЦИЯ")
    str_hash_password = hashlib.sha512(password.encode()).hexdigest()
    stmt = """
    INSERT INTO users(nickname, password) VALUES (?, ?)
    """
    return execute(
        stmt, (nickname, str_hash_password), is_commitable=True
    )


def login(nickname, password) -> bool:
    print("ЛОГИН")
    str_hash_password = hashlib.sha512(password.encode()).hexdigest()
    stmt = """
    SELECT nickname, password FROM users WHERE nickname == ? AND password == ?
    """
    list_for_login = execute(
        stmt, (nickname, str_hash_password), is_fetchable=True, fetch_strategy="one"
        )
    if list_for_login is None: 
        print("Нет такого аккаунта(")
        return False 
    else: 
        print("Вы вошли в аккаунт!") 
        return True
    

def get_weather_by_coordinates(lat: float, lon: float) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    response = requests.get(url, params=params)
    posts = response.json()
    if response.status_code != 200:
        raise ValueError("такой координаты нет(")
    return posts


def get_weather_by_name(city_name: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
    }
    response = requests.get(url, params=params)
    posts = response.json()
    return posts


def print_weather(data: dict) -> str:
    print(
        f"Город: {data['name']}\nМаксимальная температура: {data['main']['temp_max']} градусов\nМинимальная температура: {data['main']['temp_min']} градусов\nСкорость ветра: {data['wind']['speed']} м\с"
    )


while True:
    choice_init = input("Регистрация или Вход?: ")
    if choice_init.lower() == "регистрация":
        nickname = input("Введите ваш никнейм: ")
        password = input("Введите ваш пароль: ")
        register(nickname=nickname, password=password)
    elif choice_init.lower() == "вход":
        nickname = input("Введите ваш никнейм: ")
        password = input("Введите ваш пароль: ")
        checker = login(nickname=nickname, password=password)
        if checker is True:
            while True:
                choice = input("Вы будете искать погоду по названию города или по координатам (или выход)? / город, координаты, выход: ")
                if choice.lower() == "город": 
                    user_city = input("Напишите город: ")
                    print_weather(get_weather_by_name(user_city))
                    stmt = """
                    INSERT INTO history(nickname, city_name, city_coordinates) VALUES(?, ?, ?)
                    """
                    execute(stmt, (nickname, user_city, "None"), is_commitable=True)
                elif choice.lower() == "координаты": 
                    user_lat = float(input("Напишите широту: "))
                    user_lon = float(input("Напишите долготу: "))
                    print_weather(get_weather_by_coordinates(user_lat, user_lon))
                    stmt = """
                    INSERT INTO history(nickname, city_name, city_coordinates) VALUES(?, ?, ?)
                    """
                    str_for_coordinates = f"lat: {user_lat}, lon: {user_lon}"
                    execute(stmt, (nickname, "None", str_for_coordinates), is_commitable=True)
                elif choice.lower() == "выход": 
                    break
                else: 
                    print("404") 
                choice_last = input("вы хотите увидеть свою историю поиска?/ да, нет: ")
                if choice_last.lower() == "да":
                    print("1 - user's id, 2 - user's nickname, 3 - city, 4 - coordinates")
                    stmt = """
                    SELECT * FROM history
                    """
                    whole_history = execute(stmt, is_fetchable=True, fetch_strategy="all")
                    print(whole_history)
