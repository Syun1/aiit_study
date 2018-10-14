'''
Python上でシェルスクリプト(bash)を動かすプログラム
'''

# -*- coding: utf-8 -*-

import os
import re

while True:
    pattern = r"^\s?cd\s?(.*)"
    command = input("mysh> ")
    result = re.match(pattern, command) 

    if result:
        try:
            if result.group(1) == "~":
                os.chdir(os.environ['HOME'])
            else:
                os.chdir(result.group(1))
        except OSError:
            print("No such file or directory: '%s'" % (result.group(1)))
    elif command == "pwd":
        print(os.getcwd())
    elif command == "exit":
        break
    else:
        os.system(command)
    
