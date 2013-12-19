#coding:utf-8
# Поиск хэдеров, для которых нет текстов.
import codecs
import os
TXT_DIR_PATH = 'C:\LTC\\texts'
#TXT_DIR_PATH = 'C:\GitHub\\LTC_statistics\\test_texts'

def get_pairs(directory):
    head_files = []
    txt_files = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if not os.path.isdir(file_path):
            parts = file_name.split('.')
        if len(parts) >= 2:
            file_id = parts[0]
            file_type = parts[1]
            if file_type == "head":
                head_files.append(file_id)
            elif file_type == "txt":
               txt_files.append(file_id)
    return head_files, txt_files


def compare_names(head_files, txt_files):
    head_set = set(head_files)
    txt_set = set(txt_files)
    without_txt = head_set.difference(txt_set)
    without_head = txt_set.difference(head_set)
    return without_head, without_txt

def count_average(directory):
    translations = set()
    sources = {}

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if not os.path.isdir(file_path):
            parts = file_name.split('.')
        if len(parts) >= 2:
            file_type = parts[1]
            file_id = parts[0]
            if file_type == "head":
                with codecs.open(file_path, "r", encoding='utf-8') as f:
                    for num, line in enumerate(f):
                        line = line.strip()
                        if num == 8:
                            if line == "Source":
                                sources[file_id] = set()
                            if line == "Translation":
                                translations.add(file_id)
    for item in translations:
        parts = item.split(u"_")
        if len(parts) == 3:
            print "Warning. Bad translation path:", item
            sup_key = item
        elif len(parts) == 4:
            r_index = item.rfind(u"_")
            sup_key = item[:r_index]
        else:
            print "Error. Bad translation path:", item
            continue

        if sup_key.startswith("EN"):
            sup_key = sup_key.replace("EN", "RU")
        elif sup_key.startswith("RU"):
            sup_key = sup_key.replace("RU", "EN")
        else:
            print "Error. Bad translation lang:", item
            continue

        sources[sup_key].add(item)

    en_sources = {}
    ru_sources = {}
    for key, translations in sources.iteritems():
        if key.startswith("EN"):
            en_sources[key] = len(translations)
        elif key.startswith("RU"):
            ru_sources[key] = len(translations)

    print "Translations for EN", sum(en_sources.values()) / float(len(en_sources))
    print "Translations for RU", sum(ru_sources.values()) / float(len(ru_sources))




if __name__ == "__main__":
    #head_files, txt_files = get_pairs(TXT_DIR_PATH)
    #without_head, without_txt = compare_names(head_files, txt_files)
    # print "Txt without head: "
    # for el in without_head:
    #     print el
    # print "Overall: ", len(without_head)
    # print "Head without txt: "
    # for el in without_txt:
    #     print el
    # print "Overall: ", len(without_txt)
    count_average(TXT_DIR_PATH)



