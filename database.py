import sqlite3


def get_connection():
    try:
        con = sqlite3.connect("./mock_task.db")
        return con
    except Exception as e:
        print("Connection unsuccessfull")
        print(e)
        raise e


def execute(
    stmt: str,
    values: tuple = (),
    is_commitable: bool = False,
    is_fetchable: bool = False,
    fetch_strategy: str = "one",
    fetch_size: int = 5,
):
    con = get_connection()
    cursor = con.cursor()

    cursor.execute(stmt, values)

    res = None
    if is_fetchable:
        if fetch_strategy == "one":
            res = cursor.fetchone()
        elif fetch_strategy == "many":
            res = cursor.fetchmany(size=fetch_size)
        elif fetch_strategy == "all":
            res = cursor.fetchall()

    cursor.close()

    if is_commitable:
        con.commit()
    con.close()

    return res


get_connection()
