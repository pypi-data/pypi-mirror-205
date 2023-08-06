from olstecnologia.services.utils_service import colors, abort_system
from olstecnologia.services.services_service import Services
from olstecnologia.services.check_db_service import check_db, check_tables, check_columns, check_lines
from olstecnologia.features.update_addres_feature import update_address_admini7, update_address_clini7
import json, os, time, random as rd
import urllib.parse
from sqlalchemy import MetaData, Table
from tqdm import tqdm

def menu_app():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colors("gold", "====== MENU PRINCIPAL ======\n\n"))
    print(f"{colors('gold', '1')} => Análises no banco\n{colors('gold', '2')} => Atualizar endereços Clin7\n{colors('gold', '3')} => Atualizar endereços Admini7\n{colors('gold', '4')} => Sair do sistema\n\n")
    
    opt = input("Opção: ").lower()

    if opt == "1":
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors("gold", "====== ANÁLISES NO BANCO ======\n\n") )
        print(f"{colors('gold', '1')} => Verificar Banco o banco completo\n{colors('gold', '2')} => Verificar tabela(s)\n{colors('gold', '3')} => Verificar coluna(s)\n{colors('gold', '4')} => Verificar linhas\n{colors('gold', '5')} => Sair do sistema\n\n")
        print("")
    
        opt = input("Opção: ").lower()

        if opt == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== VERIFICANDO O BANCO DE DADOS ======\n"))
            return None, '0'+ opt

        elif opt == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== VERIFICANDO AS TABELAS ======\n"))

            tables = input(f"Quais tabelas {colors('gold', '(separadas por virgulas)')}? ").split(",")

            print("")

            return tables, '0'+ opt

        elif opt == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== VERIFICANDO AS COLUNAS ======\n"))

            table_name = input("Qual tabela? ")
            columns = input("Quais colunas? (deixa em branco para todas): ")
            print("")

            data = [table_name, columns]
            
            return data, '0'+ opt
        
        elif opt == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== VERIFICANDO AS LINHAS ======\n"))

            table_name = input("Qual tabela? ")
            column = input("Qual coluna? ")
            print("")

            data = table_name, column

            return data, "0"+ opt

    elif opt == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors("gold", "====== ATUALIZAÇÃO ENDEREÇOS DO ")+colors("green", "CLINI7 ")+ colors("gold", "======"))
        print("")
        return None, '10'
    
    elif opt == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors("gold", "====== ATUALIZAÇÃO ENDEREÇOS DO ")+colors("green", "ADMINI7 ")+ colors("gold", "======"))
        print("")
        return None, '11'
    
    elif opt == "4":
        abort_system()
    else:
        print(colors("red", "Opção errada, tente novamente!"))
        os.abort()

def loading_dot(connect_string):
    x = rd.randint(0,10)

    for i in range(10):
        print(".", end="", flush=True)

        if i == x:
            return Services(connect_string)
            
        time.sleep(0.5)

