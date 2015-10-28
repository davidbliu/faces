import os
from config import *
OUTPUT_FILE = './js/data.js' 

def get_directory_filenames(d):
    return list(set([x for x in os.listdir(d)]))
face_urls = get_directory_filenames(FACES_DIR)
face_urls = [x for x in face_urls if '.jpg' in x]

morph_urls = get_directory_filenames(MORPH_DIR)
morph_urls = [x for x in morph_urls if '.png' in x]

with open(OUTPUT_FILE, 'w') as outfile:
    outfile.write('face_urls=')
    outfile.write(str(face_urls)+';')
    outfile.write('\n')
    outfile.write('morph_urls=')
    outfile.write(str(morph_urls)+';')


