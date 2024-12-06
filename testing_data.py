from data_controller import DataController
from pathlib import Path

if __name__ == "__main__":
    path = Path('C:/Users/rohan/Downloads/sample_tiny.json')

    data_controller = DataController()

    data_controller.change_file(path)

    print(data_controller.top_k_documents(3, '3e92caf3e56ad750'))

