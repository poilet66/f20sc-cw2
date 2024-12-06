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

    def get_test_graph(self, user_id: str, doc_id: str) -> graphviz.Digraph:

        # current user, document

        # get K OTHER top users from same document

        # get their top L read documents exclude current doc

        working_df: pd.DataFrame = self.df.copy()

        working_df = working_df[working_df['env_doc_id'] == self.document_uuid]

        # Filter out search user when generating other user profiles
        top_other_readers = working_df[working_df['visitor_uuid'] != user_id]

        # Get top K other readers (we'll hardcode 4 for now)
        top_other_readers = self.top_k_readers(4 + 1, doc_id=doc_id)

        # filter out user if they happen to be in top readers, otherwise remove bottom reader
        if user_id in top_other_readers['visitor_uuid'].values:
            top_other_readers = top_other_readers[top_other_readers['visitor_uuid'] != user_id]
        else:
            top_other_readers = top_other_readers.head(3)

        print(f'other top reader length: {len(top_other_readers)}')

        users_top_docs = {}

        # iterate through readers
        for _, row in top_other_readers.iterrows():
            print(f'getting top docs for user: {row["visitor_uuid"]}')
            # get top documents for user
            user_top_docs = self.top_k_documents(4, row['visitor_uuid'])
            
            # Check if doc_id present
            if doc_id in user_top_docs['env_doc_id'].values:
                user_top_docs = user_top_docs[user_top_docs['env_doc_id'] != doc_id]
            
            users_top_docs[row['visitor_uuid']] = user_top_docs.head(3)

        print(users_top_docs) 


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
    
    def top_k_readers(self, k, doc_id = None) -> pd.DataFrame:
        working_df = self.df.copy() # make sure to avoid ref bugs

        if doc_id is not None:
            working_df = working_df[working_df['visitor_uuid'] == doc_id]
        elif not self.global_toggled and self.document_uuid is not None:
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
    
    def top_k_documents(self, k, user_id) -> pd.DataFrame:
        """
        Get the top K document id's that user `user_id` has read
        """
        working_df: pd.DataFrame = self.df.copy()

        # filter to user
        working_df = working_df[working_df['visitor_uuid'] == user_id]
        
        # filter to only 'pagereadtime' events
        working_df = working_df[working_df['event_type'] == 'pagereadtime']
        
        # convert readtime from millis to seconds
        working_df['read_time_seconds'] = working_df['event_readtime'] / 1000
        
        # group by doc id, sum read time once grouped
        doc_times = working_df.groupby('env_doc_id')['read_time_seconds'].sum().reset_index()
        
        # account for initial 2 seconds
        doc_times['read_time_seconds'] += 2
        
        return (
            doc_times[['env_doc_id', 'read_time_seconds']]
            .sort_values('read_time_seconds', ascending=False)
            .head(k)
            .round()
        )