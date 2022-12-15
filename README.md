# Mochi_longman
A simple python script to retrieve words from Longman dictionary and turn them into Mochi markdown flashcard type

![mochi_flash_bash](https://user-images.githubusercontent.com/52382093/207743984-3b1757d1-13ed-4fc2-abb3-5a720dbf9b48.PNG)
![mochi_side](https://user-images.githubusercontent.com/52382093/207744386-6ec66255-da69-40a6-a58a-468b3f0ac1c7.PNG)

### Whats this?
- saves words as markdown flashcards
- retrieve the pronunciation, examples, etc.
- gets all the defenitions
- easy to use with git-bash
- very colorful


### How to install  
pip these:  
```
pip install pyenchant

pip install beautifulsoup4

pip install requests

pip install lxml
```
### How to use  

the script saves all flashcards on `data\default`  
- run `run.bat`
- choose to add a new word 
- import the flashcards from mochi as markdown

#### Note: sequence for each word is 
- word
- pronunciation
- examples
- definition
and then the same repeats for other definitions
