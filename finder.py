#coding:utf-8
# Поиск хэдеров, для которых нет текстов.
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

if __name__ == "__main__":
    head_files, txt_files = get_pairs(TXT_DIR_PATH)
    without_head, without_txt = compare_names(head_files, txt_files)
    print "Txt without head: ", without_head, "Overall: ", len(without_head)
    print "Head without txt: ", without_txt, "Overall: ", len(without_txt)


