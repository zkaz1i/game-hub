from flask import Flask, render_template, request
from flask import session
import random

app = Flask(__name__)

number_to_guess = random.randint(1, 100)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    global number_to_guess
    result = None

    if request.method == 'POST':
        try:
            user_guess = int(request.form['user_guess'])
            if user_guess < number_to_guess:
                result = 'Try a higher number.'
            elif user_guess > number_to_guess:
                result = 'Try a lower number.'
            else:
                result = f'Congratulations! You guessed the correct number {number_to_guess}! Play Again?'

                number_to_guess = random.randint(1, 100)
        except ValueError:
            result = 'Please enter a valid number.'

    return render_template('guess.html', result=result)

@app.route('/rps', methods=['GET', 'POST'])
def rps():
    result = None
    if request.method == 'POST':
        user_choice = request.form['choice']
        computer_choice = random.choice(['rock', 'paper', 'scissors'])
        
        if user_choice == computer_choice:
            result = f"It's a tie! Both chose {user_choice}. Play again?"

        elif (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'paper' and computer_choice == 'rock') or
            (user_choice == 'scissors' and computer_choice == 'paper')
        ):
            result = f"You win! You chose {user_choice} and the computer chose {computer_choice}. Play Again?"
        
        else:
            result = f"You lose! You chose {user_choice} and the computer chose {computer_choice}. Play Again?"
    return render_template('rps.html', result=result)

app.secret_key = 'sipersecretkey123'

words_list = ['PYTHON', 'FLASK', 'HANGMAN', 'GAME', 'RANDOM', 'GUESS', 'MOVIES', 'WORDLE', 'ANJUMAN', 'COMPUTER', 'PROGRAMMING', 'PROJECT', 'REQUEST', 'LOCKET', 'ISLAND', 'TELEVISION', 'RYZEN', 'FLASK', 'MODULE', 'MOBILE', 'LAPTOP', 'BEAUTIFUL', 'INVIGORATING', 'COWARD', 'PERFECTIONIST', 'MYRRH']

@app.route('/hangman', methods=['GET', 'POST'])
def hangman():
    if 'word' not in session:
        session['word'] = random.choice(words_list)
        session['guessed_letters'] = []
        session['wrong_guesses'] = 0

    word = session['word']
    guessed_letters = session['guessed_letters']
    wrong_guesses = session['wrong_guesses']
    message = None

    if request.method == 'POST':
        letter = request.form['letter'.lower()]
        if letter not in guessed_letters:
            guessed_letters.append(letter)
            if letter not in word:
                wrong_guesses += 1
        session['guessed_letters'] = guessed_letters
        session['wrong_guesses'] = wrong_guesses
        
    display_word = ' '.join([c if c in guessed_letters else '_' for c in word])

    if '_' not in display_word:
        message = f'You win! The word was "{word}"'
        session.pop('word')
        session.pop('guessed_letters')
        session.pop('wrong_guesses')
    elif wrong_guesses >= 6:
        message = f'Game Over! The word was "{word}"'
        session.pop('word')
        session.pop('guessed_letters')
        session.pop('wrong_guesses')

    return render_template('hangman.html',
                           display_word=display_word,
                           wrong_guesses=wrong_guesses,
                           guessed_letters=guessed_letters,
                           message=message)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)