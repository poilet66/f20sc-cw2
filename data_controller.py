import pandas as pd
import re
from typing import Optional

import graphviz
from PIL import Image
import io
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller import Controller


class DataController:
    def __init__(self) -> None:

        self.file_path: Optional[str] = None
        self.df = None
        self.global_toggled = True

        self.user_uuid: Optional[str] = None
        self.document_uuid: Optional[str] = None

    def has_file(self) -> bool:
        return self.file_path is not None

    def register_controller(self, controller: "Controller") -> None:
        self.controller = controller

    def change_file(self, file_path) -> None:
        self.file_path = file_path
        self.df = self.path_to_pd(file_path)

    def set_document_filter(self, document_uuid: str) -> None:
        self.document_uuid = document_uuid

    def set_user_filter(self, user_uuid: str) -> None:
        self.user_uuid = user_uuid

    def path_to_pd(self, file_path: str) -> pd.DataFrame:
        
        df_all = pd.DataFrame()

        for chunk in pd.read_json(file_path, lines=True, chunksize=1000000):
            df_all = pd.concat([df_all, chunk], ignore_index=True)

        return df_all

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

    def top_browsers(self, verbose) -> pd.DataFrame:
        """
        Return top browsers, set verbose = False for grouping by browser agent (e.g.: All mozilla entries in one group)
        """
        working_df = self.df
        column = 'visitor_useragent' if verbose else 'visitor_useragent_grouped'

        # Filter by searched document if needed
        if not self.global_toggled and self.document_uuid is not None:
            working_df = working_df[working_df['env_doc_id'] == self.document_uuid]

        # add grouped browser name if needed
        if not verbose:
            working_df['visitor_useragent_grouped'] = working_df['visitor_useragent'].apply(self.group_browser)

        return (
            working_df[column]
            .value_counts()
            .reset_index()
        )
    
    def group_browser(self, name: str) -> str:
        """
        Provide input verbose browser name, get grouped name as return
        """
        pattern = r'^([^/]+)'
        matched = re.search(pattern, name)

        if matched:
            return matched.group(1)
        else:
            return "Unknown"

    def get_test_graph(self) -> graphviz.Digraph:
        graph = graphviz.Digraph()

        graph.attr(rankdir='LR')

        graph.node('A', 'Node A', style='filled', fillcolor='green')
        graph.node('B', 'Node B')
        graph.node('C', 'Node C')

        graph.edge('A', 'B', style='filled', fillcolor='green')
        graph.edge('B', 'C')
        graph.edge('C', 'A')

        return graph
    
    def image_from_graph(self, graph: graphviz.Digraph) -> np.ndarray:
        png = graph.pipe(format='png')
        image = Image.open(io.BytesIO(png))

        return np.array(image)
    
    def top_k_readers(self, k) -> pd.DataFrame:
        working_df = self.df.copy() # make sure to avoid ref bugs

        if not self.global_toggled and self.document_uuid is not None:
            working_df = working_df[working_df['env_doc_id'] == self.document_uuid]

        """
        To track the duration of the reading session the read time events are transmitted at increasing time intervals starting after 2 seconds. 
        The readtime field in the event indicates the time in milliseconds elapsed since last event. 

        This means that we need to use the 'pagereadtime' event. We can sum these to get a user's read time for a document. However, we must also remember
        to add 2000 milliseconds (2 seconds) to each sum, to account for the time elapsed before the first event
        """

        # filter to only 'pagereadtime' events
        working_df = working_df[working_df['event_type'] == 'pagereadtime']

        # convert readtime from millis to seconds
        working_df['read_time_seconds'] = working_df['event_readtime'] / 1000

        # group by user/doc reading, sum read time once grouped
        reader_times = working_df.groupby(['visitor_uuid', 'env_doc_id'])['read_time_seconds'].sum().reset_index()

        # Only display last 4 chars of each user id
        reader_times['visitor_uuid'] = reader_times['visitor_uuid'].str[-4:]

        # account for initial 2 seconds
        reader_times['read_time_seconds'] += 2

        return (
            reader_times[['visitor_uuid', 'read_time_seconds']]
            .sort_values('read_time_seconds', ascending=False)
            .head(k)
            .round() # round to whole numbers
        )
