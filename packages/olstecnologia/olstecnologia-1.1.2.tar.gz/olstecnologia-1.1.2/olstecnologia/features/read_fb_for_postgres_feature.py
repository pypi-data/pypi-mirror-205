from sqlalchemy import Table, select, update, bindparam, MetaData
from olstecnologia.services.utils_service import colors, abort_system, get_ibges
import os

def get_data_in_fb(table, conn):
    metadata_fdb = MetaData()

def insert_data_in_fb(table, conn):
    metadata_post = MetaData()


def population_postgres(conn):
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors("gold", "====== LENDO DADOS DO ")+colors("green", "FIREBIRD ")+ colors("gold", "E COLOCANDO NO ")+colors("green", "POSTGRES ")+ colors("gold", "======"))
        print("")

        