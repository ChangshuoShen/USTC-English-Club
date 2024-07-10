
import pandas as pd
def import_riddles(path_to_csv_file, Riddle):
    df = pd.read_csv(path_to_csv_file)
    for _, row in df.iterrows():
        Riddle.create_riddle(
            main_category=row['main_category'],
            riddle_text=row['riddle_text'],
            answer=row['Answer'],
            difficulty=row['Difficulty']
        )
    print('data importted successfully')