import pandas as pd

class DataController:
    def __init__(self) -> None:
        self.file_path = None
        self.df = None

    def change_file(self, file_path) -> None:
        self.file_path = file_path
        self.df = self.path_to_pd(file_path)

    def path_to_pd(self, file_path) -> pd.DataFrame:
        # To get past 'trailing data' issue (not all in one entry)
        data = []
        with open(file_path, encoding='utf-8', mode='r') as f:
            for line in f:
                data.append(line)


        df = pd.DataFrame(data)
        print(df.dtypes)
        return df

    def top_k_countries(self) -> pd.DataFrame:
        """
        Return df of top k countries and their viewage
        """
        raise Exception('no impl')