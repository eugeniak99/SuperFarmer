# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, session, request, redirect

import random
from math import floor

app = Flask(__name__)
app.secret_key = 'somuchsecrets'
gamesAll = {}
gameId = 1


@app.route("/")
def main():  
    return render_template('index.html')

class Player:
    def __init__(self):
        self.herd = {'rabbit': 1, 'sheep': 0, 'pig': 0, 'cow': 0, 'horse': 0, 'smallDog': 0, 'bigDog': 0}
    name = str()
        
@app.route("/imiona", methods = ['GET', 'POST'])
def NamesHotseat():
    global firstPlayer
    global secondPlayer
    global gamesAll
    global gameId
    GetReady()
    if request.method == 'POST':
        form = request.form
        
        gamesAll[session['game']]['1'].name = form['username1']
        gamesAll[session['game']]['2'].name = form['username2']

        return redirect("/game")        
    return render_template('form.html') 

@app.route("/imie", methods = ['GET', 'POST'] )
def NameComputer():
    global firstPlayer
    global secondPlayer
    global gamesAll
    global gameId
    GetReady()
    if request.method == 'POST':
    
        form = request.form
        gamesAll[gameId]['1'].name = form['username']
        gamesAll[gameId]['2'].name = 'Komputer'
    
        return redirect("/gameComputer")
    return render_template("form2.html")

@app.route("/imie1", methods = ['GET', 'POST'] )
def NameFirstNet():
    global firstPlayer
    global secondPlayer
    global gamesAll
    global gameId
    GetReady()
    if request.method == 'POST':
        form = request.form
        gamesAll[gameId]['1'].name = form['username']
        return redirect(url_for('CreateNewGame'))
    return render_template("form2.html")

@app.route("/imie2", methods = ['GET', 'POST'])
def NameSecondNet():
    global firstPlayer
    global secondPlayer
    global gamesAll
    gameId = request.args.get('gameId')
    if request.method == 'POST':
        form = request.form
        gamesAll[int(gameId)]['2'].name = form['username']
        return redirect(url_for('JoinExistingGame', gameId = gameId))
    return render_template("form2.html", gamesAll = gamesAll, gameId = gameId)

@app.route("/dolacz")
def JoinNetwork():
    global gamesAll
    return render_template("network.html", gamesAll = gamesAll)

@app.route("/newgame")
def CreateNewGame():
    global gamesAll
    global gameId
    session['game'] = int(gameId)
    gamesAll[session['game']]['network'] = True
    session['player'] = gamesAll[int(gameId)]['1'].name
    return render_template('wait.html', game = gamesAll[session['game']])


@app.route("/join")
def JoinExistingGame():
    global gamesAll
    global game
    global gameId
    global secondPlayer
    gameId = request.args.get('gameId')
    #if gamesAll[int(gameId)]['both'] == False:
    session['player'] = gamesAll[int(gameId)]['2'].name
    session['game'] = int(gameId)
    gamesAll[session['game']]['both'] = True
    gamesAll[session['game']]['began'] = True
    game = gamesAll[session['game']]
    game['both'] = True
    return redirect(url_for('WaitForMyTurn'))

@app.route("/zacznij")
def StartYourGame():
    global gamesAll
    global gameId
    game_id = request.args.get('gameId')
    #if gamesAll[int(game_id)] == gamesAll[session['game']]:
    if gamesAll[session['game']]['began'] == True:
        gameId = int(gameId) + 1
        return render_template('plansza.html', game = gamesAll[session['game']])


@app.route("/oczekuj")    
def WaitForMyTurn():
    global gamesAll
    
    game = gamesAll[session['game']]
    first_animal = request.args.get('first_animal')
    second_animal = request.args.get('second_animal')
    if Winner(game['1']) or Winner(game['2']) :
        return render_template('winner.html', winner = game['current'])
    if gamesAll[session['game']]['current'].name == session['player']:
        return render_template('plansza.html', game = gamesAll[session['game']])
    return render_template('wait_your_turn.html', game = game, first_animal = first_animal, second_animal = second_animal)
      
   
