from sqlalchemy import Table, select, update, bindparam, MetaData, inspect
from sqlalchemy.dialects.postgresql import insert
from olstecnologia.services.utils_service import colors, abort_system, get_ibges
from olstecnologia.services.connection_service import Conn
import os, time, random as rd
import ipdb


def loading_dot(connect_string):
    x = rd.randint(0,10)

    for i in range(10):
        print(".", end="", flush=True)

        if i == x:
            return Conn(connect_string)
            
        time.sleep(0.5)

def create_table(metadata, data: Table):
    def get_columns(columns):
        for col in columns: 
            # ipdb.set_trace()
            yield col

    columns = list(get_columns(data.columns))
    ipdb.set_trace()
    
    cols = ''
    for col in columns:
        cols += col + ",\n"

    properties = f"""
        {data.name},\n
        {metadata},\n
        {cols}
    """

    ipdb.set_trace()

    return Table(data.name, metadata, **get_columns(data.columns))

    


def get_data_in_fb(table, conn):
    metadata_fdb = MetaData()

    table = Table(table, metadata_fdb, autoload_with=conn[0])

    with conn[0].connect() as s:
            try:
                data = s.execute(select(table)).all()
                ipdb.set_trace()
                return data
            except Exception as e:
                error = e.args
                ipdb.set_trace()

def insert_data_in_fb(conn: Conn, tb, data):
    metadata_post = MetaData()

    insp = conn.inspect()
    engine = conn.engine()
    session = conn.session()

    table = create_table(metadata_post, tb[0])


    ipdb.set_trace()

    # metadata_post.create_all(engine)
    ipdb.set_trace()
    table.create(engine)

    # table = Table(table, metadata_post, autoload_with=conn.engine())

    # datas = Table(data)

    for x in data:
        # query = table(id_endereco=data[0],\
        #                 id_pessoa=x[1],\
        #                 id_rua=x[2],\
        #                 numero=x[3],\
        #                 complemento=x[4],\
        #                 principal=x[5],\
        #                 descricao=x[6],\
        #                 id_contrato=x[7],\
        #                 valor_contrato=x[8])
        # print(x)
        stmt = insert(table).values(id_endereco=data[0],\
                        id_pessoa=x[1],\
                        id_rua=x[2],\
                        numero=x[3],\
                        complemento=x[4],\
                        principal=x[5],\
                        descricao=x[6],\
                        id_contrato=x[7],\
                        valor_contrato=x[8])
        
        # do_nothing_stmt = stmt.on_conflict_do_nothing()

        try:
            # session.add(stmt)
            # session.commit()
            with engine.connect() as s:
                result = s.execute(stmt)
            ipdb.set_trace()
        except Exception as e:
            print(e)
            ipdb.set_trace()


    ipdb.set_trace()


def population_postgres(conn):
        
        metadata_fdb = MetaData()

        ipdb.set_trace()
        insp = conn[3]

        tables_in_db = insp.get_table_names()

        all_tables = list(map(lambda x: Table(x, metadata_fdb, autoload_with=conn[0]), tables_in_db))

        schemas = insp.get_schema_names()

        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors("gold", "====== LENDO DADOS DO ")+colors("green", "FIREBIRD ")+ colors("gold", "E COLOCANDO NO ")+colors("green", "POSTGRES ")+ colors("gold", "======"))
        print("")

        # for schema in schemas:
        #     print(f"Schema: {schema}")
        #     procedures = insp.get_procedure_names(schema=schema)
        #     for procedure in procedures:
        #         print(f"\tProcedure: {procedure}")

        # ipdb.set_trace()

        table = Table("PESSOA_ENDERECO", metadata_fdb, autoload_with=conn[0])

        data = get_data_in_fb("PESSOA_ENDERECO", conn)

        # string_connect = "postgresql://scott:tiger@localhost:5432/mydatabase"

        print(f"======== STRING DE CONEXÃO | (usuário{colors('gold', ':')}senha{colors('gold', '@')}host{colors('gold', '/')}database) ========")
        # connect_string = input("String de conexão: ")
        connect_string = "postgresql://postgres:root@127.0.0.1:5432/admini7_all"
        print("")
        print("conectando com o bando", end="")
        
        try:
            conn = loading_dot(connect_string)
            ipdb.set_trace()
            insert_data_in_fb(conn, all_tables, data)
        except Exception as e:
            print(e.args)
            print(f"Erro aon conectar no banco de dados postgres")
            abort_system(False)

        # srv.menu()




        