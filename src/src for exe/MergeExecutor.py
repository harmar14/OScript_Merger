import os
import sys
import codecs
import shutil
import difflib

SUBTAG_FOLDER_PATH = "\\files\\subtags\\"
MODULE_FOLDER_PATH = "\\files\\modules\\"
OLD_FOLDER_NAME = "old"
NEW_FOLDER_NAME = "new"
MERGED_FOLDER_NAME = "merged"
EXPLANATION_FOLDER_NAME = "_explanation"

class MergeOScript:
    
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def prepareExplanationFolder(self, explanation_path):
        
        # Создание папки explanation при ее отсутствии.
        
        if not (os.path.isdir(explanation_path)):
            try:
                os.mkdir(explanation_path)
            except Exception as e:
                self.ok = False
                self.errMsg = e
        
        return self
    
    def mergeScript(self, old_path, new_path, merged_path, script):
        
        old_script_path = f"{old_path}{script}"
        new_script_path = f"{new_path}{script}"
        merged_script_path = f"{merged_path}{script}"
        
        # Проверяем корректность путей к файлам для мерджа.
        
        if not (os.path.exists(old_script_path) and os.path.exists(new_script_path)):
            self.ok = False
            self.errMsg = "Не найдены исходные скрипты."
            return self
        
        old_script = codecs.open(old_script_path, mode='r', encoding='utf-8')
        new_script = codecs.open(new_script_path, mode='r', encoding='utf-8')
        merged_script = codecs.open(merged_script_path, mode='w', encoding='utf-8')
        
        # Считываем содержимое файлов.
        
        old_lines = old_script.readlines()
        new_lines = new_script.readlines()
        
        # Выполняем сравнение файлов, построчно обходим результат. В explanation пишем абсолютно всё, а в итоговый файл - только строки, которые уже были или появились.
        
        for line in difflib.Differ().compare(old_lines, new_lines):
            if (line[0] != '-' and line[0] != '?'):
                merged_script.write(line[2:])
        
        old_script.close()
        new_script.close()
        merged_script.close()
        
        return self
    
    def mergeScriptWithExplanation(self, old_path, new_path, merged_path, script, explanation_path):
        
        # В Python нет перегрузки, поэтому оъявлена идентичная предыдущей функция (не захотелось городить условия в предыдущей).
        
        old_script_path = f"{old_path}{script}"
        new_script_path = f"{new_path}{script}"
        merged_script_path = f"{merged_path}{script}"
        explanation_file_path = f"{explanation_path}{script}"
        
        # Проверяем корректность путей к файлам для мерджа.
        
        if not (os.path.exists(old_script_path) and os.path.exists(new_script_path)):
            self.ok = False
            self.errMsg = "Не найдены исходные скрипты."
            return self
        
        old_script = codecs.open(old_script_path, mode='r', encoding='utf-8')
        new_script = codecs.open(new_script_path, mode='r', encoding='utf-8')
        merged_script = codecs.open(merged_script_path, mode='w', encoding='utf-8')
        explanation_file = codecs.open(explanation_file_path, mode='w', encoding='utf-8')
        
        # Считываем содержимое файлов.
        
        old_lines = old_script.readlines()
        new_lines = new_script.readlines()
        
        # Выполняем сравнение файлов, построчно обходим результат. В explanation пишем абсолютно всё, а в итоговый файл - только строки, которые уже были или появились.
        
        for line in difflib.Differ().compare(old_lines, new_lines):
            explanation_file.write(line)
            if (line[0] != '-' and line[0] != '?'):
                merged_script.write(line[2:])
        
        old_script.close()
        new_script.close()
        merged_script.close()
        explanation_file.close()
        
        return self    
    
    def execute(self, old_path, new_path, merged_path, script, explanation_path=None):
        
        # Проверяем, передан ли explanation_path. Если да, проверяем существование этого пути и выполняем мердж с записью доп.файла процесса мерджа. Иначе - запускаем обычный мердж.
        
        if (explanation_path is not None):
            self = self.prepareExplanationFolder(explanation_path)
            if not (self.ok):
                print(self.errMsg)
                return self
            self = self.mergeScriptWithExplanation(old_path, new_path, merged_path, script, explanation_path)
        else:
            self = self.mergeScript(old_path, new_path, merged_path, script)
        
        if not (self.ok):
            print(self.errMsg)
            return

