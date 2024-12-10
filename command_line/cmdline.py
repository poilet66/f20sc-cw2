import argparse
import data_controller
from command_line.arg_types import ArgTypes
from command_line.tabulate import print_bar
from command_line.graph_view import GraphWindow


class CommandLineHandler:
    def __init__(self):

        self.parser = argparse.ArgumentParser(description="")
        self.add_args()

        self.args = vars(self.parser.parse_args())
        self.data_controller = data_controller.DataController()

    def add_args(self) -> None:
        self.parser.add_argument("-u", type=ArgTypes.user_uuid_type, required=False, help="The uuid to search for")
        self.parser.add_argument("-d", type=ArgTypes.doc_uuid_type, required=False, help="The doc UUID")
        self.parser.add_argument("-t", type=ArgTypes.task_type, required=False, help="The task number to run")
        self.parser.add_argument("-f", type=ArgTypes.file_name_type, required=False, help="The data file path/name")

    def has_args(self) -> bool:
        return self.args["t"] is not None

    def run(self):
        if self.args["f"] is None:
            raise argparse.ArgumentError(None, "Missing file argument")

        def on_load(success: bool):
            if not success:
                raise FileNotFoundError()
        self.data_controller.change_file(self.args["f"], on_load)

        if self.args["d"] is not None:
            self.data_controller.set_document_filter(self.args["d"])

        if self.args["u"] is not None:
            self.data_controller.set_user_filter(self.args["u"])

        match self.args["t"]:
            case "2a":
                self.q2a()
            case "2b":
                self.q2b()
            case "3a":
                self.q3a()
            case "3b":
                self.q3b()
            case "4":
                self.q4()
            case "5d":
                self.q5d()
            case "6":
                self.q6()
            case _:
                raise Exception("Invalid Task")

    def q2a(self):
        df = self.data_controller.top_k_countries(10)
        print_bar(df, "visitor_country", "count")

    def q2b(self):
        df = self.data_controller.top_continents()
        print_bar(df, "visitor_continent", "count")

    def q3a(self):
        df = self.data_controller.top_browsers(True)
        print_bar(df, "visitor_useragent", "count")

    def q3b(self):
        df = self.data_controller.top_browsers(False)
        print_bar(df, "visitor_useragent_grouped", "count")

    def q4(self):
        df = self.data_controller.top_k_readers(10)
        print_bar(df, "visitor_uuid", "read_time_seconds")

    def q5d(self) -> None:
        if self.args["d"] is None:
            print('You must specify a document id')
            return
        if self.args["u"] is None:
            print('You must specify a user')
            return
        user_dict = self.data_controller.also_likes_data()
        print('List of also-liked documents:')
        count = 1
        for doc_list in user_dict.values():
            for doc in doc_list:
                print(f'{count}. {doc}')
                count += 1

    def q6(self) -> None:
        window = GraphWindow(self.data_controller)
