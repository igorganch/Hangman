import random
import pymongo 
from pymongo import MongoClient





class Player:
    def __init__(this, name, guesses, errors) :
        this.name = name
        this.guesses = len(guesses)
        this.errors = len(errors)
        this.score = 110 
    def calculateScore(this):

        this.score =  this.score - (this.errors * 10) 

    def printScore(this):
        print("Player : " + this.name + "\n" + "Score : " + str(this.score) + "/110" + "\n" + "Guesses : " + str(this.guesses) + "\nErrors : " + str(this.errors))    


def create_collection():
    client = pymongo.MongoClient("mongodb+srv://iganch:325343945@cluster0.arzco.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    db = client["test"] 

    dblist = client.list_database_names()

    col = db["hangmanscores"]   

    return col 


def connect_mongodb() :
    client = pymongo.MongoClient("mongodb+srv://iganch:325343945@cluster0.arzco.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    col = db.hangmanscores
    return col


def insert_player(col, player):
    id = col.insert_one(player.__dict__)
    return id

def get_players(col):
    players = col.find()
    return players



def draw_stickman(errors_made) :
    global hangman_draw
    if len(errors_made) == 0 :
        print("___")
    elif len(errors_made)  == 1 :
        print(hangman_draw[21:24])
    elif len(errors_made) == 2 :
        print(  hangman_draw[13:15]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 3 :
        print(hangman_draw[6: 8] + "\n" + hangman_draw[13:15]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 4 : 
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 8] + "\n" + hangman_draw[13:15]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made)  == 5 :
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:15]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 6 : 
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:15]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 7 :
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:18]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 8 :
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:19]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 9 :
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:20]+ "\n" + hangman_draw[21:24]) 
    elif len(errors_made) == 10 :
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:20]+ "\n" + hangman_draw[21:27]) 
    elif len(errors_made) == 11 :
        print( hangman_draw[0: 5] +"\n"+ hangman_draw[6: 12] + "\n" + hangman_draw[13:20]+ "\n" + hangman_draw[21:28]) 


    







def replacer(temp_, guess_,pos_):
    if pos_  == 0:
        temp_ =  guess_ + temp_[len(guess_) : len(temp_)]
    elif pos_ > 0 and (len(guess_) + pos) == len(temp_) :
        temp_ = temp_[:pos] + guess_
    else:
        temp_ = temp[:pos] + guess_ + temp_[(pos + len(guess_)) :]
    return temp_


                 #                    Basepos
hangman_draw = "  ___\n |   O\n |  /|\\\n_|_ /\'\\"
guesses = []
duplicate = False
errors = []

collection = connect_mongodb()
get_players(collection)

print("=================")
print("=====Hangman=====")
print("=================")

start_game = input("PRESS Y TO PLAY: ")
word_equals = False

tf = False
word_list = ['anagram' , 'forest' , 'explanation', 'jupiter' , 'currency' , 'alter' , 'college' , 'mercedes']


while tf == False:
    if start_game.lower() == "y":
        tf = True
    elif start_game.lower() == "n":
        exit()
    else:
        print("TRY again")
        start_game = input("PRESS Y TO PLAY: ")

if tf == True:
    selected_word = word_list[random.randrange(0,len(word_list))]
    temp =""
    for  i in range(len(selected_word)):
      temp +=  "_"
   
temp2 = selected_word

while word_equals == False:

    draw_stickman(errors)
    for i in range(len(temp)):
        print(temp[i] , end = " ")
    print()
    print()
    guess = input("Enter a letter : ")
    if guess.lower() in guesses:
        print("You\'ve already entered this word/letter")
        continue
    elif guess.isalpha() == False:
        print("You\'re guess must be in words!")
    else : 
        guesses.append(guess.lower())
        if guess.lower() in selected_word:
               
            while(guess.lower() in selected_word) :
                pos = selected_word.find(guess.lower())
                temp = replacer(temp, guess.lower(), pos)   
                selected_word = selected_word.replace(guess.lower(), "-", 1)
            selected_word = temp2
            if temp == selected_word:
                word_equals = True
                    
        else:
            errors.append(guess.lower())
            if  len(errors) == 11:
                word_equals = True 
 
        

if len(errors) == 11:
    draw_stickman(errors)
    print("Sorry you\'ve lost, the word was " + selected_word)
else :
    print("Congrats you\'ve won !! ")

name = input("Enter your name to save score: ")
p1 = Player(name, guesses, errors)
p1.calculateScore()
p1.printScore()
new_player = insert_player(collection, p1)

print("==================Hangman Scores==================")
print("---Name------Guesses------Errors------Total Score-")
for x in collection.find().sort("score", -1):
    name = str(x["name"])
    guesses = str(x["guesses"])
    errors = str(x["errors"])
    score = str(x["score"])
    if str(new_player.inserted_id) == str(x["_id"]):
        
        print(f"--> {name.ljust(9)}{guesses.ljust(13)}{errors.ljust(12)}{score.ljust(10)}  " )
    else:
        print(f"    {name.ljust(9)}{guesses.ljust(13)}{errors.ljust(12)}{score.ljust(10)}  " )