class MergeModule:
    
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def getModulePath(self):
        
        # Формирование путей к папкам для мерджа модулей.
        
        path_dict = dict.fromkeys(["old_path", "new_path", "merged_path"])
        
        #path = os.path.abspath(__file__)
        path = sys.executable
        path = '\\'.join(path.split('\\')[:-2]) + MODULE_FOLDER_PATH
        
        path_dict["old_path"] = f"{path}{OLD_FOLDER_NAME}\\"
        path_dict["new_path"] = f"{path}{NEW_FOLDER_NAME}\\"
        path_dict["merged_path"] = f"{path}{MERGED_FOLDER_NAME}\\"
        
        self.path = path_dict
        
        return self
    
    def checkFolders(self):
        
        # Формирование путей old, new, merge.
        
        self = self.getModulePath()
        
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
    
    def getModuleNames(self):
        
        # Формирование списка имен модулей. Не важно, из old или new: берется отовсюду.
        
        modules = set()
        
        for module in os.listdir(self.path["old_path"]):
            modules.add(module)
        
        for module in os.listdir(self.path["new_path"]):
            modules.add(module)
        
        self.modules = list(modules)
        
        return self
    
    def prepareFolders(self):
        
        # Подготовка папок для мерджа.
        
        for module in self.modules:
            try:
                os.mkdir(f"{self.path['merged_path']}{module}")
            except Exception as e:
                self.ok = False
                self.errMsg = e
            try:
                os.mkdir(f"{self.path['merged_path']}{EXPLANATION_FOLDER_NAME}\\{module}")
            except Exception as e:
                self.ok = False
                self.errMsg = e
    
    def mergeIni(self, old_ini_path, new_ini_path, merged_ini_path, module):
        
        # Мердж ini-файлов модуля.
        
        old_dependencies = []
        old_description = []
        old_install = []
        old_ospaces = []
        new_dependencies = []
        new_description = []
        new_install = []
        new_ospaces = []
        dependencies = []
        description = []
        install = []
        ospaces = []
        
        ini = codecs.open(merged_ini_path, mode='w', encoding='utf-8')
        old_ini = codecs.open(old_ini_path, mode='r', encoding='utf-8')
        new_ini = codecs.open(new_ini_path, mode='r', encoding='utf-8')
        
        # Чтение двух версий ini-файла модуля.
        
        old_data = [line.strip() for line in old_ini]
        new_data = [line.strip() for line in new_ini]
        
        # Парсинг ini-файла модуля OT21.
        
        while(len(old_data) != 0):
            if (old_data[0] == '[dependencies]'):
                old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] != ''):
                    old_dependencies.append(old_data[0].split('=')[1])
                    old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] == ''):
                    old_data.pop(0)
            elif (old_data[0] == '[description]'):
                old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] != ''):
                    old_description.append(old_data[0])
                    old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] == ''):
                    old_data.pop(0)
            elif (old_data[0] == '[install]'):
                old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] != ''):
                    old_install.append(old_data[0])
                    old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] == ''):
                    old_data.pop(0)
            elif (old_data[0] == '[OSpaces]'):
                old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] != ''):
                    old_ospaces.append(old_data[0].split('=')[1])
                    old_data.pop(0)
                while (len(old_data) > 0 and old_data[0] == ''):
                    old_data.pop(0)
        
        # Парсинг ini-файла модуля OT24.
        
        while(len(new_data) != 0):
            if (new_data[0] == '[dependencies]'):
                new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] != ''):
                    new_dependencies.append(new_data[0].split('=')[1])
                    new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] == ''):
                    new_data.pop(0)
            elif (new_data[0] == '[description]'):
                new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] != ''):
                    new_description.append(new_data[0])
                    new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] == ''):
                    new_data.pop(0)
            elif (new_data[0] == '[install]'):
                new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] != ''):
                    new_install.append(new_data[0])
                    new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] == ''):
                    new_data.pop(0)
            elif (new_data[0] == '[OSpaces]'):
                new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] != ''):
                    new_ospaces.append(new_data[0].split('=')[1])
                    new_data.pop(0)
                while (len(new_data) > 0 and new_data[0] == ''):
                    new_data.pop(0)
        
        # Сборка итоговых данных для ini-файла модуля.
        
        # Секция dependencies.
        
        choice = ''
        
        if (sorted(old_dependencies) != sorted(new_dependencies)):
            while (choice != "old" and choice != "new" and choice != "merged"):
                choice = input(f"Секции dependencies модуля {module} отличаются. Выберите ini, из которого будет взята итоговая секция (old/new), либо опцию объединения (merged):")
        else:
            choice = "new"
        
        if (choice == "old"):
            dependencies = old_dependencies
        elif (choice == "merged"):
            dependencies = list(set(old_dependencies) | set(new_dependencies))
        else:
            dependencies = new_dependencies
        
        # Секции description и install всегда берем из new ini.
        
        description = new_description
        install = new_install
        
        # Секция OSpaces.
        
        choice = ''
        
        if (sorted(old_ospaces) != sorted(new_ospaces)):
            while (choice != "old" and choice != "new" and choice != "merged"):
                choice = input(f"Секции OSpaces модуля {module} отличаются. Выберите ini, из которого будет взята итоговая секция (old/new), либо опцию объединения (merged): ")
        else:
            choice = "new"
        
        if (choice == "old"):
            ospaces = old_ospaces
        elif (choice == "merged"):
            ospaces = list(set(old_ospaces) | set(new_ospaces))
        else:
            ospaces = new_ospaces
            
        # Запись готовых данных в итоговый ini-файл модуля.
        
        ini.write("[dependencies]\n")
        i = 0
        for line in dependencies:
            i += 1
            ini.write(f"requires_{i}={line}\n")
        
        ini.write("\n[description]\n")
        for line in description:
            ini.write(line + '\n')
        
        ini.write("\n[install]\n")
        for line in install:
            ini.write(line + '\n')
        
        ini.write("\n[ospaces]\n")
        i = 0
        for line in ospaces:
            i += 1
            ini.write(f"ospace_{i}={line}\n")
        
        old_ini.close()
        new_ini.close()
        ini.close()
        
        return ospaces
    
    def mergeIniFiles(self, old_path, new_path, merged_path, module):
        
        # Запуск мерджа ini-файлов.
        
        old_ini_path = f"{old_path}{module}.ini"
        new_ini_path = f"{new_path}{module}.ini"
        merged_ini_path = f"{merged_path}{module}.ini"
        
        if (os.path.exists(old_ini_path) and os.path.exists(new_ini_path)):
            return self.mergeIni(old_ini_path, new_ini_path, merged_ini_path, module)
        else:
            self.ok = False
            self.errMsg = f"Не обнаружены ini-файлы модуля {module}"
            return None
    
    def mergeStructure(self, old_path, new_path, merged_path, need_explanation, explanation_path=None):
        
        # Создание целевой папки мерджа.
        
        if not (os.path.isdir(merged_path)):
            try:
                os.mkdir(merged_path)
            except Exception as e:
                print(f"Ошибка создания папки: {e}")
                return
        
        # Создание папки для доп.файлов с пояснениями к мерджу.
        
        if (need_explanation and not os.path.isdir(explanation_path)):
            try:
                os.mkdir(explanation_path)
            except Exception as e:
                print(f"Ошибка создания папки: {e}")
                return
        
        # Получение содержимого директорий.
        
        old_objects = set(os.listdir(old_path))
        new_objects = set(os.listdir(new_path))
        
        objects = old_objects & new_objects
        
        # Какие-то из объектов присутствуют только в первой или только во второй исходной директории, их нужно перенести.
        
        for obj in (old_objects - objects):
            if (os.path.isdir(f"{old_path}{obj}\\")):
                shutil.copytree(f"{old_path}{obj}\\", f"{merged_path}{obj}\\")
            else:
                shutil.copyfile(f"{old_path}{obj}", f"{merged_path}{obj}")
        
        for obj in (new_objects - objects):
            if (os.path.isdir(f"{new_path}{obj}\\")):
                shutil.copytree(f"{new_path}{obj}\\", f"{merged_path}{obj}\\")
            else:
                shutil.copyfile(f"{new_path}{obj}", f"{merged_path}{obj}")
        
        # Объекты, присутствующие в обеих исходных папках, подлежат мерджу.
        for obj in objects:
            if (os.path.isdir(f"{old_path}{obj}\\")):
                self.mergeStructure(f"{old_path}{obj}\\", f"{new_path}{obj}\\", f"{merged_path}{obj}\\", need_explanation, f"{explanation_path}{obj}\\")
            else:
                MergeOScript().execute(old_path, new_path, merged_path, obj, explanation_path)
        
    def mergeOspace(self, old_path, new_path, merged_path, module, ospace, need_explanation):
        
        # Мердж кода модуля.
        
        old_ospace_path = f"{old_path}{ospace.upper()}\\"
        new_ospace_path = f"{new_path}{ospace.upper()}\\"
        merged_ospace_path = f"{merged_path}{ospace.upper()}\\"
        
        if (need_explanation):
            explanation_path = f"{self.path['merged_path']}{EXPLANATION_FOLDER_NAME}\\{module}\\"
            explanation_ospace_path = f"{explanation_path}{ospace.upper()}\\"
                
        # Если OSpace есть в одной версии модуля, но отсутствует в другой, просто копируем оттуда, где он есть.
        # Если он в обоих версиях присутствует, тогда нужен мердж кода.
        
        if (os.path.isdir(old_ospace_path) and not os.path.isdir(new_ospace_path)):
            shutil.copytree(old_ospace_path, merged_ospace_path)
            
        elif (not os.path.isdir(old_ospace_path) and os.path.isdir(new_ospace_path)):
            shutil.copytree(new_ospace_path, merged_ospace_path)
            
        elif (os.path.isdir(old_ospace_path) and os.path.isdir(new_ospace_path)):
            if (need_explanation):
                self.mergeStructure(old_ospace_path, new_ospace_path, merged_ospace_path, need_explanation, explanation_ospace_path)
            else:
                self.mergeStructure(old_ospace_path, new_ospace_path, merged_ospace_path, need_explanation)
            
        else:
            self.ok = False
            self.errMsg = f"Не удалось получить OSpace {ospace} модуля {module}. Необходимо проверить переданные на мердж модули."
        
        return self
    
    def mergeModule(self, module, need_explanation):
        
        old_path = f"{self.path['old_path']}{module}\\"
        new_path = f"{self.path['new_path']}{module}\\"
        merged_path = f"{self.path['merged_path']}{module}\\"
        
        if (os.path.isdir(old_path) and not os.path.isdir(new_path)):
            try:
                os.rmdir(merged_path)
                shutil.copytree(old_path, merged_path)
                print(f"Рекомендуется проверить файлы модуля {module}. Модуль не найден в {new_path}. Произведено копирование из {old_path}.")
            except Exception as e:
                print(f"Ошибка переноса модуля: {e}")
            return
        
        if (not os.path.isdir(old_path) and os.path.isdir(new_path)):
            try:
                os.rmdir(merged_path)
                shutil.copytree(new_path, merged_path)
                print(f"Рекомендуется проверить файлы модуля {module}. Модуль не найден в {old_path}. Произведено копирование из {new_path}.")
            except Exception as e:
                print(f"Ошибка переноса модуля: {e}")
            return
        
        # Если предыдущие два условия не выполнились, модуль точно есть и в old, и в new. Значит, есть, что мерджить.
        
        # Мердж ini-файлов.
        
        ospaces = self.mergeIniFiles(old_path, new_path, merged_path, module)
        
        # Мердж OScript.
        
        for ospace in ospaces:
            self = self.mergeOspace(old_path, new_path, merged_path, module, ospace, need_explanation)
        
        if ((len(ospaces) + 1) < len(os.listdir(old_path)) or (len(ospaces) + 1) < len(os.listdir(new_path))):
            print(f"Рекомендуется проверить файлы модуля {module}. В нем могут быть вспомогательные папки (например, html, support или др.).")
        
    def execute(self, need_explanation=False):
        
        # Проверка корректности структуры папок.
        
        self = self.checkFolders()
        
        if not (self.ok):
            print(self.errMsg)
            return
        
        # Получение всех имен папок модулей из структур.
        
        self = self.getModuleNames()
        
        # Подготовка папок модулей для мерджа.
        
        self.prepareFolders()
        
        if not (self.ok):
            print(self.errMsg)
            return
        
        # Запуск мерджа каждого модуля.
        
        for module in self.modules:
            self.mergeModule(module, need_explanation)

