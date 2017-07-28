# -*- coding: cp1251 -*-
import py_compile

def to_oem866(string):
    """
    Returns string in OEM 866 coding.
    (need for Windows console)
    """
    return str(string).decode("cp1251").encode("cp866")

while True:
    s = raw_input(to_oem866("Введите имя файла: "))
    if s == '.': break
    
    try:
        py_compile.compile(s)
        print to_oem866("Готово!"),
        break
    except IOError, e:
        print to_oem866('''Нет такого файла...\nЧтобы выйти, введите "."\n''')


raw_input(to_oem866("Нажми Enter, чтобы закрыть окно.\n"))

