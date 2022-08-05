from bs4 import BeautifulSoup
import os
import requests

#modificato
os.system('cls' if os.name == 'nt' else 'clear')
path = os.getcwd() + '\\files\\'

nextType = ''

home_url = 'https://thebeginningaftertheend.online'

home_html = requests.get(home_url).text
soup = BeautifulSoup(home_html, 'lxml')

chapters = soup.find('ul', class_='su-posts su-posts-list-loop').find_all('li', class_='su-post')

chapter_num_list = []
chapter_link_list = []

for chapter in chapters:
    chapter_num_list.insert(0, int(chapter.find('a').text.split(' ')[-1]))
    chapter_link_list.insert(0, chapter.find('a')['href'])

def Read(chapter_to_read):
    if chapter_to_read.isnumeric():
        chapter_to_read = int(chapter_to_read)
    else:
        return 'chapter needs to be a number'

    if chapter_to_read not in chapter_num_list:
        return 'chapter does not exist'
    
    if chapter_to_read == chapter_num_list[-1]:
        url = chapter_link_list[chapter_to_read - 1]
        os.startfile(url)
        return 'opened countdown'

    url = chapter_link_list[chapter_to_read - 1]

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # if chapter_to_read >= 150:
    #     separators = soup.find_all('div', class_='wp-block-image')
    # else:
    #     separators = soup.find_all('div', class_='separator')

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
        
        print ("\033[A                             \033[A")
    with open(path + 'list.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')
        file.close()

    with open(path + 'list.txt', 'a') as file:
        if str(chapter_to_read) not in contents:
            file.write(str(chapter_to_read) + '\n')
        file.close()
    with open(path + 'last_read.txt', 'w') as file:
        file.write(str(chapter_to_read) + '\n' + nextType)
        file.close()

    os.startfile(path + 'index.html')

def List():
    try:
        with open(path + 'list.txt', 'r') as file:
            contents = file.read().rstrip().split('\n')
            for content in contents:
                print(content)
            file.close()
    except:
        print('something went wrong')

def ClearList():
    with open(path + 'list.txt', 'w') as file:
        file.write('you read chapters:\n')
        file.close()
    with open(path + 'last_read.txt', 'w') as file:
        file.write('0' + '\n' + nextType)
        file.close()
    print('list cleared')

def CancelFromList():
    selected_chapter = input('what chapter do you want to delete from the list? ')
    if selected_chapter.isnumeric() == False:
        return 'chapter needs to be a number'
    
    with open(path + 'list.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')
        file.close()
    
    if selected_chapter in contents:
        contents.remove(selected_chapter)
    else:
        return 'chapter is not in the list'
    
    with open(path + 'list.txt', 'w') as file:
        for line in contents:
            file.write(line + '\n')
        file.close()

def Sort():
    with open(path + 'list.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')
        file.close()
    
    contents[0] = -1
    for content in contents:
        contents[contents.index(content)] = int(content)
    
    contents.sort()

    contents[0] = 'you read chapters:'

    with open(path + 'list.txt', 'w') as file:
        for line in contents:
            file.write(str(line) + '\n')
        file.close()

def NextToTheBigger():
    with open(path + 'list.txt', 'r') as file:
        contents = file.read().rstrip().split('\n')
        file.close()
    
    Read(str(int(contents[-1]) + 1))

def NextToTheLast():
    with open(path + 'last_read.txt', 'r') as file:
        contents = file.read().split('\n')
        content = contents[0]
        file.close()
    Read(str(int(content) + 1))

def Next(nextType):
    match nextType:
        case 'NextToTheBigger':
            NextToTheBigger()
        case 'NextToTheLast':
            NextToTheLast()

def ChapterList():
    for chapter in chapter_num_list:
        print(chapter)

while True:
    with open(path + 'last_read.txt', 'r') as file:
        last_read_contents = file.read().split('\n')
        nextType = last_read_contents[-1]
        file.close()

    action = input('what do you want to do? ').lower()
    Sort()

    commands = ['quit - exit', 'read', 'list', 'clear list', 'cls - clear', 'switch next', 'nxt - next - nx', 'canc - cancel - del - delete', 'chapters', 'sort']
    
    match action:
        case 'quit' | 'exit':
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        case 'read':
            read = Read(input('what chapter do you want to read? '))
            if read == None:
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(read)
        case 'list':
            os.system('cls' if os.name == 'nt' else 'clear')
            List()
        case 'clear list':
            os.system('cls' if os.name == 'nt' else 'clear')
            ClearList()
        case 'cls' | 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        case 'switch next':
            os.system('cls' if os.name == 'nt' else 'clear')
            match nextType:
                case 'NextToTheBigger':
                    with open(path + 'last_read.txt', 'w') as file:
                        file.write(last_read_contents[0] + '\n' + 'NextToTheLast')
                        file.close()
                    print('switched to NextToTheLast')
                case 'NextToTheLast':
                    with open(path + 'last_read.txt', 'w') as file:
                        file.write(last_read_contents[0] + '\n' + 'NextToTheBigger')
                        file.close()
                    print('switched to NextToTheBigger')
            
        case 'nxt' | 'nx' | 'next':
            os.system('cls' if os.name == 'nt' else 'clear')
            Next(nextType)
        case 'canc' | 'cancel' | 'del' | 'delete':
            deleted = CancelFromList()
            if deleted != None:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(deleted)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('chapter deleted succesfully')
        case 'chapters':
            os.system('cls' if os.name == 'nt' else 'clear')
            ChapterList()
        case 'sort':
            os.system('cls' if os.name == 'nt' else 'clear')
            Sort()
        case 'commands':
            os.system('cls' if os.name == 'nt' else 'clear')
            for command in commands:
                print(command)
        case _:
            print('command does not exist')
