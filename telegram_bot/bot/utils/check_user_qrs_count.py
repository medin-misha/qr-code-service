import sqlite3


def check_user_qrs_count(data_base_path: str, username: str) -> int:
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
            where users.username = ?
            """, (username,)
        )
        conn.commit()
        return cursor.fetchone()[0]
