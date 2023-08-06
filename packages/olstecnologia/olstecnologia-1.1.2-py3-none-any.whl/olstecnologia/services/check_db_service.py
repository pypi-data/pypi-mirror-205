from sqlalchemy import MetaData, Table, select
from olstecnologia.services.utils_service import colors
from tqdm import tqdm

# Inspecionar o banco e pegar as tabelas.
# Ler cada tabela procurando o erro
    # encontrando erro vericar as colunas Adicionar no errors o nome da tabela
        # Verica cada coluna para ver qual que tem erro.
            # achando a coluna com erro, adicionar no dict da tabela criada e verificar as linhas
                # achando a liha com erro verificar cada digito.


def check_db(conn):

    tables, errors = check_tables(conn=conn, mode="r")

    tables_error = []
    errors_found = list()

    for error in errors:
        for table, error in error.items():
            if len(error) > 0:
                tables_error.append(table)
                errors_found.append((table,error))
    
    print(colors("reset","Quantidade de tabelas: ") + colors("gold", str(len(tables))))
    print(colors("reset", "Quantidade de erros encontrado: ") + colors("gold", str(len(tables_error))))

    if len(tables_error) > 0:
        print(colors("reset", "Tabelas com erros: ") + colors("gold", str(tables_error)))
        print("")
        print(colors("red", "Erros encontrados:"))
        [print(colors("reset") + f"Tabela: {x[0]}: Colunas: {x[1]}") for x in errors_found]
        print(colors("reset", " "))
    else:
        print("")
        print(colors("gold", "Não foi encontrado erros neste banco de dados!"))

def check_tables(conn, tables = "*", mode="p"):

    insp = conn[3]
    metadata_obj = MetaData()

    if tables == "*":
         tables = [Table(x, metadata_obj, autoload_with=conn[0]) for x in tqdm(insp.get_table_names(), desc =f"Lendo todas tabelas => ")]

    if type(tables) == str:
        tables = tables.split(",")
        tables = [Table(x, metadata_obj, autoload_with=conn[0]) for x in tqdm(tables, desc =f"Lendo as tabelas => ")]

    errors_found = list()

    for table in tqdm(tables, desc =f"Verificando erros na tabela => "):
        columns_errors = { table: check_columns(conn, table=table, mode="r")}
        errors_found.append(columns_errors)

    if mode == 'r':
        return tables, errors_found
    else:
        tables_error = []
        errors = list()

        for error in errors_found:
            for table, error in error.items():
                if len(error) > 0:
                    tables_error.append(table)
                    errors.append((table, error))

        print("")
        print(f"Tabela(s): {[x.name for x in tables]}")
        print(f"Quantidade de erros encontrados: {len(tables_error)}")
        if len(tables_error) > 0:
            print(f"Tabelas com erro: {[x.name for x in tables_error]}")
            print("")
            print("Erros encontrados:")
            [print(f"Tabela: {x[0]}: Colunas: {x[1]}") for x in errors]

        else:
            print("")
            print(colors("green", "Não foi encontrado erros nas tabelas!"))

        return tables_error, errors

def check_columns(conn, table, columns="*", mode ="p"): #1:40
    
    engine = conn[0]
    insp = conn[3]

    errors_found = []

    if columns == "*":
        # columns = [column['name'] for column in  insp.get_columns(table)]
        columns = [x for x in table.columns]

    if type(columns) == str:
        columns = columns.split(",")

        for col in columns:
            columns = []

            if col in [x for x in table.columns]:
                columns.append(col)



    for col in columns:
    
        try:
                query = select(col)

                with engine.connect() as s:
                    s.execute(query).all()

        except Exception as e:
            errors_found.append(col)
            continue

    if mode == 'r':
        return errors_found
    else:
        
        print(f"Tabela: {table}")
        print(f"Coluna(s): {[x.name for x in columns]}")
        print(f"Quantidade de erros encontrados: {len(errors_found)}")
        if len(errors_found) >0:
            print(f"Colunas com erro: {errors_found}")
        else:
            print("")
            print(colors("green", "Não foi encontrado erros nas colunas!"))

def check_lines(conn, table, column, lines="*", mode ="p"):

    engine = conn[0]

    errors_found = list()

    if lines == "*":
        columns = [x for x in table.columns]
        print("Verificando a tabela", end="")

        for col in columns:
            try:
                print(colors("gold", "."), end="", flush=True)
                with engine.connect() as s:
                    data = s.execute(select(col)).all()
                    end = len(data)
                    init = 1
                    break

            except Exception as e:
                print(colors("gold", "."), end="", flush=True)
                continue
        
        if not end or not init and mode == "p":
            print(f"A {table.name} esta com todas colunas com erros")
            error = f"A {table.name} esta com todas colunas com erros"
            errors_found.append(error)
            return None

        if not end or not init and mode == "r":
            return False

    else:
        lines = [line.strip() for line in lines.split(",")]
        init = int(lines[0])
        end = int(lines[1])
        
    for lin in tqdm(range(0,end), desc ="Analisando cada linha: "):
        query = select([column]).limit(1).offset(lin)

        try:
                with engine.connect() as s:
                    s.execute(query).first()

        except UnicodeDecodeError as e:
            error = {lin:(f"Erro: {e.args[0]}", f"Valor: {e.args[1]}",f"Posição: {e.args[2]} a {e.args[3]}", f"Descrição do erro {e.args[4]}")}
            errors_found.append(error)
            continue
        except Exception as e:
            error = e.args
            errors_found.append(error)
            continue

    if mode == 'r':
        return errors_found
    else:
        print("")
        print(f"Tabela: {table}")
        print(f"Coluna: {column}")
        print(f"Quantidade de erros: {len(errors_found)}")
        if len(errors_found) >0:
            print("Erros encontrados:")
            [print(x) for x in errors_found]
        else:
            print("")
            print(colors("green", "Não foi encontrado erros nas linhas!"))

def update_lines():
    pass
