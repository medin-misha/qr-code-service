import sqlite3


def add_new_user(data_base_path: str, username: str) -> None:
    """
    Эта функция проверяет, пользовался ли человек нашим ботом если нет то заносит его в базу данных
    :param data_base_path:
    :param username:
    :return:
    """
    with sqlite3.connect(data_base_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            select username from users
            where username = ?
            """, (username,)
        )
        result: list = cursor.fetchall()

        if len(result) == 0:
            cursor.execute(
                """
                insert into users (username, qr_count) 
                values (?,?)
                """, (username, 0)
            )
        conn.commit()