def GetReady():
    global game
    global gamesAll
    global gameId
    global computer
    firstPlayer = Player() 
    secondPlayer = Player()
    game = {'id': gameId, '1': firstPlayer, '2': secondPlayer, 'primary': {'rabbit': 58, 'sheep': 24, 'pig': 20, 'cow': 12, 'horse': 6, 'smallDog': 4, 'bigDog': 2}, 'current': firstPlayer, 'computer': False, 'network': False, 'both': False, 'began': False}
    gamesAll[gameId] = game
    session['game'] = gameId
       
    
@app.route("/game") 
def StartHotseat():
    global firstPlayer
    global secondPlayer
    global game
    global gamesAll  
    global gameId
    gameId += 1    
    return render_template("plansza.html", game = gamesAll[session['game']])


@app.route("/gameComputer")
def StartComputer():
    global game
    global firstPlayer
    global secondPlayer
    global strategy
    global gameId
    game['computer'] = True
    strategy = random.choice(range(1, 4))
    gameId += 1
    return render_template("plansza.html", game = game, strategy = strategy)

@app.route("/<rzut>")
def Tour(rzut):
    global game
    global firstPlayer
    global secondPlayer
    global strategy
    if rzut == 'Dicehotseat':
        game = gamesAll[session['game']]
        firstPlayer = game['1']
        secondPlayer = game['2']
        if game['current'] == firstPlayer and game['computer'] == False:
            result = ThrowDice(game['current'])
            if Winner(game['current']):
                return render_template("winner.html", winner = game['current'])
            else:
                game['current'] = secondPlayer
               
        elif game['current'] == secondPlayer and game['computer'] == False:
            result = ThrowDice(game['current'])
            if Winner(game['current']):
                return render_template("winner.html", winner = game['current'])
            else:
                game['current'] = firstPlayer
              
        elif game['current'] == firstPlayer and game['computer'] == True:
            result = ThrowDice(game['current'])
            if Winner(game['current']):
                return render_template("winner.html", winner = game['current'])
            else:
                game['current'] = secondPlayer 
        elif game['current'] == secondPlayer and game['computer'] == True:
            result = ThrowDice(game['current'])
            if Winner(game['current']):
                return render_template("winner.html", winner = game['current'])
            else:
                ComputerStrategies(strategy)
                game['current'] = firstPlayer
                redirect("/gameComputer")
        
        return render_template('plansza.html', game = game, first_animal = result[0],  second_animal = result[1], secondPlayer = secondPlayer)
                    
    if rzut == 'DiceNet' and gamesAll[session['game']]['network'] == True:
        game = gamesAll[session['game']]
        firstPlayer = game['1']
        secondPlayer = game['2']
        if game['current'] == firstPlayer and game['computer'] == False:
            result = ThrowDice(game['current'])
            if Winner(game['current']):
                return render_template("winner.html", winner = game['current'])
            else:
                game['current'] = secondPlayer
                
               
        elif game['current'] == secondPlayer and game['computer'] == False:
            result = ThrowDice(game['current'])
            if Winner(game['current']):
                return render_template("winner.html", winner = game['current'])
            else:
                game['current'] = firstPlayer
                
        return redirect(url_for('WaitForMyTurn', first_animal = result[0], second_animal = result[1]))
       
    
    #return render_template('plansza.html', game = game, first_animal = result[0],  second_animal = result[1], secondPlayer = secondPlayer)

