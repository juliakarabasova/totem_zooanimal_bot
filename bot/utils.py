import random
import logging
import pandas as pd     # пока сделаем бд на csv (xlsx проще расширять), можно также на sqlite сделать


logging.basicConfig(filename='totem_animal_bot.log', encoding='utf-8', level=logging.INFO, filemode='a',
                    format="%(name)s %(levelname)s [%(asctime)s] %(message)s")

try:
    # db = pd.read_csv('totem_animals_db.csv', encoding='utf-8', sep=';')
    db = pd.read_excel('../data/totem_animals_db.xlsx')
    # qs = pd.read_csv('questions_db.csv', encoding='utf-8', sep=';')
    qs = pd.read_excel('../data/questions_db.xlsx')
except:
    logging.exception(f'Exception while reading base files: ')
    db = pd.DataFrame()
    qs = pd.DataFrame()


def get_number_questions():
    try:
        return len([q for q in db.columns if q.startswith('Q')])
    except:
        logging.exception(f'Exception while get_number_questions(): ')
        return 0


def get_options(i):
    try:
        return sorted(qs.loc[qs['Q_number'] == f'Q{i}'].filter(regex='^option').values[0])
    except:
        logging.exception(f'Exception while get_options(): ')
        return []


def get_question_text(i):
    try:
        return qs[qs['Q_number'] == f'Q{i}']['Q_Text'].tolist()[0]
    except:
        logging.exception(f'Exception while get_question_text(): ')
        return ''


def get_winner(answers):
    try:
        animals_to_answers = [sum([row[q] == ans for q, ans in answers.items()]) for i, row in db.iterrows()]
        win_ind = random.choice([i for i in range(len(animals_to_answers)) if animals_to_answers[i] == max(animals_to_answers)])
        win = db.iloc[win_ind]

        return [win_ind + 1] + win[['animal', 'link', 'description']].tolist()
    except:
        logging.exception(f'Exception while get_winner(): ')
        return []
