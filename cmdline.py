import argparse
import data_controller
import re


class ArgTypes:
    @staticmethod
    def task_type(value: str):
        if value not in ["2a", "2b", "3a", "3b", "4", "5d", "6", "7"]:
            raise argparse.ArgumentTypeError(f"Invalid task: {value}")
        return value

    @staticmethod
    def user_uuid_type(value: str):
        # TODO
        pattern = r"^.*$"
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid task: {value}")
        return value

    @staticmethod
    def doc_uuid_type(value: str):
        # TODO
        pattern = r"^.*$"
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid task: {value}")
        return value

    @staticmethod
    def file_name_type(value: str):
        # TODO
        pattern = r"^.*$"
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid task: {value}")
        return value


class CommandLineHandler:
    def __init__(self):

        self.parser = argparse.ArgumentParser(description="")
        self.add_args()

        self.args = vars(self.parser.parse_args())

    def add_args(self) -> None:
        self.parser.add_argument("-u", type=ArgTypes.user_uuid_type, required=False, help="The uuid to search for")
        self.parser.add_argument("-d", type=ArgTypes.doc_uuid_type, required=False, help="The doc UUID")
        self.parser.add_argument("-t", type=ArgTypes.task_type, required=False, help="The task number to run")
        self.parser.add_argument("-f", type=ArgTypes.file_name_type, required=False, help="The data file path/name")

    def has_args(self) -> bool:
        return self.args["t"] is not None

    def run(self):
        print("running in cmd mode")
