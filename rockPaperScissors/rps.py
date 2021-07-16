from random import shuffle
import ctypes
from json import load, dump

DEBUG = True

ctypes.windll.kernel32.SetConsoleTitleW("Rock paper scissors")
decisionMaker = [] # Array of 100 elements, 1 represents fairness, 0 repreents cheating
rpsArrOriginal = ["ROCK", "PAPER", "SCISSORS"]

def mainMenu():
    while True:
        try:
            print("="*70)
            choice = int(input("1- Play\n2- Set difficulty\n3- Scores\n0- Exit\n--> "))
            if choice >= 0 and choice <=3:
                return choice
            else:
                print("Invalid choice!")
        except:
            print("Choice must be an integer!")

def login():
    un = input("Enter username: ")
    return un

def game(username, difficulty):
    decisionMaker.clear()
    if difficulty <= 0.5:
        fairnessLimit = interpolate(0, difficulty, 0.5, 0, 100)
    else:
        fairnessLimit = interpolate(0.5, difficulty, 1, 100, 0)
    for i in range(100):
        if i<=fairnessLimit:
            decisionMaker.append(1)
        else:
            decisionMaker.append(0)
    round = 0
    while True:
        try:
            print(f"Round {round}".center(50, "*"))
            choice = int(input("1- Rock\n2- Paper\n3- Scissors\n--> "))
            if choice >= 1 and choice <=3:
                with open("data.json", "r", encoding="utf-8") as fil:
                    data = load(fil)
                    if username in data["scores"]:
                        score = data["scores"][username]
                    else:
                        score = 0
                        data["scores"].update({username : score })
                score += play(rpsArrOriginal[choice - 1], difficulty)
                data["scores"].update({username : score })
                with open("data.json", "w", encoding="utf-8") as fil:
                    dump(data, fil)
            else:
                print("Invalid choice!")
        except KeyboardInterrupt:
            return 
        except Exception as ex:
            if DEBUG:
                print (ex)
            print("Choice must be an integerarg!")
        else:
            round += 1
        
def play(choice, difficulty):
    shuffle(decisionMaker)
    decision = decisionMaker[0]
    if decision == 1: # be fair
        logFairness("fairplay")
        return(fair(choice))
    else: # cheat
        if difficulty < 0.5:
            logFairness("cheating (force win)")
            return(won())
        else:
            logFairness("cheating (force lose)")
            return(lost())

def logFairness(note):
    with open("fairnessHistory.txt", "a", encoding="utf-8") as fil:
        fil.write(note + '\n')
    
def interpolate(xMin, xKnown, xMax, yMin, yMax):
    deltax = xMax - xMin
    xDifference = xKnown - xMin
    ratio = xDifference/deltax
    deltay = yMax - yMin
    y = deltay*ratio + yMin
    return y

def fair(input):
    rpsArr = ["ROCK", "PAPER", "SCISSORS"]
    shuffle(rpsArr)
    rps = rpsArr[0]
    if (input == "ROCK" and rps == "SCISSORS") or (input == "SCISSORS" and rps == "PAPER") or (input == "PAPER" and rps == "ROCK"):
        return won()
    elif input == rps:
        return tie()
    else:
        return lost()
    
def won():
    print("You won!")
    return 1
def tie():
    print("Tie!")
    return 0
def lost():
    print("You lost!")
    return -1

def setDifficulty(data):
    while True:
        try:
            choice = int(input("1- Easy\n2- Fair\n3- Hard\n4- Custom\n--> "))
            if choice == 1:
                data["difficulty"] = 0.25
                break
            elif choice == 2:
                data["difficulty"] = 0.5
                break
            elif choice == 3:
                data["difficulty"] = 0.75
                break
            elif choice == 4:
                try:
                    newDifficulty = float(input("Enter difficulty percentage: "))
                    if newDifficulty >= 0 and newDifficulty <= 100:
                        data["difficulty"] = newDifficulty/100.0
                        break
                    else:
                        print("Please enter a number between 0-100")
                except:
                    print("Please enter a number!")
            else:
                print("Invalid choice!")
        except:
            print("Choice must be an integer!")
    with open("data.json", "w", encoding="utf-8") as fil:
        dump(data, fil)
    
    difficulty = data["difficulty"]


while True:
    try:
        with open("data.json", "r", encoding="utf-8") as fil:
            data = load(fil)
        print(" ")
        print("="*70)
        print(f"Difficulty: {data['difficulty']}")
        mode = mainMenu()

        if mode == 1:
            print("Press CTRL^C to return main menu")
            game(login(), difficulty=data["difficulty"])
        elif mode == 2:
            print("Difficulty".center(70, "-"))
            setDifficulty(data)
        elif mode == 3:
            print("scores".center(70, "-"))
            scores = sorted(data["scores"].items(), key=(lambda x: x[1]), reverse=True)
            for i, playerData in enumerate(scores):
                print(f"{str(i+1).rjust(2)}-) {playerData[0]}: {playerData[1]}")
        elif mode == 0:
            break
        else:
            pass

    except KeyboardInterrupt:
        continue
    except (Exception, OSError, RuntimeError, ImportError) as ex:
        print(ex) 
