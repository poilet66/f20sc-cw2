import pandas as pd
import re
from typing import Optional, Dict, List, Any, Callable

import graphviz
from graphviz.exceptions import ExecutableNotFound
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

        self.user_uuid: Optional[str] = None
        self.document_uuid: Optional[str] = None

    def has_file(self) -> bool:
        return self.file_path is not None

    def register_controller(self, controller: "Controller") -> None:
        self.controller = controller

    def change_file(self, file_path: str, callback: Optional[Callable[[bool], None]]) -> None:
        """change the file location, return true if successful"""
        self.file_path = file_path
        self.df = self.path_to_pd(file_path)
        if self.df is None:
            if callback:
                callback(False)
            return
        self.df = self.filter_data(self.df)
        if callback:
            callback(True)


    def filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        needed_types = ["pagereadtime", "pageread"]
        return df[df['event_type'].isin(needed_types)]

    def set_document_filter(self, document_uuid: str) -> None:
        if document_uuid == "": 
            self.document_uuid = None
            return
        self.document_uuid = document_uuid

    def set_user_filter(self, user_uuid: str) -> None:
        if user_uuid == "": 
            self.user_uuid = None
            return
        self.user_uuid = user_uuid

    def path_to_pd(self, file_path: str) -> Optional[pd.DataFrame]:
        
        df_all = pd.DataFrame()

        try:
            for chunk in pd.read_json(file_path, lines=True, chunksize=1000000):
                df_all = pd.concat([df_all, chunk], ignore_index=True)
            return df_all
        except UnicodeDecodeError:
            return None
        except ValueError:
            return None

    def top_k_countries(self, k: int) -> pd.DataFrame:
        """
        Return df of top k countries and their viewage
        """
        working_df = self.df

        # If a valid uuid is provided
        if self.document_uuid is not None:
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

        if self.document_uuid is not None:
            working_df = working_df[working_df['env_doc_id'] == self.document_uuid]

        working_df = working_df.merge(continent_df, on="visitor_country", how="left")

        return (
            working_df['visitor_continent']
            .value_counts()
            .reset_index()
        )

    def top_browsers(self, verbose: bool) -> pd.DataFrame:
        """
        Return top browsers, set verbose = False for grouping by browser agent (e.g.: All mozilla entries in one group)
        """
        working_df = self.df
        column = 'visitor_useragent' if verbose else 'visitor_useragent_grouped'

        # Filter by searched document if needed
        if self.document_uuid is not None:
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
        try:
            matched = re.search(pattern, name)
            if matched:
                return matched.group(1)

        except TypeError:
            pass
        return "Unknown"

    def also_likes_data(self) -> Optional[Dict[str, List[str]]]:

        working_df: pd.DataFrame = self.df.copy()

        if self.document_uuid is None:
            return None

        print(self.document_uuid, self.user_uuid)

        user_id = self.user_uuid
        doc_id = self.document_uuid


        # Filter out search user when generating other user profiles
        print(working_df.iloc[0]['visitor_uuid'])

        # remove search user, doc from these dfs so they wont be in the return of sub functions
        top_other_readers_df = working_df[working_df['visitor_uuid'] != user_id] if user_id is not None else working_df
        other_docs_df = working_df[working_df['env_doc_id'] != doc_id]

        # Get top K other readers (we'll hardcode 4 for now)
        top_other_readers = self.top_k_readers(4, doc_id=doc_id, df=top_other_readers_df)

        users_top_docs = {}

        # iterate through readers
        for _, row in top_other_readers.iterrows():
            print(f'getting top docs for user: {row["visitor_uuid"]}')
            # get top documents for user
            user_top_docs = self.top_k_documents(4, row['visitor_uuid'], df=other_docs_df)
            
            users_top_docs[row['visitor_uuid']] = list(user_top_docs['env_doc_id'])

        return users_top_docs
    
    def graph_from_data(self, data_dict: Dict[str, List[str]]) -> Optional[graphviz.Digraph]:
        graph = None
        try:
            graph = graphviz.Digraph()
        except ExecutableNotFound as e: # If graphviz not installed, return None
            return None

        if self.document_uuid is None:
            return None
        if self.user_uuid is None:
            return None

        graph.attr(rankdir='TB')

        graph.node(self.document_uuid, self.document_uuid[-4:], style='filled', fillcolor='green')
        graph.node(self.user_uuid, self.user_uuid[-4:], style='filled', fillcolor='green', shape='box')

        graph.edge(self.user_uuid, self.document_uuid, style='filled', fillcolor='green')

        for other_user_id in data_dict.keys():
            # create user node
            graph.node(other_user_id, other_user_id[-4:], shape='box')
            for other_user_doc in data_dict.get(other_user_id):
                # create user doc node and edge to it from user
                graph.node(other_user_doc, other_user_doc[-4:])
                graph.edge(other_user_id, self.document_uuid)
                graph.edge(other_user_id, other_user_doc)

        return graph
    
    def image_from_graph(self, graph: graphviz.Digraph) -> np.ndarray[Any, Any]:
        png = graph.pipe(format='png')
        image = Image.open(io.BytesIO(png))

        return np.array(image)
    
    def top_k_readers(self, k: int, doc_id: Optional[str] = None, df = None) -> pd.DataFrame:

        if df is None:
            working_df = self.df.copy() # make sure to avoid ref bugs
        else:
            working_df = df

        if doc_id is not None:
            working_df = working_df[working_df['env_doc_id'] == doc_id]
        elif self.document_uuid is not None:
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
        if df is None: reader_times['visitor_uuid'] = reader_times['visitor_uuid'].str[-4:] # TODO: Make this cleaner, currently just a workaround to not break this

        # account for initial 2 seconds
        reader_times['read_time_seconds'] += 2

        return (
            reader_times[['visitor_uuid', 'read_time_seconds']]
            .sort_values('read_time_seconds', ascending=False)
            .head(k)
            .round() # round to whole numbers
        )
    
    def top_k_documents(self, k, user_id, df = None) -> pd.DataFrame:
        """
        Get the top K document id's that user `user_id` has read
        """

        if df is None:
            working_df: pd.DataFrame = self.df.copy()
        else:
            working_df = df

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