class MergeSubtag:
    
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def getSubtagPath(self):
        
        # Формирование путей к папкам для мерджа сабтегов.
        
        path_dict = dict.fromkeys(["old_path", "new_path", "merged_path"])
        
        #path = os.path.abspath(__file__)
        path = sys.executable
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

class MergeExecutor:
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def checkInstrumentStructure(self):
        
        #path = os.path.abspath(__file__)
        path = sys.executable
        path = '\\'.join(path.split('\\')[:-2])
        
        if not (os.path.isdir(f"{path}files\\modules\\old\\")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}files\\modules\\old\\"
        
        if not (os.path.isdir(f"{path}files\\modules\\new\\")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}files\\modules\\new\\"
        
        if not (os.path.isdir(f"{path}files\\subtags\\old\\")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}files\\subtags\\old\\"
        
        if not (os.path.isdir(f"{path}files\\subtags\\new\\")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}files\\subtags\\new\\"
            
        return self
    
    def mergeModules(self, need_explanation):
        MergeModule().execute(need_explanation)
    
    def mergeSubtags(self, need_explanation):
        MergeSubtag().execute(need_explanation)
    
    def execute(self):
        
        action = ''
        need_explanation = ''
        
        print("Выберите действие:")
        print("1 - мердж модулей")
        print("2 - мердж сабтегов")
        print("3 - мердж и модулей, и сабтегов")
        print("4 - выход")
        action = input()
        while (action not in ["1", "2", "3", "4"]):
            print("Неизвестное значение. Попробуйте еще раз.")
            action = input()
        if (action == "4"):
            return
        
        print("Нужно ли записывать процесс мерджа? (Запись производится в дополнительную папку.)")
        print("1 - да")
        print("2 - нет")
        print("3 - выход")
        need_explanation = input()
        while (need_explanation not in ["1", "2", "3"]):
            print("Неизвестное значение. Попробуйте еще раз.")
            need_explanation = input()
        if (need_explanation == "3"):
            return
        
        if (action == "1"):
            if (need_explanation == "1"):
                self.mergeModules(True)
            elif (need_explanation == "2"):
                self.mergeModules(False)
        elif (action == "2"):
            if (need_explanation == "1"):
                self.mergeSubtags(True)
            elif (need_explanation == "2"):
                self.mergeSubtags(False)
        elif (action == "3"):
            if (need_explanation == "1"):
                self.mergeModules(True)
                self.mergeSubtags(True)
            elif (need_explanation == "2"):
                self.mergeModules(False)
                self.mergeSubtags(False)

MergeExecutor().execute()
input("Для выхода нажмите Enter.")