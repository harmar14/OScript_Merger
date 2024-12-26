import os
from MergeModule import MergeModule
from MergeSubtag import MergeSubtag

class MergeExecutor:
    def __init__(self):
        self.ok = True
        self.errMsg = ''
    
    def checkInstrumentStructure(self):
        
        path = os.path.abspath(__file__)
        path = '\\'.join(path.split('\\')[:-2])
        
        if not (os.path.isdir(f"{path}\\files\\modules\\old")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}\\files\\modules\\old"
            return self
        
        if not (os.path.isdir(f"{path}\\files\\modules\\new")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}\\files\\modules\\new"
            return self
        
        if not (os.path.isdir(f"{path}\\files\\subtags\\old")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}\\files\\subtags\\old"
            return self
        
        if not (os.path.isdir(f"{path}\\files\\subtags\\new")):
            self.ok = False
            self.errMsg = f"Отсутствует директория {path}\\files\\subtags\\new"
            return self
            
        return self
    
    def mergeModules(self, need_explanation):
        MergeModule().execute(need_explanation)
    
    def mergeSubtags(self, need_explanation):
        MergeSubtag().execute(need_explanation)
    
    def execute(self):
        
        self.checkInstrumentStructure()
        if not (self.ok):
            print(self.errMsg)
            return
        
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