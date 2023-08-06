from olstecnologia.services.check_db_service import check_db, check_tables, check_columns, check_lines
from olstecnologia.services.utils_service import colors, abort_system
from olstecnologia.config import Conn
import os, time, random as rd
from olstecnologia.features.update_addres_feature import update_address_clini7, update_address_admini7
from olstecnologia.features.read_fb_for_postgres_feature import population_postgres
from sqlalchemy import MetaData, Table
from tqdm import tqdm

class Services:
    def __init__(self, string_connection) -> None:
        self.string_connection = string_connection

        try:
            connection = Conn(f"firebird://{string_connection}")

            engine = connection.engine()
            metadata = connection.metadata()
            inspect = connection.inspect()
            session = connection.session()
            session_maker = connection.session_maker()

            self.conn =  (engine, connection, metadata, inspect, session, session_maker)
    
        except Exception as e:
            raise()
  
    def menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors("gold", "====== MENU PRINCIPAL ======\n\n"))
        print(f"{colors('gold', '1')} => Análises no banco\n{colors('gold', '2')} => Atualizar endereços Clin7\n{colors('gold', '3')} => Atualizar endereços Admini7\n{colors('gold', '4')} => Ler do Firebird e adicionar no Firebird\n{colors('gold', '5')} => Sair do sistema\n\n")
        
        opt = input("Opção: ").lower()

        if opt == "1":
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== ANÁLISES NO BANCO ======\n\n"))
            print(f"{colors('gold', '1')} => Verificar Banco o banco completo\n{colors('gold', '2')} => Verificar tabela(s)\n{colors('gold', '3')} => Verificar coluna(s)\n{colors('gold', '4')} => Verificar linhas\n{colors('gold', '5')} => Sair do sistema\n\n")

            opt = input("Opção: ").lower()

            if opt == "1":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.verify_db()

            elif opt == "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.verify_table()

            elif opt == "3":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.verify_columns()

            elif opt == "4":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.verify_lines()

            elif opt == "5":
                abort_system()

        elif opt == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.update_address("clini7")

        elif opt == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.update_address("admini7")

        elif opt == "4":
            self.read_fb_for_postgres()
            
        elif opt == "5":
            abort_system()
        else:
            print("")
            print(colors("red", "Você precisa escolher uma opção de 1 a 4!"))
            print("vontando...")
            time.sleep(1.5)
            self.menu()

    def verify_db(self):
        
        print(colors("gold", "====== VERIFICANDO O BANCO DE DADOS ======\n\n"))
       
        check_db(self.conn)

    def verify_table(self):
        print(colors("gold", "====== VERIFICANDO AS TABELAS ======\n\n"))

        tables = input(f"Quais tabelas {colors('gold', '(separadas por virgulas)')}? ").split(",")

        print("")

        metadata_obj = MetaData()

        try:
            tables = [Table(x.strip(), metadata_obj, autoload_with=self.conn[0]) for x in tqdm(tables, desc =f"Lendo as tabelas => ")]
        except Exception as e:
            print(f"\n{colors('red', 'ERRO:')} Não encontrou a tabela {colors('blue', e.args[0])} no banco de dados")
            abort_system(False)


        check_tables(self.conn, tables=tables)

    def verify_columns(self):

        print(colors("gold", "====== VERIFICANDO AS COLUNAS ======\n\n"))

        table_name = input("Qual tabela? ")

        metadata_obj = MetaData()

        try:
            table = Table(table_name, metadata_obj, autoload_with=self.conn[0])
            columns_in_table = [column['name'] for column in  tqdm(self.conn[3].get_columns(table_name), desc =f"Buscando as colunas => ")]
            print(f"Colunas encontradas: {columns_in_table}\n")

            columns = input("Quais colunas? (deixa em branco para todas): ")
            print("")
        except Exception as e:
            print(f"\n{colors('red', 'ERRO:')} Não encontrou a tabela {colors('blue', table_name)} no banco de dados")
            abort_system(False)


        if columns == "" or columns == "all":
            check_columns(conn=self.conn, table=table)
        else:
            check_columns(conn=self.conn, table=table, columns=columns)
    
    def verify_lines(self):

        print(colors("gold", "====== VERIFICANDO AS COLUNAS ======\n\n"))

        table_name = input("Qual tabela? ")

        metadata_obj = MetaData()

        try:
            table = Table(table_name, metadata_obj, autoload_with=self.conn[0])
            columns_in_table = [column['name'] for column in  tqdm(self.conn[3].get_columns(table_name), desc =f"Buscando as colunas => ")]
            # print(f"Colunas encontradas: {columns_in_table}\n")
            column = input("Qual coluna? ")
            print("")
        except:
            print(f"\n{colors('red', 'ERRO:')} Não encontrou a tabela {colors('blue', table_name)} no banco de dados")
            abort_system(False)

        try:
            columns_in_table.index(column)
            column = table.columns[column]
        except:
            print(f"\n{colors('red', 'ERRO:')} Não encontrou a coluna {colors('blue', column)} na tabela {colors('blue', table_name)}")
            abort_system(False)
        
        lines = input("Quais linhas? (ex. 1,10 ou ENTER para todas as linhas): ")
        print("")

        if lines:
            check_lines(self.conn, table=table, column=column, lines=lines)
        else:
            check_lines(self.conn, table=table, column=column)

    def update_address(self, db, alias=''):
        if db == "clini7":
            if alias:
                update_address_clini7(self.conn, alias)
            else:
                update_address_clini7(self.conn)

        elif db == "admini7":
            if alias:
                update_address_admini7(self.conn, alias)
            else:
                update_address_clini7(self.conn)

        else:
            raise ValueError("Não existe esta ATUALIZAÇÃO para este banco de dados!")
        
    def read_fb_for_postgres(self):
        population_postgres(self.conn)

    def conn(self):
        return self.conn