def ComputerStrategies(strategy):
    primaryHerd = game['primary']
    #inwestowanie w konia --> zamieniam zaraz zwierzątka jak mam więcej o jedno by dojsc do konia
    if strategy == 1:
        
        if game['2'].herd['rabbit'] > 6 and primaryHerd['sheep'] > 0:
            Barter(1)
        if game['2'].herd['sheep'] > 3 and primaryHerd['pig'] > 0:
            Barter(2)
        if game['2'].herd['pig'] > 3 and primaryHerd['cow'] > 0:
            Barter(4)
        if game['2'].herd['cow'] > 2 and primaryHerd['horse'] > 0:
            Barter(6)
        if game['2'].herd['horse'] > 1:
            Barter(8)
            Barter(7)
            Barter(5)
            Barter(3)
    
    # inwestowanie w króliki i małe psy
    if strategy == 2:
        if game['2'].herd['smallDog'] < 2:
            if game['2'].herd['sheep'] > 1 and game['2'].herd['rabbit'] > 10:
                Barter(9)
            if game['2'].herd['sheep'] < 1 and game['2'].herd['rabbit'] > 15:
                Barter(1)
                Barter(9)
        if game['2'].herd['sheep'] < 1 and game['2'].herd['rabbit'] > 15:
                Barter(1)
        if floor(game['2'].herd['rabbit'] / 2) > primaryHerd['rabbit']:
            Barter(1)
            Barter(1)
        if game['2'].herd['rabbit'] == 60:
            Barter(1)
            Barter(1)
            Barter(1)
            Barter(1)
            
    # nieparzysta liczba zwierzat każdego gatunku (prócz królików bo to się nie opłaca) + ochrona dużych zwierząt
    if strategy == 3:
        if game['2'].herd['sheep'] != 1 and game['2'].herd['sheep'] % 2 == 0:
            if game['2'].herd['rabbit'] > 10:
                if game['2'].herd['sheep'] < 1:
                    Barter(1)
                    Barter(9)
                else:
                    Barter(9)
            else: 
                Barter(3)
        if game['2'].herd['pig'] != 1 and game['2'].herd['pig'] % 2 == 0:
            Barter(4)
        if game['2'].herd['cow'] != 1 and game['2'].herd['cow'] % 2 == 0:
            if game['2'].herd['sheep'] > 5 or game['2'].herd['pig'] > 3:
                Barter(10) #jesli duzo zwierzat(nie królików)  kup duzego psa
            else:
                Barter(7) # jesli nie to zamien krowe na swinie

