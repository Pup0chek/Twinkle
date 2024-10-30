import psycopg2
import os
import pandas as pd

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Almaty111@db:5432/lol")

# Path to the Excel file
input_file = "exercises_data.xlsx"

# Чтение данных из Excel-файла с помощью pandas
try:
    df = pd.read_excel(input_file)

    # Проверяем, что столбцы существуют
    required_columns = ['Name', 'Description', 'Muscle Group', 'Equipment', 'Difficulty']
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Отсутствует столбец: {column}")

except Exception as e:
    print(f"Ошибка при чтении данных из Excel-файла: {e}")
    exit(1)

# Подключение к базе данных и вставка данных
connection = None
cursor = None
try:
    # Подключаемся к базе данных
    connection = psycopg2.connect(DATABASE_URL)
    connection.set_client_encoding('UTF8')
    cursor = connection.cursor()

    # SQL-запрос для вставки данных
    insert_query = """
        INSERT INTO exercises ("name", "description", "muscle_group", "equipment", "difficulty")
        VALUES (%s, %s, %s, %s, %s)
    """

    # Вставка данных из DataFrame в базу данных
    for _, row in df.iterrows():
        name = row['Name']
        description = row['Description']
        muscle_group = row['Muscle Group']
        equipment = row['Equipment']
        difficulty = row['Difficulty']

        cursor.execute(insert_query, (name, description, muscle_group, equipment, difficulty))

    # Фиксируем изменения в базе данных
    connection.commit()
    print("Данные успешно вставлены в базу данных")

except Exception as e:
    print(f"Ошибка при вставке данных в базу данных: {e}")

finally:
    # Закрываем соединение
    if cursor:
        cursor.close()
    if connection:
        connection.close()

#convert to csv
# import pandas as pd
#
# # Path to the uploaded Excel file
# input_file = '/mnt/data/exercises_data.xlsx'
# # Path to save the output CSV file
# output_file = '/mnt/data/exercises_data.csv'
#
# # Read the Excel file
# df = pd.read_excel(input_file)
#
# # Save as CSV with ',' as the delimiter
# df.to_csv(output_file, index=False, sep=',')
#
# output_file

# COPY exercises (name, description, muscle_group, equipment, difficulty)
# FROM 'C:\Users\User\Downloads\exercises_data_utf8_sig.csv'  -- Укажите полный путь к файлу
# WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');