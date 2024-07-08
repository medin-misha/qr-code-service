import sqlite3


def minus_qr(data_base_path: str, username: str, count: int) -> None:
    """
    функция которая отнимает куаркоды у пользователя
    :param data_base_path:
    :param username:
    :param count:
    :return:
    """
    with sqlite3.connect(data_base_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET qr_count = qr_count - ?
            WHERE username = ?;
            """, (count, username)
        )
        conn.commit()


def plus_qr(data_base_path: str, username: str, count: int) -> None:
    """
    Функция которая добавляет куаркоды пользователю
    :param data_base_path:
    :param username:
    :param count:
    :return:
    """
    with sqlite3.connect(data_base_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET qr_count = qr_count + ?
            WHERE username = ?;
            """, (count, username)
        )
        conn.commit()


def get_qrs_count(data_base_path: str, username: str) -> int:
    """
    Эта функция возвращяет количество оставшихся куаркодов
    :param data_base_path:
    :param username:
    :return:
    """
    with sqlite3.connect(data_base_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            select qr_count from users
            WHERE users.username = ?;
            """, (username,)
        )
        return cursor.fetchone()[0]
