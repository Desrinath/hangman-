from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

words = ["hangman", "javascript", "programming", "computer", "keyboard", "internet"]

def initialize_game():
    chosen_word = random.choice(words).upper()
    guesses_left = 6
    guessed_letters = set()
    display_word = ['_' if letter.isalpha() else letter for letter in chosen_word]
    return chosen_word, guesses_left, guessed_letters, display_word

@app.route('/')
def index():
    chosen_word, guesses_left, guessed_letters, display_word = initialize_game()
    return render_template('index.html', chosen_word=chosen_word, guesses_left=guesses_left, display_word=display_word)

@app.route('/guess', methods=['POST'])
def guess():
    letter = request.form['letter']
    chosen_word = request.form['chosen_word']
    guesses_left = int(request.form['guesses_left'])
    guessed_letters = set(request.form['guessed_letters'])
    display_word = list(request.form['display_word'])
    
    if letter not in guessed_letters:
        guessed_letters.add(letter)
        if letter not in chosen_word:
            guesses_left -= 1
        else:
            for i, char in enumerate(chosen_word):
                if char == letter:
                    display_word[i] = letter

    return jsonify({
        'guesses_left': guesses_left,
        'guessed_letters': list(guessed_letters),
        'display_word': display_word,
        'game_over': '_' not in display_word or guesses_left == 0
    })

if __name__ == '__main__':
    app.run(debug=True)
