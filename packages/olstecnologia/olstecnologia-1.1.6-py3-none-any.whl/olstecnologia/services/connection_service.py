from olstecnologia.config import Conn

def connect_db(connect_string):

    try:
        connection = Conn(f"firebird://{connect_string}")

        engine = connection.engine()
        metadata = connection.metadata()
        inspect = connection.inspect()
        session = connection.session()
        session_maker = connection.session_maker()

        return (engine, connection, metadata, inspect, session, session_maker)
    except Exception as e:
        print("Erro na conexão do banco de dados!")
        print(f"Erro: {e}" )