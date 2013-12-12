#coding:utf-8
#DO TO  и все такое:
# 1.Статистика по дублям (TUVs с идентичным текстом и метаданными).
# 2.Количество текстов и токенов с разбивкой "русский-английский" и "оригиналы-переводы"
# 3.Количество текстов разных жанров
# 4.среднее число переводов на один оригинал  для разных направлений перевода
# 5. статистика по всем метаданным, которые есть в корпусе (возраст, университет и т.п.)
import os
import logging

from counters import HeadFilesLangCounter, TranslationMetaCounter
from counters import MetaCounter

TMX_FILE = u'C:\LTC\\ru-en_01-01.tmx'
TXT_DIR_PATH = 'C:\LTC\\texts'

class HeadFileInfo(object):
    def __init__(self):
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


def get_head_file_info(filename, file_lang):
    info = HeadFileInfo()
    info.lang = file_lang if file_lang in ("EN", "RU") else None

    with open(filename, "r") as f:
        for num, line in enumerate(f):
            line = line.strip()
            #if line:
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
        if file_type == "head":
            file_lang = parts[0][:2]
            info = get_head_file_info(file_path, file_lang)
            if info.type is None or info.lang is None:
                logger.error("There is no lang or type parameter in '%s' head file", file_path)
                return None
            else:
                return info
    return None


def get_all_headers(directory):
    ru_headcounter = HeadFilesLangCounter("RU")
    en_headcounter = HeadFilesLangCounter("EN")

    gender_values = ["M","F","None"]
    gender = TranslationMetaCounter(gender_values, "gender")

    course_values = ['1f', '2f', '3f', '4f', '5f', '1p', '2p', '3p', '4p', '5p', '1nl', '2nl', '3nl', '4nl', '5nl']
    course = TranslationMetaCounter(course_values, "course")

    mark_values = ['1', '2', '3', '4', '5']
    mark = TranslationMetaCounter(mark_values, "mark")

    state_values = ["Final", "Draft"]
    state = TranslationMetaCounter(state_values,"state")

    genre_values = ["Academic", "Informational", "Essay", "Interview", "Tech", "Fiction", "Educational", "Encyclopaedia", "Speech", "Letters", "Advertisement", "Review", "None"]
    genre = MetaCounter(genre_values, "genre")

    stress_values = ["Routine", "Exam", "Contest"]
    stress = TranslationMetaCounter(stress_values, "stress")

    place_values = ["Home", "Classroom"]
    place = TranslationMetaCounter(place_values, "place")

    year_values = ["2007", "2008", "2009", "2010", "2011", "2012", "2013"]
    year = TranslationMetaCounter(year_values, "year")

    uni_values = ["TSU", "MSU", "UdSU", "MAirI", "PermSU", "LUNN", "KSU", "HSE", "SSU", "UlSTU"]
    uni  = TranslationMetaCounter(uni_values, "uni")

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if not os.path.isdir(file_path):
            file_info = get_file_info(file_name, file_path)
            ru_headcounter.update(file_info)
            en_headcounter.update(file_info)
            gender.meta_update(file_info)
            course.meta_update(file_info)
            mark.meta_update(file_info)
            state.meta_update(file_info)
            genre.meta_update(file_info)
            stress.meta_update(file_info)
            place.meta_update(file_info)
            year.meta_update(file_info)
            uni.meta_update(file_info)

    return ru_headcounter, en_headcounter, gender, course, mark, state, genre, stress, place, year, uni


#количество текстов на русском языке
#количество текстов на английском языке

#/var/www/texts - path to txts

#количество английских оригиналов и переводов
#количество русских оригиналов и переводов

if __name__ == "__main__":
    FORMAT = '%(levelname)s::%(asctime)s::%(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logger = logging.getLogger("stat_logger")
    ru, en, gender, course, mark, state, genre, stress, place, year, uni = get_all_headers(TXT_DIR_PATH)
    print ru
    print en
    print gender
    print course
    print mark
    print state
    print genre
    print stress
    print place
    print year
    print uni
