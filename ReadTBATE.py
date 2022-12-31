#!./venv/bin/python

from bs4 import BeautifulSoup
import os
import requests
from ruamel import yaml

os.system('cls' if os.name == 'nt' else 'clear') # clears the console
if os.name == 'nt':
    filesDirectory = '\\files\\'
    import pyautogui as pgui
    pgui.press("F11")
elif os.name == 'posix':
    filesDirectory = '/files/'
    print('remember, with this operating system you can not read, but you can see the list if you want')
else:
    print('this operating system is not supported')
    quit()

path = os.getcwd() + filesDirectory

home_url = 'https://thebeginningaftertheend.online' # TBATE
# home_url = 'https://damnreincarnation.com/' # Damn reincarnation

home_html = requests.get(home_url).text
soup = BeautifulSoup(home_html, 'lxml')

chapters = soup.find('ul', class_='su-posts su-posts-list-loop').find_all('li', class_='su-post')

chapter_num_list = []
chapter_link_list = []

for chapter in chapters:
    if "." in chapter.find('a').text.split(' ')[-1]:
        chapter_num_list.insert(0, float(chapter.find('a').text.split(' ')[-1]))
    else:
        chapter_num_list.insert(0, int(chapter.find('a').text.split(' ')[-1]))
    chapter_link_list.insert(0, chapter.find('a')['href'])

def Read(chapter_to_read):
    if chapter_to_read.isnumeric():
        chapter_to_read = int(chapter_to_read)
    else:
        return 'chapter needs to be a number'

    if chapter_to_read not in chapter_num_list:
        return 'chapter does not exist'
    
    # if chapter_to_read == chapter_num_list[-1]:
    #     url = chapter_link_list[chapter_to_read - 1]
    #     os.startfile(url)
    #     return 'opened countdown'

    url = chapter_link_list[chapter_to_read - 1]

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    if chapter_to_read >= 156 and chapter_to_read <= 162:
        separators = soup.find_all('div', class_='wp-block-image')
    else:
        separators = soup.find_all('div', class_='separator')
    
    image_num = 0

    for separator in separators:
        image_num += 1
        image_url = separator.find('img')['src']

        print('loading image ' + str(image_num) + ' of ' + str(len(separators)))
        
        if image_num == 1:
            with open(path + "index.html", 'w') as html_write:
                html_write.write(f'<!DOCTYPE html><html><head><title>TBATE</title><link rel="stylesheet" href="style.css"><script src="script.js"></script></head><body><img src="{image_url}" align="absbottom">')
                html_write.close()
        elif image_num == len(separators):
            with open(path + 'index.html', 'a') as html_write:
                html_write.write(f'<img src="{image_url}" align="absbottom"></body></html>')
                html_write.close()
        else:
            with open(path + 'index.html', 'a') as html_write:
                html_write.write(f'<img src="{image_url}" align="absbottom">')
                html_write.close()
        
        print ("\033[A                             \033[A") # clears the line on top
    with open(path + 'list TBATE.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')

    with open(path + 'list TBATE.txt', 'a') as file:
        if str(chapter_to_read) not in contents:
            file.write(str(chapter_to_read) + '\n')
    with open(path + 'data.yml', 'w') as file:
        file.write(fileBackup.replace(" last read TBATE: " + str(dataFile[" last read TBATE"]), " last read TBATE: " + str(chapter_to_read)))

    os.startfile(path + 'index.html')

def List():
    try:
        with open(path + 'list TBATE.txt', 'r') as file:
            contents = file.read().rstrip().split('\n')
            for content in contents:
                print(content)
            return contents
    except:
        print('something went wrong')

def ClearList():
    with open(path + 'list TBATE.txt', 'w') as file:
        file.write('you read chapters:\n')
    with open(path + 'data.yml', 'w') as file:
        file.write(fileBackup.replace(" last read TBATE: " + str(dataFile[" last read TBATE"]), " last read TBATE: 0"))
    print('list cleared')

def CancelFromList():
    selected_chapter = input('what chapter do you want to delete from the list? ')
    if selected_chapter.isnumeric() == False:
        return 'chapter needs to be a number'
    
    with open(path + 'list TBATE.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')
    
    if selected_chapter in contents:
        contents.remove(selected_chapter)
    else:
        return 'chapter is not in the list'
    
    with open(path + 'list TBATE.txt', 'w') as file:
        for line in contents:
            file.write(line + '\n')

def Sort():
    with open(path + 'list TBATE.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')
    
    contents[0] = -1
    for content in contents:
        contents[contents.index(content)] = int(content)
    
    contents.sort()

    contents[0] = 'you read chapters:'

    with open(path + 'list TBATE.txt', 'w') as file:
        for line in contents:
            file.write(str(line) + '\n')

def Next(nextType):
    match nextType:
        case 'NextToTheBigger':
            return Read(str(int(List()[-1]) + 1))
        case 'NextToTheLast':
            return Read(str(int(dataFile[" last read TBATE"]) + 1))

def ChapterList():
    for chapter in chapter_num_list:
        print(chapter)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    with open(path + "data.yml", 'r') as file:
        dataFile = yaml.safe_load(file)
        nextType = dataFile["next type"]
    with open(path + "data.yml", 'r') as file:
        fileBackup = file.read()

    action = input('what do you want to do? ').lower()
    Sort()

    commands = ['quit - exit', 'read', 'list', 'clear list', 'cls - clear', 'switch next', 'nxt - next - nx', 'del - delete - rm - remove', 'chapters', 'sort', 'edit']
    
    match action:
        case 'quit' | 'exit':
            clear_console()
            break
        case 'read':
            output = Read(input('what chapter do you want to read? '))
            if output == None:
                clear_console()
            else:
                clear_console()
                print(output)
        case 'list':
            clear_console()
            List()
        case 'clear list':
            clear_console()
            ClearList()
        case 'cls' | 'clear':
            clear_console()
        case 'switch next':
            clear_console()
            match nextType:
                case 'NextToTheBigger':
                    with open(path + 'data.yml', 'w') as file:
                        file.write(fileBackup.replace(nextType, "NextToTheLast"))
                    print('switched to NextToTheLast')
                case 'NextToTheLast':
                    with open(path + 'data.yml', 'w') as file:
                        file.write(fileBackup.replace(nextType, "NextToTheBigger"))
                    print('switched to NextToTheBigger')
            
        case 'nxt' | 'nx' | 'next':
            clear_console()
            output = Next(nextType)
            if output == None:
                clear_console()
            else:
                clear_console()
                print(output)
        case 'del' | 'delete' | 'rm' | 'remove':
            deleted = CancelFromList()
            if deleted != None:
                clear_console()
                print(deleted)
            else:
                clear_console()
                print('chapter deleted succesfully')
        case 'chapters':
            clear_console()
            ChapterList()
        case 'sort':
            clear_console()
            Sort()
        case 'commands':
            clear_console()
            for command in commands:
                print(command)
        case 'edit':
            os.system('code .')
            break
        case _:
            print('command does not exist')