def start():
    print(colors("green", "=== Sistema OLS Tecnologia ==== "))
    print("")
    print(f"{colors('gold', '1')} => Pegar dados do arquivo.\n{colors('gold', '2')} => digitar a string de conexão.\n\n")
    opt = input(f"Digite a opção {colors('green', 'ou enter')} para opção {colors('gold', '1')}: ")

    if opt.lower() == '2':
        
        print(f"======== STRING DE CONEXÃO | (usuário{colors('gold', ':')}senha{colors('gold', '@')}host{colors('gold', '/')}database) ========")
        connect_string = input("String de conexão: ")
        print("")
        print("conectando com o bando", end="")
        
        try:
            srv = loading_dot(connect_string)
        except:
            print(f"Erro aon conectar no banco de dados {alias}")
            abort_system(False)

        srv.menu()
    
    elif opt == 't':
        # connect_string = "sysdba:masterkey@localhost/C:/Users/user/Documents/dbs_tests/db_test_clin7.FDB"
        connect_string = "sysdba:masterkey@192.168.100.10/d:/Servidor/Desenvolvimento/BD DOS CLIENTES/BD - Otomed/CLINOT_08112022.FDB"
        connect_string_fredson = "sysdba:masterkey@192.168.100.10/D:/Servidor/Desenvolvimento/BD DOS CLIENTES/BD - Fredson/CLINI7.FDB"
        connect_string_admini7_unimais = "sysdba:masterkey@192.168.100.10/D:\Servidor\Desenvolvimento\BD DOS CLIENTES\BD - Unimais\ADMINI7_UNIMAIS - Copia.FDB"
        opt = input(f"Qual exemplo? {colors('gold', '1')} => clini7(Fredson) | {colors('gold', '2')} => Admini7(unimais)\n\nEscolha: ")
        
        if opt == '2':
            srv = Services(connect_string_admini7_unimais)
        else:
            srv = Services(connect_string_fredson)
        srv.menu()

    else:
        
        file_name = input("Caminho do arquivo com extensão .json: ")
        file = open(file_name, "r")

        data_dict = json.loads(file.read())


        if len(data_dict['content']) > 1:

            data, opt = menu_app()

            if not opt in ['01', '02', '03', '04', '05', '10', '11']:
                print(colors("red", "Opção errada, tente novamente!"))
                os.abort()

            for x in range(len(data_dict['content'])):
                alias = data_dict['content'][x]['Alias']
                user = data_dict['content'][x]['user_nameBD']
                password = urllib.parse.quote_plus(data_dict['content'][x]['PassWordBD'])
                host = data_dict['content'][x]['Server']
                port = data_dict['content'][x]['Porta']
                database = data_dict['content'][x]['Database']

                connect_string = f"{user}:{password}@{host}:{port}/{database}"
                
                
                print(f"conectando com o bando {colors('gold', alias)}", end="")

                try:
                    srv = loading_dot(connect_string)
                
                    if opt == "01":
                        check_db(srv.conn)

                    elif opt == "02":
                        
                        tables = data
                        
                        metadata_obj = MetaData()

                        try:
                            print("")
                            tables = [Table(x.strip(), metadata_obj, autoload_with=srv.conn[0]) for x in tqdm(tables, desc =f"Lendo as tabelas => ")]
                            check_tables(srv.conn, tables=tables)
                            print(colors("gold","=========="))
                        except Exception as e:
                            print(f"\n{colors('red', 'ERRO:')} Não encontrou a tabela {colors('blue', e.args[0])} no banco de dados")
                            print('')
                            continue

                    elif opt == "03":

                        table_name, columns = data

                        metadata_obj = MetaData()

                        try:
                            table = Table(table_name, metadata_obj, autoload_with=srv.conn[0])
                            print("")

                            if columns == "" or columns == "all":
                                check_columns(conn=srv.conn, table=table)
                            else:
                                check_columns(conn=srv.conn, table=table, columns=columns)

                            print(colors("gold","=========="))

                        except Exception as e:
                            print(e)
                            print(f"\n{colors('red', 'ERRO:')} Não encontrou a tabela {colors('blue', table_name)} ou as colunas {colors('blue', columns)} no banco de dados")
                            continue
                        

                    elif opt == "04":

                        table_name, column = data

                        metadata_obj = MetaData()

                        try:
                            table = Table(table_name, metadata_obj, autoload_with=srv.conn[0])
                            print("")
                            
                            try:
                                column = table.columns[column]
                            except:
                                print(f"\n{colors('red', 'ERRO:')} Não encontrou a coluna {colors('blue', column)} na tabela {colors('blue', table_name)}")
                                continue

                            check_lines(srv.conn, table=table, column=column)
                            print(colors("gold","=========="))
                        except:
                            print(f"\n{colors('red', 'ERRO:')} Não encontrou a tabela {colors('blue', table_name)} no banco de dados")
                            continue

                    elif opt == "05":
                        abort_system()

                    elif opt == "10":
                        print("")
                        srv.update_address("clini7", alias)

                    elif opt == "11":
                        print("")
                        srv.update_address("admini7", alias)
                except:
                        print(f"\nErro aon conectar no banco de dados {colors('gold', alias)}\n")
                        print(colors("gold","=========="))
                        continue

        else:

            alias = data_dict['content'][0]['Alias']
            user = data_dict['content'][0]['user_nameBD']
            password = urllib.parse.quote_plus(data_dict['content'][0]['PassWordBD'])
            host = data_dict['content'][0]['Server']
            port = data_dict['content'][0]['Porta']
            database = data_dict['content'][0]['Database']

            connect_string = f"{user}:{password}@{host}:{port}/{database}"

            print(f"conectando com o bando {colors('gold', alias)}", end="")
            try:
                srv = loading_dot(connect_string)
            except:
                print(f"Erro aon conectar no banco de dados {alias}")
                abort_system(False)

            srv.menu()

if __name__ == '__main__':
    start()