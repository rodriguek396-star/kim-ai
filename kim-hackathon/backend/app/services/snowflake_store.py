from contextlib import contextmanager
from ..config import settings

@contextmanager
def snowflake_connection():
    import snowflake.connector
    required = [settings.snowflake_account, settings.snowflake_user, settings.snowflake_password, settings.snowflake_warehouse]
    if not all(required): raise RuntimeError('Configuration Snowflake incomplète : renseignez SNOWFLAKE_ACCOUNT/USER/PASSWORD/WAREHOUSE.')
    conn = snowflake.connector.connect(account=settings.snowflake_account,user=settings.snowflake_user,password=settings.snowflake_password,warehouse=settings.snowflake_warehouse,database=settings.snowflake_database,schema=settings.snowflake_schema,role=settings.snowflake_role or None)
    try: yield conn
    finally: conn.close()
