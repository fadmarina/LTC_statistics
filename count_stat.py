#coding:utf-8
#DO TO  и все такое:
# 1.Статистика по дублям (TUVs с идентичным текстом и метаданными).
# 2.Количество текстов и токенов с разбивкой "русский-английский" и "оригиналы-переводы"
# 3.Количество текстов разных жанров
# 5. статистика по всем метаданным, которые есть в корпусе (возраст, университет и т.п.)
import codecs
import os
import logging
import re

from counters import HeadFilesLangCounter, TranslationMetaCounter, TokensCounter
from counters import MetaCounter
from counters import CommonCounter
from counters import YearCounter

TXT_DIR_PATH = 'C:\LTC\\texts'
#TXT_DIR_PATH = 'C:\GitHub\\LTC_statistics\\test_texts'

class SimpleFileInfo(object):
    def __init__(self, file_path, file_lang):
        self.lang = file_lang
        self.file_path = file_path

class HeadFileInfo(object):
    def __init__(self, filename):
        self.gender = None
        self.course = None
        self.state = None
        self.genre = None
        self.stress = None
        self.place = None
        self.year = None
        self.type = None
        self.uni = None
        self.lang = None
        self.filename = filename


def get_head_file_info(filename, file_lang):
    info = HeadFileInfo(filename)
    info.lang = file_lang if file_lang in ("EN", "RU") else None

    with codecs.open(filename, "r", encoding='utf-8') as f:
        for num, line in enumerate(f):
            line = line.strip()
            if num == 0:
                info.gender = line
            elif num == 1:
                info.course = line
            elif num == 2:
                info.mark = line
            elif num == 3:
                info.state = line
            elif num == 4:
                info.genre = line
            elif num == 5:
                info.stress = line
            elif num == 6:
                info.place = line
            elif num == 7:
                info.year = line
            elif num == 8:
                if line in ("Translation", "Source"):
                    info.type = line
            elif num == 9:
                info.uni = line
    return info


def get_file_info(file_name, file_path):
    parts = file_name.split('.')
    if len(parts) >= 2:
        file_type = parts[1]
        file_lang = parts[0][:2]
        if file_type == "head":
            info = get_head_file_info(file_path, file_lang)
            if info.type is None or info.lang is None:
                logger.error(u"There is no lang or type parameter in '%s' head file", file_path)
                return None
            else:
                return info
        elif parts[1] == "txt":
            return SimpleFileInfo(file_path, file_lang)
    return None


def get_all_headers(directory):
    ru_headcounter = HeadFilesLangCounter("RU")
    en_headcounter = HeadFilesLangCounter("EN")

    gender_values = ["M","F","None"]
    gender = TranslationMetaCounter(gender_values, "gender")

    course = CommonCounter("course")

    mark_values = ['1', '2', '3', '4', '5', "None"]
    mark = TranslationMetaCounter(mark_values, "mark")

    state_values = ["Final", "Draft", "None"]
    state = TranslationMetaCounter(state_values,"state")

    genre_values = ["Academic", "Informational", "Essay", "Interview", "Tech",
                    "Fiction", "Educational", "Encyclopaedia", "Speech", "Letters",
                    "Advertisement", "Review", "None"]
    genre = MetaCounter(genre_values, "genre")

    stress_values = ["Routine", "Exam", "Contest", "None"]
    stress = TranslationMetaCounter(stress_values, "stress")

    place_values = ["Home", "Classroom", "None"]
    place = TranslationMetaCounter(place_values, "place")

    year = YearCounter()
    uni = CommonCounter("uni")
    token_counter = TokensCounter()

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if not os.path.isdir(file_path):
            file_info = get_file_info(file_name, file_path)
            if isinstance(file_info, HeadFileInfo):
                ru_headcounter.update(file_info)
                en_headcounter.update(file_info)
                gender.update(file_info)
                course.update(file_info)
                mark.update(file_info)
                state.update(file_info)
                genre.update(file_info)
                stress.update(file_info)
                place.update(file_info)
                year.update(file_info)
                uni.update(file_info)
            elif isinstance(file_info, SimpleFileInfo):
                token_counter.update(file_info)

    return ru_headcounter, en_headcounter, gender, course, mark, state, genre, stress, place, year, uni, token_counter


def get_page_html(counters):
    html = u"""
    <html>
    <head><title>Статистика</title></head>
    <body>
        %s
    </body>
    <html>
    """ % u'\n'.join([cnt.html() for cnt in counters])
    with open("stat.html", "w") as page:
        page.write(html.encode('utf8'))


#количество текстов на русском языке
#количество текстов на английском языке

#/var/www/texts - path to txts

#количество английских оригиналов и переводов
#количество русских оригиналов и переводов

if __name__ == "__main__":
    FORMAT = '%(levelname)s::%(asctime)s::%(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='log/count_stat.log')
    logger = logging.getLogger("stat_logger")
    counters = get_all_headers(TXT_DIR_PATH)
    get_page_html(counters)
    print "END"
    #ru, en, gender, course, mark, state, genre, stress, place, year, uni, tokens = get_all_headers(TXT_DIR_PATH)
    # print ru
    # print en
    # print gender
    # print course
    # print mark
    # print state
    # print genre
    # print stress
    # print place
    # print year
    # print uni
    # # count_tokens('C:\GitHub\\LTC_statistics\\test_texts\\RU_1_1_2.txt', "RU")
    # print tokens