def ThrowDice(currentPlayer):
    global game
    global gamesAll
    primaryHerd = gamesAll[session['game']]['primary']
    redDice = ['rabbit', 'rabbit', 'rabbit','rabbit','rabbit','rabbit', 'sheep', 
       'sheep','pig', 'pig', 'horse', 'fox']
    blueDice = ['rabbit', 'rabbit', 'rabbit','rabbit','rabbit','rabbit', 'sheep', 
       'sheep','pig', 'pig', 'cow', 'wolf']
    firstAnimal = random.choice(redDice)
    secondAnimal = random.choice(blueDice)
    #jesli wilk i lis, sprawdz czy jest duzy lub maly pies. Lis zabiera kroliki procz jednego 
    #wilk zabiera wszystko prócz konia, królików i małego psa (jesli ma). Duzy pies nie chroni przed lisem
    if firstAnimal == 'fox' and secondAnimal == 'wolf':
        if currentPlayer.herd['bigDog'] > 0:
            currentPlayer.herd['bigDog'] -= 1
            primaryHerd['bigDog'] += 1
            
        else:
            primaryHerd['sheep'] += currentPlayer.herd['sheep'] 
            currentPlayer.herd['sheep'] = 0
            primaryHerd['pig'] += currentPlayer.herd['pig'] 
            currentPlayer.herd['pig'] = 0
            primaryHerd['cow'] += currentPlayer.herd['cow'] 
            currentPlayer.herd['cow'] = 0
            if currentPlayer.herd['smallDog'] > 0:
                currentPlayer.herd['smallDog'] -= 1
                primaryHerd['smallDog'] += 1
            else:
                if currentPlayer.herd['rabbit'] > 1:
                    primaryHerd['rabbit'] += currentPlayer.herd['rabbit'] 
                    currentPlayer.herd['rabbit'] = 0
                    primaryHerd['rabbit'] -= 1
                    currentPlayer.herd['rabbit'] += 1
                         
    elif firstAnimal == 'fox' and secondAnimal != 'wolf':
        if currentPlayer.herd['smallDog'] > 0:
                currentPlayer.herd['smallDog'] -= 1
                primaryHerd['smallDog'] += 1
        else:
            if currentPlayer.herd['rabbit'] > 1:
                primaryHerd['rabbit'] += currentPlayer.herd['rabbit'] 
                currentPlayer.herd['rabbit'] = 0
                primaryHerd['rabbit'] -= 1
                currentPlayer.herd['rabbit'] += 1
            if secondAnimal != 'rabbit':
                if currentPlayer.herd[secondAnimal] > 1:
                  if primaryHerd[secondAnimal] >= floor(currentPlayer.herd[secondAnimal] / 2):
                      add = floor(currentPlayer.herd[secondAnimal] / 2)
                      currentPlayer.herd[secondAnimal] += add
                      primaryHerd[secondAnimal] -= add
                  else:
                      currentPlayer.herd[secondAnimal] += primaryHerd[secondAnimal]
                      primaryHerd[secondAnimal] -= primaryHerd[secondAnimal]
                 
                elif currentPlayer.herd[secondAnimal] == 1:
                    if primaryHerd[secondAnimal] >= 1:
                       currentPlayer.herd[secondAnimal] += 1
                       primaryHerd[secondAnimal] -= 1
                    
    
    elif firstAnimal != 'fox' and secondAnimal == 'wolf':
        if currentPlayer.herd['bigDog'] > 0:
            currentPlayer.herd['bigDog'] -= 1
            primaryHerd['bigDog'] += 1
        else:
           primaryHerd['sheep'] += currentPlayer.herd['sheep'] 
           currentPlayer.herd['sheep'] = 0
           primaryHerd['pig'] += currentPlayer.herd['pig'] 
           currentPlayer.herd['pig'] = 0
           primaryHerd['cow'] += currentPlayer.herd['cow'] 
           currentPlayer.herd['cow'] = 0
           if firstAnimal == 'rabbit':
               if currentPlayer.herd[firstAnimal] > 1:
                   if primaryHerd[firstAnimal] >= floor(currentPlayer.herd[firstAnimal] / 2):
                       add = floor(currentPlayer.herd[firstAnimal] / 2)
                       currentPlayer.herd[firstAnimal] += add
                       primaryHerd[firstAnimal] -= add
                   else:
                      currentPlayer.herd[firstAnimal] += primaryHerd[firstAnimal]
                      primaryHerd[firstAnimal] -= primaryHerd[firstAnimal]
               elif currentPlayer.herd[firstAnimal] == 1:
                    if primaryHerd[firstAnimal] >= 1:
                       currentPlayer.herd[firstAnimal] += 1
                       primaryHerd[firstAnimal] -= 1  
    
    
    elif firstAnimal != 'fox' and secondAnimal != 'wolf':
       if firstAnimal == secondAnimal:
        if primaryHerd[firstAnimal] >= 1:
            currentPlayer.herd[firstAnimal] += 1
            primaryHerd[firstAnimal] -= 1
       elif firstAnimal != secondAnimal:
           if currentPlayer.herd[firstAnimal] > 1:
               if primaryHerd[firstAnimal] >= floor(currentPlayer.herd[firstAnimal] / 2):
                   add = floor(currentPlayer.herd[firstAnimal] / 2)
                   currentPlayer.herd[firstAnimal] += add
                   primaryHerd[firstAnimal] -= add
               else:
                      currentPlayer.herd[firstAnimal] += primaryHerd[firstAnimal]
                      primaryHerd[firstAnimal] -= primaryHerd[firstAnimal]
           elif currentPlayer.herd[firstAnimal] == 1:
               if primaryHerd[firstAnimal] >= 1:
                   currentPlayer.herd[firstAnimal] += 1
                   primaryHerd[firstAnimal] -= 1
           if currentPlayer.herd[secondAnimal] > 1:
               if primaryHerd[secondAnimal] >= floor(currentPlayer.herd[secondAnimal] / 2):
                   add = floor(currentPlayer.herd[secondAnimal] / 2)
                   currentPlayer.herd[secondAnimal] += add
                   primaryHerd[secondAnimal] -= add
               else:
                      currentPlayer.herd[secondAnimal] += primaryHerd[secondAnimal]
                      primaryHerd[secondAnimal] -= primaryHerd[secondAnimal]
           elif currentPlayer.herd[secondAnimal] == 1:
               if primaryHerd[secondAnimal] >= 1:
                   currentPlayer.herd[secondAnimal] += 1
                   primaryHerd[secondAnimal] -= 1
                
    return firstAnimal, secondAnimal

