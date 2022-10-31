import multiprocessing
import pathlib
from pathlib import Path
import argparse
import os
import array
from multiprocessing import Process, Pool
from random import Random
from RandomWordGenerator import RandomWord

import subprocess
VOWELS = set("аэуыояеюиёАЭУЫОЯЕЮИЁioaueoIOAUE")

def check_consonant(char) -> bool:
    return char.isalpha() and char not in VOWELS

def check_vowel(char) -> bool:
    return char in VOWELS
     
def new_process_main_task(directory : str, count_created_files: int):
    rand= Random()
    pool = Pool(multiprocessing.cpu_count())
    multiple_results = [pool.apply_async(main_task, args = (directory, rand.randint(100000, 5000000))) for i in range(count_created_files)]
    for res in multiple_results:
        res.get()
    pool.close()
    pool.join()  

def main_task(directory : str, count_word_write_to_file : int):
    """cоздаёт файл, имеющий название pid и записывает 
    в этот файл рандомные слова  в количестве переданном в функцию, 
    после чего выводит анализ данного файла"""
    current_path = pathlib.Path(directory, str(os.getpid()) +".txt")
    file1 = File_Analyzer(current_path)
    file1.write_rand_words(count_word_write_to_file)
    file1.conduct_analysis_file()
    file1.print_analysis_file()


class File_Analyzer():
    path : str = str
    arr_repeat_words_in_lenght = [None for i in range(100)]
    count_symbol :int = 0
    count_word :int = 0
    max_lenght_word :int = None
    min_lenght_word :int= None
    average_size_word :int = None
    quantity_consonants :int = 0
    quantity_vowels :int = 0
    def __init__(self, file_path):
        self.path = file_path
        
    def print_path(self):
        print(self.path) 

    def print_name_file(self):
        print(Path(self.path).name)

    def print_analysis_file(self):
        try:
            print("*"*70)
            print("Анализ для файла", self.path)
            print("*"*70)
            print("1. Всего символов -->", self.count_symbol)
            print("2. Максимальная длина слова -->", self.max_lenght_word)
            print("3. Минимальная длина символов -->", self.min_lenght_word)
            print("4. Средняя длина символов -->", self.average_size_word)
            print("5. Количество гласных -->", self.quantity_vowels)
            print("6. Количество согласных -->", self.quantity_consonants)
            print("7. Количество повторений слов с одинаковой длиной:")
            print()
            self.print_repeated_in_lenght_words()
        except Exception:
            print("Ошибка при выводе анализа")
      
    def conduct_analysis_file(self):
        self.count_symbol :int = 0
        self.count_word :int = 0
        self.max_lenght_word :int = -1
        self.min_lenght_word :int= 999
        self.average_size_word :int = None
        self.quantity_consonants :int = 0
        self.quantity_vowels :int = 0
        self.arr_repeat_words = [0 for i in range(100)]    
        with open(self.path,'r') as file:      
            for line in file:                      
                self.__conduct_analysis_str(line)
        if self.count_word != 0:    
            self.average_size_word =  self.count_symbol / self.count_word
        


    def __conduct_analysis_str(self, str):
        try:
            words = str.split()
            for word in words:
                self.count_word += 1
                self.arr_repeat_words[len(word)] +=1
                if len(word) > self.max_lenght_word:
                    self.max_lenght_word = len(word)
                elif len(word) < self.min_lenght_word:
                    self.min_lenght_word = len(word)
                for char in word:
                    self.count_symbol += 1  
                    if check_vowel(char):
                     self.quantity_vowels += 1
                    elif check_consonant(char):
                        self.quantity_consonants +=1
        except Exception:
            print("Ошибка при анализе")
                    
    def print_repeated_in_lenght_words(self):
        for i in range(len(self.arr_repeat_words)):
            if self.arr_repeat_words[i] == 0:
                continue
            print("\t * " + str(i) + " сим. >> " + str(self.arr_repeat_words[i]) + " повтор.")

    def write_rand_words(self, count : int):
        try:
           with open(self.path,'w') as file:
                for _ in range(count):               
                    file.write(" " + self.gen_word())
        except Exception:
            print("Ошибка при записи")

    def gen_word(self) -> str:
        rw = RandomWord(max_word_size = 10, constant_word_size = False )
        return rw.generate()    
    

def main():
    # использование библиотеки pathlib для создания стандартного пути к редактируемому файлу
    path_to_file :str = pathlib.Path(pathlib.Path.cwd(), )
    # использование библиотеки agrparse для обработки аргументов начальной настройки программы (задание пути)
    set_up = argparse.ArgumentParser()
    # Аргументы строки (один аргумент, имеюющий стандартное относительное значение пути для редактируемого файла)
    set_up.add_argument('path', type=str, nargs='?', help=' path to file', default = str(path_to_file) )
    arguments = set_up.parse_args()
    print("-"*70)
    print("Местоположение для проверки файлов - " + arguments.path)
    print("-"*70)
    new_process_main_task(arguments.path, 1)
   
if __name__ == "__main__":
    main()