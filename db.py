import mysql.connector

def get_connection():
    return mysql.conncetor.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "u194014241_kpi_db"
    )


