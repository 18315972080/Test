import os

# pymysql MySQL bridge — only when DATABASE_URL contains mysql
_db_url = os.environ.get("DATABASE_URL", "")
if "mysql" in _db_url:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
