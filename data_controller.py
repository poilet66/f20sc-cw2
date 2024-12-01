import pandas as pd
from typing import Optional

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import Controller


class DataController:
    def __init__(self) -> None:

        self.file_path: Optional[str] = None
        self.df = None
        self.document_uuid = None
        self.global_toggled = True

    def has_file(self) -> bool:
        return self.file_path is not None

    def register_controller(self, controller: "Controller") -> None:
        self.controller = controller

    def change_file(self, file_path) -> None:
        self.file_path = file_path
        self.df = self.path_to_pd(file_path)

    def set_document_filter(self, document_uuid) -> None:
        self.document_uuid = document_uuid

    def path_to_pd(self, file_path) -> pd.DataFrame:
        
        df =  pd.read_json(file_path, lines=True)

        return df

    def top_k_countries(self, k: int) -> pd.DataFrame:
        """
        Return df of top k countries and their viewage
        """
        working_df = self.df

        # If we're not in global mode and valid uuid is provided
        if not self.global_toggled and self.document_uuid is not None:

            working_df = working_df[working_df['env_doc_id'] == self.document_uuid] # TODO: Add check here to ensure doc exists?

        return (
            working_df['visitor_country']
            .value_counts()
            .head(k)
            .reset_index()
        )
    
    def top_continents(self) -> pd.DataFrame:
        """
        Return top k continents and their viewage
        """
        working_df = self.df
        continent_df = pd.read_csv('data/continents.csv')

        if not self.global_toggled and self.document_uuid is not None:
            working_df = working_df[working_df['env_doc_id'] == self.document_uuid]

        working_df = working_df.merge(continent_df, on="visitor_country", how="left")

        return (
            working_df['visitor_continent']
            .value_counts()
            .reset_index()
        )

    def top_browsers(self, verbose = True) -> pd.DataFrame:
        """
        Return top browsers, set verbose = False for grouping by browser agent (e.g.: All mozilla entries in one group)
        """
        working_df = self.df

        # Filter by searched document if needed
        if not self.global_toggled and self.document_uuid is not None:
            working_df = working_df[working_df['env_doc_id'] == self.document_uuid]

        return (
            working_df["visitor_useragent"]
            .value_counts()
            .reset_index()
        )
