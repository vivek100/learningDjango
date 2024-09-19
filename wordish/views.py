# wordish/views.py
from django.shortcuts import render
import random
import json
from django.http import HttpResponseRedirect
import ast


WORD_LIST = ['apple', 'banana', 'cherry', 'dates', 'elder']  # Add your word list

def start_page(request):
    message = "Welcome to Wordish!"
    error = ""
    if request.method == 'POST':
        target_word = request.POST.get('target_text')
        print(target_word)
        if not target_word:
            error = "Please set a target word."
        elif not target_word.isalpha() or len(target_word) < 5 or len(target_word) > 5:
            error = "Invalid word! Please enter a word with at least 5 alphabetic characters."
        else:
            # Redirect to the game page, passing the target word in a hidden field
            game_state = {
                "target_word": target_word,
                "guesses": [],
                "max_attempts": 6,
                "attempts_left": 6,
                "game_over": False
            }
            return render(request, 'wordish/game_page.html', {
                "game_state": game_state,
                "message": "Start the game"
            })
    return render(request, 'wordish/start_page.html', {'message': message,'error': error})

def game_page(request):
    if request.method == 'POST':
        game_state_json = request.POST.get('game_state', None)
        guess = request.POST.get('guess', '').lower()
        message = "Start the game!"
        
        if not game_state_json:
            # New game start
            target_word = request.POST.get('target_word', '')
            if not target_word:
                target_word = random.choice(WORD_LIST)

            # Initialize game state
            game_state = {
                "target_word": target_word,
                "guesses": [],
                "max_attempts": 6,
                "attempts_left": 6,
                "game_over": False
            }
            message = "Start the game!"
            return render(request, 'wordish/game_page.html', {
                "game_state": game_state,
                "message": message,
            })
        else:
            # Load the game state from hidden form input
            game_state = ast.literal_eval(game_state_json)

            if game_state['attempts_left'] < 0 or game_state['game_over']:
                message = f"Game over! The word was {game_state['target_word']}."
                error = "Please come back tomorrow."
                return render(request, 'wordish/game_page.html', {
                    'game_state': game_state,
                    'message': message,
                    'error': error
                })
            elif  not guess.isalpha() or len(guess) < 5 or len(guess) > 5:
                error = "Invalid word! Please enter a word with at least 5 alphabetic characters."
                return render(request, 'wordish/game_page.html', {
                    'game_state': game_state,
                    'message': message,
                    'error': error
                })
                
            print(game_state,game_state['target_word'])
            # Check guess and color letters
            result = []
            target_word = game_state['target_word']
            used_positions = set()

            # Check for exact matches (green)
            for i, letter in enumerate(guess):
                if letter == target_word[i]:
                    idForFrontend = "cell_" + str(game_state['attempts_left'] - 6) + "_" + str(i)
                    result.append(('green', letter,idForFrontend))
                    used_positions.add(i)
                else:
                    idForFrontend = "cell_" + str(game_state['attempts_left'] - 6) + "_" + str(i)
                    result.append(('grey', letter,idForFrontend))  # Set to grey for now

            # Check for letters in the wrong position (yellow)
            for i, letter in enumerate(guess):
                if result[i][0] != 'green' and letter in target_word:
                    for j, target_letter in enumerate(target_word):
                        if target_letter == letter and j not in used_positions:
                            idForFrontend = "cell_" + str(game_state['attempts_left'] - 6) + "_" + str(i)
                            result[i] = ('yellow', letter, idForFrontend)
                            used_positions.add(j)
                            break

            # Append the guess result to the game state
            game_state['guesses'].append(result)
            game_state['attempts_left'] -= 1
            print(game_state)
            # Check win/lose conditions
            if guess == target_word:
                message = "Congratulations, you won!"
                game_state['game_over'] = True
            elif game_state['attempts_left'] == 0:
                message = f"Game over! The word was {target_word}."
            else:
                message = "Keep trying!"

            return render(request, 'wordish/game_page.html', {
                'game_state': game_state,
                'message': message,
            })

    return HttpResponseRedirect('/')
