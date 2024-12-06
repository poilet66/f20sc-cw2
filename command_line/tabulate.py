import os
import pandas as pd

def print_bar(df: pd.DataFrame, category_col: str, value_col: str):
    max_width = int(os.get_terminal_size().columns)
    max_col_width = max_width // 2

    cat_items = df[category_col]
    val_items = df[value_col]

    # find the max width for title and all elements in df
    cat_width = max(len(category_col), *map(lambda x: len(str(x)[:max_col_width]), cat_items)) + 1
    val_width = max(len(value_col), *map(lambda x: len(str(x)[:max_col_width]), val_items)) + 1
    
    max_value = val_items.max()
    scale: float = (max_width - (cat_width + val_width)) / max_value

    cat_title_spacing = cat_width - len(category_col)
    val_title_spacing = val_width - len(value_col)

    print(f"{category_col}{' ' * cat_title_spacing}{value_col}{' ' * val_title_spacing} Chart")

    print("-" * max_width)

    for _, row in df.iterrows():

        category_str = str(row[category_col])[:max_col_width]
        value: int = row[value_col]
        value_str = str(value)[:max_col_width]

        cat_item_width = cat_width - len(category_str)
        val_item_width = val_width - len(value_str)

        bar = "█" * int(value * scale)  # Scale the bar length
        print(f"{category_str}{' ' * cat_item_width}{value_str}{' ' * val_item_width}{bar}")
