import pandas as pd
import redshift_connector

class RedshiftToDf:
    def __init__(self, database:str, user:str, password:str, host:str, port:int=5439):
        self.conn = redshift_connector.connect(
                                            database=database
                                            ,user = user
                                            ,password = password
                                            ,host=host
                                            ,port=port
                                        )

        self.cursor = self.conn.cursor()
        return None

    def create_df(self, sql:str, save_csv:bool=False, file_path:str='./df.csv') -> pd.DataFrame:
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        try:
            col = [x[0].decode('utf-8') for x in self.cursor.description]
        except AttributeError:
            col = [x[0] for x in self.cursor.description]
        frame = pd.DataFrame(result, columns=col)
        if save_csv:
            frame.to_csv(file_path,na_rep='NaN')
        return frame

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        print('Redshift connection is closed')
        return None
