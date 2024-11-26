import pandas as pd

class DataController:
    def __init__(self) -> None:
        self.file_path = None
        self.df = None

    def change_file(self, file_path) -> None:
        self.file_path = file_path
        self.df = self.path_to_pd(file_path)

    def path_to_pd(self, file_path) -> pd.DataFrame:
        
        df =  pd.read_json(file_path, lines=True)
        print(df.dtypes)

        return df

    def top_k_countries(self) -> pd.DataFrame:
        """
        Return df of top k countries and their viewage
        """
        raise Exception('no impl')