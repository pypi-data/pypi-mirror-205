from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import MetaData
from sqlalchemy import inspect
from sqlalchemy import text
import fdb

                      
class Conn():
    def __init__(self, connect_string, **kwargs):

        connect_string = connect_string#"?charset=ANSI_CHARSET"
        self.connect_string = connect_string
        


    def __conn(self):

        fdb.load_api(fb_library_name="fbclient.dll")

        try:
            return create_engine(self.connect_string, pool_size=20, max_overflow=0, echo=False)
        
        except Exception as e:
            raise(e)

    def engine(self):
        return self.__conn()
    
    def session_maker(self):
        
        Session = sessionmaker(bind=self.__conn())
        session = Session()
        return session
    
    def session(self):
        session = Session(self.__conn())
        return session

    def metadata(self):
        metadata_obj = MetaData()
        return metadata_obj
    
    def metadata_all_table(self, schema=""):
        metadata_obj = MetaData(schema=schema)
        metadata_obj.reflect(self.__conn())
        return metadata_obj
    
    def inspect(self):
        insp = inspect(self.__conn())
        return insp
    
    def get_table(self, table_name, columns="*"):
        
        if type(columns) == list:
            cols = ""
            for c in columns:
                if c == columns[-1]:
                    cols += f"{c}"
                else:
                    cols += f"{c}, "
        else:
            cols = columns

        with self.__conn().begin() as connection:
            result = connection.execute(text(f"select {cols} from {table_name}") )

            return result

        