import argparse
import re
class ArgTypes:
    @staticmethod
    def task_type(value: str):
        if value not in ["2a", "2b", "3a", "3b", "4", "5d", "6", "7"]:
            raise argparse.ArgumentTypeError(f"Invalid task: {value}")
        return value

    @staticmethod
    def user_uuid_type(value: str):
        pattern = r"^[a-z0-9]{16}$"
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid user uuid: {value}")
        return value

    @staticmethod
    def doc_uuid_type(value: str):
        # TODO
        pattern = r"^.*$"
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid doc uuid: {value}")
        return value

    @staticmethod
    def file_name_type(value: str):
        # TODO
        pattern = r"^.*$"
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid file name: {value}")
        return value

