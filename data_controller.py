import pandas as pd

class DataController:
    def __init__(self) -> None:
        self.file_path = None
        self.df = None
        self.document_uuid = None

    def change_file(self, file_path) -> None:
        self.file_path = file_path
        self.df = self.path_to_pd(file_path)

        self.top_k_countries(10)

    def set_document_filter(self, document_uuid) -> None:
        self.document_uuid = document_uuid

    def path_to_pd(self, file_path) -> pd.DataFrame:
        
        df =  pd.read_json(file_path, lines=True)
        print(df.dtypes)

        return df

    def top_k_countries(self, k: int) -> pd.DataFrame:
        """
        Return df of top k countries and their viewage
        """
        working_df = self.df # Use operations on this

        if self.document_uuid is not None:
            working_df = working_df[working_df['env-doc-id'] == self.document_uuid]


        ret = (
            working_df['visitor_country']
            .value_counts()
            .head(k)
            .reset_index()
        )

        print(ret)

        return ret
        