@app.route('/wymiana/<int:typie>', methods=['GET', 'POST'])
def Barter(typie):
    global game
    currentPlayer = game['current']
    primaryHerd = game['primary']
    
    if typie == 1: # króliki na owcę
        if  currentPlayer.herd['rabbit'] >= 6:
            currentPlayer.herd['rabbit'] -= 6
            primaryHerd['rabbit'] += 6
            currentPlayer.herd['sheep'] += 1
            primaryHerd['sheep'] -= 1
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
    
    if typie == 2: # owce na swinię
        if currentPlayer.herd['sheep'] >= 2:
            currentPlayer.herd['sheep'] -= 2
            primaryHerd['sheep'] += 2
            currentPlayer.herd['pig'] += 1
            primaryHerd['pig'] -= 1
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
    
    if typie == 3: # owca na kroliki
        if currentPlayer.herd['sheep'] > 0:
            currentPlayer.herd['sheep'] -= 1
            primaryHerd['sheep'] += 1
            currentPlayer.herd['rabbit'] += 6
            primaryHerd['rabbit'] -= 6
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
    
    if typie == 4: # swinie na krowę
        if currentPlayer.herd['pig'] >= 3:
            currentPlayer.herd['pig'] -= 3
            primaryHerd['pig'] += 3
            currentPlayer.herd['cow'] += 1
            primaryHerd['cow'] -= 1
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
    
    if typie == 5: # swinia na owce
        if currentPlayer.herd['pig'] > 0:
            currentPlayer.herd['pig'] -= 1
            primaryHerd['pig'] += 1
            currentPlayer.herd['sheep'] += 2
            primaryHerd['sheep'] -= 2
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
    
    if typie == 6: # krowy na konie
        if currentPlayer.herd['cow'] >= 2:
            currentPlayer.herd['cow'] -= 2
            primaryHerd['cow'] += 2
            currentPlayer.herd['horse'] += 1
            primaryHerd['horse'] -= 1
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
   
    if typie == 7: #krowa na swinie
        if currentPlayer.herd['cow'] > 0:
            currentPlayer.herd['cow'] -= 1
            primaryHerd['cow'] += 1
            currentPlayer.herd['pig'] += 3
            primaryHerd['pig'] -= 3
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
                  
    if typie == 8: #koń na krowy
        if currentPlayer.herd['horse'] >=1:
            currentPlayer.herd['horse'] -=1
            primaryHerd['horse'] += 1
            primaryHerd['cow'] -= 2
            currentPlayer.herd['cow'] += 2
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
   
    if typie == 9: # owca na małego psa
        if primaryHerd['smallDog'] > 0:
            if currentPlayer.herd['sheep'] >= 1:
                currentPlayer.herd['sheep'] -= 1
                primaryHerd['sheep'] += 1
                primaryHerd['smallDog'] -= 1
                currentPlayer.herd['smallDog'] += 1
                if Winner(currentPlayer):
                    return render_template("winner.html", winner = currentPlayer)
                
    if typie == 10: # krowa na dużego psa
        if primaryHerd['bigDog'] > 0:
            if currentPlayer.herd['cow'] >= 1:
                currentPlayer.herd['cow'] -= 1
                primaryHerd['cow'] += 1
                primaryHerd['bigDog'] -= 1
                currentPlayer.herd['bigDog'] += 1
                if Winner(currentPlayer):
                    return render_template("winner.html", winner = currentPlayer)
                
            
    if typie == 11: # mały pies na owcę
        if currentPlayer.herd['smallDog'] > 0:
            currentPlayer.herd['smallDog'] -= 1
            primaryHerd['smallDog'] += 1
            primaryHerd['sheep'] -= 1
            currentPlayer.herd['sheep'] += 1
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
     
    if typie == 12: # duży pies na krowę
         if currentPlayer.herd['bigDog'] > 0:
            currentPlayer.herd['bigDog'] -= 1
            primaryHerd['bigDog'] += 1
            primaryHerd['cow'] -= 1
            currentPlayer.herd['cow'] += 1
            if Winner(currentPlayer):
                return render_template("winner.html", winner = currentPlayer)
    return render_template('plansza.html', game = game)


def Winner(currentPlayer):
    if currentPlayer.herd['rabbit'] >= 1 and currentPlayer.herd['sheep'] >= 1 and currentPlayer.herd['pig'] >= 1 and currentPlayer.herd['cow'] >= 1 and currentPlayer.herd['horse'] >= 1:
        return True
    else:
        return False
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5111, debug = True)
