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
        self.data_controller = data_controller.DataController()

    def add_args(self) -> None:
        self.parser.add_argument("-u", type=ArgTypes.user_uuid_type, required=False, help="The uuid to search for")
        self.parser.add_argument("-d", type=ArgTypes.doc_uuid_type, required=False, help="The doc UUID")
        self.parser.add_argument("-t", type=ArgTypes.task_type, required=False, help="The task number to run")
        self.parser.add_argument("-f", type=ArgTypes.file_name_type, required=False, help="The data file path/name")

    def has_args(self) -> bool:
        return self.args["t"] is not None

    def run(self):

        self.data_controller.change_file(self.args["f"])

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
            case "7":
                self.q7()
            case _:
                raise Exception("Invalid Task")

    def q2a(self):
        df = self.data_controller.top_k_countries(10)
        print(df)

    def q2b(self):
        df = self.data_controller.top_continents()
        print(df)

    def q3a(self):
        df = self.data_controller.top_browsers(True)
        print(df)

    def q3b(self):
        df = self.data_controller.top_browsers(False)
        print(df)

    def q4(self):
        df = self.data_controller.top_k_readers(10)
        print(df)

    def q5d(self):
        raise NotImplementedError

    def q6(self):
        raise NotImplementedError

    def q7(self):
        raise NotImplementedError
