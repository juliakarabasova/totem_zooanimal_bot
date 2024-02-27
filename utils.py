import random

import pandas as pd     # пока сделаем бд на csv, можно также на sqlite сделать


db = pd.read_csv('totem_animals_db.csv', encoding='utf-8', sep=';')
# print(db.head())

qs = pd.read_csv('questions_db.csv', encoding='utf-8', sep=';')
# print(qs)


def get_number_questions():
    return len([q for q in db.columns if q.startswith('Q')])


def get_options(i):
    print(qs.loc[qs['Q_number'] == f'Q{i}'].filter(regex='^option').values[0])
    return sorted(qs.loc[qs['Q_number'] == f'Q{i}'].filter(regex='^option').values[0])


def get_question_text(i):
    return qs[qs['Q_number'] == f'Q{i}']['Q_Text'].tolist()[0]


def get_winner(answers):
    animals_to_answers = [sum([row[q] == ans for q, ans in answers.items()]) for i, row in db.iterrows()]
    win_ind = random.choice([i for i in range(len(animals_to_answers)) if animals_to_answers[i] == max(animals_to_answers)])
    win = db.iloc[win_ind]
    # print(win[['animal', 'link']].tolist())
    return [win_ind + 1] + win[['animal', 'link', 'description']].tolist()
