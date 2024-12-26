import os
import shutil
import codecs
from MergeOScript import MergeOScript

MODULE_FOLDER_PATH = "\\files\\modules\\"
OLD_FOLDER_NAME = "old"
NEW_FOLDER_NAME = "new"
MERGED_FOLDER_NAME = "merged"
EXPLANATION_FOLDER_NAME = "_explanation"

class MergeModule:
    
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def getModulePath(self):
        
        # Формирование путей к папкам для мерджа модулей.
        
        path_dict = dict.fromkeys(["old_path", "new_path", "merged_path"])
        
        path = os.path.abspath(__file__)
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