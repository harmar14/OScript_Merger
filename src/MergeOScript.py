import os
import difflib
import codecs

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