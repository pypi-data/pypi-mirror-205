from sqlalchemy import Table, select, update, bindparam, MetaData
from olstecnologia.services.utils_service import colors, abort_system, get_ibges
from olstecnologia.services.check_db_service import check_tables, check_lines
import os
from tqdm import tqdm

def update_address_clini7(conn, dbs=""):
        
        if dbs == "":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== ATUALIZAÇÃO ENDEREÇOS DO ")+colors("green", "CLINI7 ")+ colors("gold", "======"))
            print("")

        metadata_obj = MetaData()
        
        tpaciente = Table("tpaciente", metadata_obj, autoload_with=conn[0])
        tlogradouro = Table("tlogradouro", metadata_obj, autoload_with=conn[0])
        trua = Table("trua", metadata_obj, autoload_with=conn[0])
        tbairro = Table("tbairro", metadata_obj, autoload_with=conn[0])
        tcidade = Table("tcidade", metadata_obj, autoload_with=conn[0])

        query_meta = select(
            tpaciente.c.id,
            (tlogradouro.c.descricao+" "+trua.c.rua).label("endereco"),
            trua.c.cep, tbairro.c.bairro, tcidade.c.cidade.label("municipio"),
            tcidade.c.estado.label("uf"),
            tcidade.c.ibge.label("codmunicipioibge")
                )\
                    .join(tpaciente, tpaciente.c.rua == trua.c.id)\
                        .join(tlogradouro, tlogradouro.c.id == trua.c.logradouro)\
                            .join(tbairro, tbairro.c.id == trua.c.bairro)\
                                .join(tcidade, tcidade.c.id == tbairro.c.cidade)

        with conn[0].connect() as s:
            try:
                data = s.execute(query_meta).all()
                
                stmt = update(tpaciente)\
                    .where(tpaciente.c.id == bindparam('ids'))\
                        .values(cep=bindparam("cep"),
                                endereco=bindparam("endereco"),
                                bairro=bindparam("bairro"),
                                codmunicipioibge=bindparam("codmunicipioibge"),
                                municipio=bindparam("municipio"),
                                uf=bindparam("uf"))
                
                for i in tqdm(range(len(data)), desc =f"Atualizando => "):
                    s.execute(stmt,
                                 ids=data[i][0],
                                 endereco=data[i][1],
                                 bairro=data[i][3],
                                 codmunicipioibge=data[i][6],
                                 municipio=data[i][4],
                                 uf=data[i][5],
                                 cep=data[i][2]
                                 )
                
                if dbs:
                    print("")
                    print(colors('green', f'Atualização do banco ') + colors("gold", dbs) + colors("green", " finalizada com sucesso"))
                    print("")
                else:
                    print("")
                    print(colors("green", "Atualização finalizada com sucesso"))
                    abort_system(False)
            
            except Exception as e:
                print(colors("red", "Foram encontrado alguns erros foram encontrados!"))
                print("")
                _, errors_found = check_tables(conn, tables = [tpaciente, tlogradouro, trua, tbairro, tcidade], mode="p")
                
                print("")
                if not dbs == "":
                    opt = input("Quer saber quais linhas estão com erro "+ colors("gold","pode ser demorado!")+"? (s/N): ")

                    if opt.lower() == "s":

                        for x in errors_found:
                            table = x[0]
                            
                            for col in x[1]:
                                column = table.columns[col]

                                check_lines(conn=conn, table=table, column=column)

                    else:
                        
                        print("")
                        print(colors("green", "Obrigado por usar o sistema."))
                        abort_system(False)

def update_address_admini7(conn, dbs=""):
        
        if dbs == "":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(colors("gold", "====== ATUALIZAÇÃO ENDEREÇOS DO ")+colors("green", "ADMINI7 ")+ colors("gold", "======"))
            print("")

        metadata_obj = MetaData()
        
        pessoa_endereco = Table("pessoa_endereco", metadata_obj, autoload_with=conn[0])
        rua = Table("rua", metadata_obj, autoload_with=conn[0])
        bairro = Table("bairro", metadata_obj, autoload_with=conn[0])
        cidade = Table("cidade", metadata_obj, autoload_with=conn[0])
        logradouro = Table("logradouro", metadata_obj, autoload_with=conn[0])

        query_meta = select(
            pessoa_endereco.c.id_endereco,
            (logradouro.c.descricao+" "+rua.c.rua).label("endereco"),
            rua.c.cep, bairro.c.bairro, cidade.c.cidade.label("municipio"),
            cidade.c.uf.label("uf")
                )\
                    .join(pessoa_endereco, pessoa_endereco.c.id_rua == rua.c.id_rua)\
                        .join(logradouro, logradouro.c.id_logradouro == rua.c.id_logradouro)\
                            .join(bairro, bairro.c.id_bairro == rua.c.id_bairro)\
                                .join(cidade, cidade.c.id_cidade == bairro.c.id_cidade)

        
        with conn[0].connect() as s:
            try:
                data = s.execute(query_meta).all()
                
                stmt = update(pessoa_endereco)\
                    .where(pessoa_endereco.c.id_endereco == bindparam('ids'))\
                        .values(cep=bindparam("cep"),
                                logradouro=bindparam("logradouro"),
                                bairro=bindparam("bairro"),
                                cidade=bindparam("cidade"),
                                uf=bindparam("uf"))

                
                for i in tqdm(range(len(data)), desc =f"Atualizando => "):
                    s.execute(stmt,
                                 ids=data[i][0],
                                 logradouro=data[i][1],
                                 bairro=data[i][3],
                                 cidade=data[i][4],
                                 uf=data[i][5],
                                 cep=data[i][2]
                                 )

                if dbs =="":   
                    print('O banco foi atualizado.')
                    opt = input("Quer que consulta API Externa e atualiza os códigos IBGE? (Pode ser demorado.) (s/N): ")
                    if opt.lower() == 's':
                        
                        ibges = [x[2] for x in data]
                        cods_ibge = get_ibges(ibges)

                        stmt_ibge = update(pessoa_endereco)\
                        .where(pessoa_endereco.c.id_endereco == bindparam('ids')).values(codibge=bindparam("codibge"))

                        for i in tqdm(range(len(data)), desc =f"Atualizando o Cód. IBGE => "):
                            s.execute(stmt_ibge, ids=data[i][0], codibge=cods_ibge[i])

                    print("")
                    print(colors("green", "Atualização finalizada com sucesso"))
                    abort_system(False)
                else:
                    print("")
                    print(colors('green', f'Atualização do banco ') + colors("gold", dbs) + colors("green", " finalizada com sucesso"))
                    print("")
            except:
                print(colors("red", "Foram encontrado alguns erros foram encontrados!"))
                print("")
                _, errors_found = check_tables(conn, tables = [pessoa_endereco, logradouro, rua, bairro, cidade], mode="p")
                
                print("")

                if dbs =="":
                    opt = input("Quer saber quais linhas estão com erro "+ colors("gold","pode ser demorado!")+"? (s/N): ")

                    if opt.lower() == "s":

                        for x in errors_found:
                            table = x[0]
                            
                            for col in x[1]:
                                column = table.columns[col]

                                check_lines(conn=conn, table=table, column=column)

                    else:
                        print(colors("green", "Obrigado por usar o sistema."))
                        abort_system(False)
                 



