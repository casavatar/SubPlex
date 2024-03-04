
################################
##          SUBPLEX           ##
##                            ##
##  Version: 1.0.             ##
##  Create Name: WillhemM.    ##
##  Date Create: 06-09-22.    ##
##                            ##
################################

import os
import json
import deepl # deep learning translation library.

# consult the application's configuration json.
def file_configure():
    try:
        with open('config.json') as file:
            read = json.load(file)
        return read
    except OSError as err:
        print("Error: (0)".format(err))
    return

# search for a file within a folder.
def find_file (name, path):
    try:
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
    except OSError as err:
        print("Error: (0)".format(err))
    return

# manipulation of a file for the translation of its content.
def translate_file(name, lenguaje):
    try:
        path = find_file(name,file_configure()[0]['path'])        
        if path.endswith('.srt'):
            
            data  = []
            texts = []

            translator = deepl.Translator(file_configure()[0]['auth-key'])
            
            with open(path, 'r', encoding='utf-8') as sub:
                while True:

                    sequence_number = sub.readline().strip()
                    
                    if not sequence_number:
                        break

                    texts.clear()
                    times = sub.readline().strip()
                    line  = sub.readline().strip()
                    
                    while line:

                        characters = "♪"

                        for x in range(len(characters)):
                            line = line.replace(characters[x],"").strip()
                    
                        line = translator.translate_text(line,target_lang=lenguaje).text
                        texts.append(line)
                        line = sub.readline().strip()

                    if line == '': 
                        data.append(sequence_number)
                        data.append(times)

                    for x in texts:
                        data.append(x)

                    data.append('\n')

            sub.close()

            path = path.replace('.srt',('_' + lenguaje + '.srt'))                    
            
            with open(path, 'w', encoding='utf-8') as new_sub:
                for x in data:
                    if x != '':
                        new_sub.write(x + '\n')
                    else:
                        new_sub.write(x) 
            new_sub.close()

        print("Translation completed successfully.") 

    except Exception as e: 
        print("Error occurred: {}".format(e))

# main function
if __name__ == '__main__':
    translate_file("All Of Us Strangers.srt","ES")