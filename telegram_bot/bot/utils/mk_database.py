import sqlite3


def mk_database(path: str) -> None:
    """
    Создаёт и настраивает базу данных для бота если её нет
    :param path:
    :return:
    """
    with sqlite3.connect(path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(
            """
            create table if not exists users (
                username CHAR(50) primary key,
                qr_count integer
            )
            """
        )


if __name__ == '__main__':
    pass
