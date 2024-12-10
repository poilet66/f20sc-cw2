pyinstaller --hidden-import PIL._tkinter_finder --hidden-import tkinter -F --paths venv  --clean main.py

./dist/main

