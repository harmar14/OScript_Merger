import os
import shutil
from MergeOScript import MergeOScript

SUBTAG_FOLDER_PATH = "\\files\\subtags\\"
OLD_FOLDER_NAME = "old"
NEW_FOLDER_NAME = "new"
MERGED_FOLDER_NAME = "merged"
EXPLANATION_FOLDER_NAME = "_explanation"

class MergeSubtag:
    
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def getSubtagPath(self):
        
        # Формирование путей к папкам для мерджа сабтегов.
        
        path_dict = dict.fromkeys(["old_path", "new_path", "merged_path"])
        
        path = os.path.abspath(__file__)
        path = '\\'.join(path.split('\\')[:-2]) + SUBTAG_FOLDER_PATH
        
        path_dict["old_path"] = f"{path}{OLD_FOLDER_NAME}\\"
        path_dict["new_path"] = f"{path}{NEW_FOLDER_NAME}\\"
        path_dict["merged_path"] = f"{path}{MERGED_FOLDER_NAME}\\"
        
        self.path = path_dict
        
        return self
    
    def checkFolders(self):
        
        # Формирование путей old, new, merge.
        
        self = self.getSubtagPath()
        
        # Проверка сформированных путей old и new.
        
        if not (os.path.isdir(self.path["old_path"])):
            self.ok = False
            self.errMsg = f"Неверный путь: {self.path['old_path']}"            
        
        if not (os.path.isdir(self.path["new_path"])):
            self.ok = False
            self.errMsg = f"Неверный путь: {self.path['new_path']}"
        
        # Папка merged изначально должна отсутствовать. Создается она сама и папка _explanation внутри нее.
        
        if not (os.path.isdir(self.path["merged_path"])):
            
            try:
                os.mkdir(self.path["merged_path"])
            except Exception as e:
                self.ok = False
                self.errMsg = e
            try:
                os.mkdir(f"{self.path['merged_path']}{EXPLANATION_FOLDER_NAME}\\")
            except Exception as e:
                self.ok = False
                self.errMsg = e
        else:
            self.ok = False
            self.errMsg = f"Перед запуском необходимо удалить папку {self.path['merged_path']}"
        
        return self
    
    def getSubtagNames(self):
        
        # Формирование списка имен сабтегов. Не важно, из old или new: берется отовсюду.
        
        subtags = set()
        
        for subtag in os.listdir(self.path["old_path"]):
            subtags.add(subtag.split('.')[0])
        
        for subtag in os.listdir(self.path["new_path"]):
            subtags.add(subtag.split('.')[0])
        
        self.subtags = list(subtags)
        
        return self
        
    def mergeSubtag(self, subtag, need_explanation):
        
        # Формирование путей ко всем файлам сабтегов: txt и json в папках old, new, merged.
        
        old_txt_path = f"{self.path['old_path']}{subtag}.txt"
        old_json_path = f"{self.path['old_path']}{subtag}.txt.json"
        new_txt_path = f"{self.path['new_path']}{subtag}.txt"
        new_json_path = f"{self.path['new_path']}{subtag}.txt.json"
        merged_txt_path = f"{self.path['merged_path']}{subtag}.txt"
        merged_json_path = f"{self.path['merged_path']}{subtag}.txt.json"
        
        # Формирование пути к папке, куда будет записываться процесс мерджа.
        
        explanation_path = f"{self.path['merged_path']}{EXPLANATION_FOLDER_NAME}\\"
        
        # Проверяем, что в old и new присутствуют оба файла сабтега (txt и json). В противном случае выводим предупреждение, но ошибку не вызываем.
        
        if (not os.path.exists(old_txt_path) or not os.path.exists(new_txt_path) or not os.path.exists(old_json_path) or not os.path.exists(new_json_path)):
            print(f"Рекомендуется проверить файлы сабтега {subtag}. Найдены не все исходные файлы (txt, json).")
        
        if (os.path.exists(old_txt_path) and os.path.exists(new_txt_path)):
            
            # Если происходит мердж txt из old и new, забираем json из new и выводим предупреждение.
            
            if (need_explanation):
                MergeOScript().execute(self.path['old_path'], self.path['new_path'], self.path['merged_path'], f"{subtag}.txt", explanation_path)
            else:
                MergeOScript().execute(self.path['old_path'], self.path['new_path'], self.path['merged_path'], f"{subtag}.txt")
            
            shutil.copyfile(new_json_path, merged_json_path)
            print(f"Произведен мердж кода сабтега {subtag}. Желательно проверить актуальность JSON. Он взят из {self.path['new_path']}")
            
        elif (os.path.exists(old_txt_path) and not os.path.exists(new_txt_path)):
            
            # Если берем txt из old, т.к. в new его нет, то и json берем соответствующий.
            
            shutil.copyfile(old_txt_path, merged_txt_path)
            
        elif (not os.path.exists(old_txt_path) and os.path.exists(new_txt_path)):
            
            # Если берем txt из new, т.к. в old его нет, то и json берем соответствующий.
            
            shutil.copyfile(new_txt_path, merged_txt_path)
            shutil.copyfile(new_json_path, merged_json_path)
    
    def execute(self, need_explanation=False):
        
        # Проверяем, что структура папок корректная.
        
        self = self.checkFolders()
        
        if not (self.ok):
            print(self.errMsg)
            return
        
        # Формируем общий список сабтегов на мердж.
        
        self = self.getSubtagNames()
        
        # Для каждого сабтега запускаем мердж.
        
        for subtag in self.subtags:
            self.mergeSubtag(subtag, need_explanation)