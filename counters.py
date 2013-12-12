#coding:utf-8
from collections import Counter
import re
import logging
logger = logging.getLogger("counters_logger")


class HeadFilesLangCounter(object):
    """счетчик для всех head-файлов одного языка"""
    def __init__(self, lang):
        self.lang = lang
        self.count = 0
        self.source_count = 0
        self.translation_count = 0


    def update(self, file_info):
        if file_info and file_info.lang == self.lang:
            self.count += 1
            if file_info.type == "Source":
                self.source_count += 1
            elif file_info.type == "Translation":
                self.translation_count += 1
            else:
                logger.warning(u"Unknown file type '%s' in file %s", file_info.type, file_info.filename)

    def __str__(self):
        return "Counter for language '%s':\nsource = %s\ntranslation = %s\ntotal = %s" % (
            self.lang, self.source_count, self.translation_count, self.count)


class MetaCounter(object):
    """счетчик для всей мета-информации"""
    def __init__(self, allowed_values, meta_inf):
        self.meta_inf = meta_inf
        self.meta_counters = {}.fromkeys(allowed_values, 0)

    def update(self, file_info):
        if file_info:
            meta_inf_value = getattr(file_info, self.meta_inf) or "None"
            if meta_inf_value in self.meta_counters:
                self.meta_counters[meta_inf_value] += 1
            else:
                logger.warning(u"Unknown value '%s' for %s in file %s",  meta_inf_value, self.meta_inf, file_info.filename)

    def __str__(self):
        return "Counter for '%s':\n '%s'" % (self.meta_inf, self.meta_counters)


class TranslationMetaCounter(MetaCounter):
    """счетчик для файлов-переводов"""
    def update(self, file_info):
        if file_info and file_info.type == "Translation":
            meta_inf_value = getattr(file_info, self.meta_inf) or "None"
            if meta_inf_value in self.meta_counters:
                self.meta_counters[meta_inf_value] += 1
            else:
                #if self.meta_inf == "gender":
                    #import pdb; pdb.set_trace()
                logger.warning(u"Unknown value '%s'(%s) for %s in file %s",
                               meta_inf_value, repr(meta_inf_value), self.meta_inf, file_info.filename)


class CommonCounter(object):
    """счетчик, собирающий все значения из метаданных, без проверок"""
    def __init__(self, meta_inf):
        self.counter = Counter()
        self.meta_inf = meta_inf

    def update(self, file_info):
        if file_info:
            meta_inf_value = getattr(file_info, self.meta_inf) or "None"
            self.counter[meta_inf_value] += 1

    def __str__(self):
        return "Counter for %s:\n '%s'" % (self.meta_inf, self.counter)


class YearCounter(CommonCounter):
    """счетчик для года"""
    def __init__(self):
        super(YearCounter, self).__init__("year")

    def update(self, file_info):
        if file_info and file_info.year:
            if re.match('\d{4}', file_info.year):
                self.counter[file_info.year] += 1
            else:
                logger.warning(u"Unknown value '%s' for %s in file %s", file_info.year, self.meta_inf, file_info.filename)








        


