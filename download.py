import os
from bs4 import BeautifulSoup as bs
import requests
import enchant
import vlc


# import sys
# from traceback import print_tb
# import snowballstemmer

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['+ ' + '-' * width + ' +']
    for s in lines:
        res.append('| ' + (s + ' ' * width)[:width] + ' |')
    res.append('+ ' + '-' * width + ' +')
    return '\n'.join(res)

def join_numbered_list(list_of_str):
    return "\n".join((f"{item[0]} {item[1]}" for item in  list(zip([f"({index})" for index in range(len(list_of_str))],list_of_str))))


def make_flashcard(word,out_path):

    # headers is to fake the identity . some websites can detect we are scraping
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    url = 'https://www.ldoceonline.com/dictionary/' + word
    page = requests.get(url,headers=headers)

    soup = bs(page.content,features="lxml")

    if soup.find(class_="pagetitle") is None:
        print(style.RED + f"could't find the word\ntry the word's base form instead")
        return

    title= soup.find(class_="pagetitle").text

    #bre for british insted of amefile -> brefile
    sound = soup.find(class_='speaker amefile fas fa-volume-up hideOnAmp')
    
    sound_link = ""
    if sound != None: 
        sound_link = sound['data-src-mp3'].split('?')[0]
        p = vlc.MediaPlayer(sound_link)
        p.play()
        
    else:
        print(style.RED+"Sound not found")

    #![s](https://www.ldoceonline.com/media/english/ameProns/synthetic.mp3)

    meanings= soup.find_all(class_="Sense")
    Senses=[]

    for item in meanings:
        deffinition =''
        
        deff = item.find(class_="DEF")
        if deff:
            deffinition = deff.text
        
        elif item.find(class_="REFHWD"):
            deffinition = item.find(class_="REFHWD").text.strip()

        examples=[]
        for eg in item.find_all(class_="EXAMPLE"):
            text = eg.text.strip()
            eg_sound = eg.find(class_="speaker exafile fas fa-volume-up hideOnAmp")
            if eg_sound == None:
                examples.append([text,None])
                continue
            eg_sound=eg_sound['data-src-mp3'].split('?')[0]
            examples.append([text,eg_sound])
        Senses.append([deffinition,examples])

    #------------------------write----------------------
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    flashcard_file = open(f"{out_path}/{word}.md",'w',encoding="utf-8")
    content = f'## {title}  \n---\n![sound]({sound_link})  \n---\n'
    index = 1
    for sense in Senses:
        
        for eg,s in sense[1]:
            content+=f'- {eg}  \n'
            content+=f'    ![sound]({s})\n---\n'

        content+=f'---\n### {str(index)+"." if len(Senses)>1 else ""}{sense[0]}  \n---\n'
        

        index+=1
    
    print(style.CYAN + f"\t--> {word}:  {Senses[0][0]} \n")

    flashcard_file.write(content)
    print(style.GREEN + f' << {word} >> added')
    count = 0
    while True:
        print(style.YELLOW + f"\nWould you want an example ?({len(Senses[0][1])-count} remains) (y/n)")
        choice = input().strip().lower()
        if choice =='y':
            if len(Senses[0][1])<=count:
                return
            eg_s = Senses[0][1][count]
            print(style.GREEN + f"{eg_s[0]}")
            if eg_s[1] != None:    
                p = vlc.MediaPlayer(eg_s[1])
                p.play()
            count+=1
        else:
            return




out_path = "data\\default"
dic = enchant.Dict("en_US")

while(True):
    print(style.WHITE+
    """
    (0) Exit 
    (1) New word 
    (2) List of words 
    (3) Change Folder 
    """)
    option = input().strip()
    if not option.isnumeric():
        print(style.RED+"Enter a number")
        continue
    
    option = eval(option)
    if option == 0:
        break

    elif option == 1:
        print(style.WHITE)
        input_word = input("enter new word:\n").strip().lower()
        if dic.check(input_word)==False:
            print(style.RED+"Did you mean:")
            print(style.CYAN)
            suggestions = [f"{w}" for w in dic.suggest(input_word)]
            print(bordered(join_numbered_list(suggestions)))
            
            print(style.YELLOW)
            choice = input("Select a number or Enter to continue ")
            if choice.isnumeric() and int(eval(choice))<len(suggestions):
                make_flashcard(suggestions[int(eval(choice))].lower(),out_path)
            else:
                continue  
        else:      
            make_flashcard(input_word,out_path)
    
    elif option == 2:
        print(style.YELLOW)
        words = os.listdir(out_path)
        if len(words)<=0:
            print(style.YELLOW + "--Empty Folder--")
        else:
           print(style.CYAN +  bordered("\n".join([file.split('.')[0] for file in words])))

    elif option == 3:
        print(style.YELLOW)
        dirs = [file for file in os.listdir("data")]
        items = join_numbered_list(dirs)

        print(bordered(items))
        print(style.CYAN)
        path = input("Enter Output path: ")
        if path.isnumeric():
            index = int(path)
            if index >= len(dirs):
                print(style.RED+ "Out of range")
            else:
                out_path = "data\\"+dirs[index]
        else:
            out_path = "data\\"+path
    else:
        print(style.RED+"Choose from options")

