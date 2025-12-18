"""
Flask web application for Tic-Tac-Toe.
"""
from flask import Flask, jsonify, request, session, send_file
from game import Board, get_player, get_player_info
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/api/players')
def players():
    """Get list of available AI players."""
    return jsonify(get_player_info())


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game."""
    data = request.json
    player_type = data.get('playerType', 'random')
    human_first = data.get('humanFirst', True)
    
    session['board'] = [None] * 9
    session['player_type'] = player_type
    session['human_mark'] = 'X' if human_first else 'O'
    session['ai_mark'] = 'O' if human_first else 'X'
    session['game_over'] = False
    session['winner'] = None
    
    response = {
        'board': session['board'],
        'humanMark': session['human_mark'],
        'aiMark': session['ai_mark'],
        'currentTurn': 'X',
        'gameOver': False,
        'winner': None,
    }
    
    # If AI goes first, make AI move
    if not human_first:
        board = Board(session['board'])
        ai = get_player(player_type, session['ai_mark'])
        ai_move = ai.get_move(board)
        board.mark_space(ai_move, session['ai_mark'])
        session['board'] = board.spaces
        response['board'] = board.spaces
        response['aiMove'] = ai_move
        response['currentTurn'] = session['human_mark']
    
    return jsonify(response)


@app.route('/api/move', methods=['POST'])
def make_move():
    """Human makes a move, AI responds."""
    if session.get('game_over'):
        return jsonify({'error': 'Game is already over'}), 400
    
    data = request.json
    position = data.get('position')
    
    if position is None or not (0 <= position < 9):
        return jsonify({'error': 'Invalid position'}), 400
    
    board = Board(session['board'])
    
    if not board.is_open_space(position):
        return jsonify({'error': 'Space is already taken'}), 400
    
    # Human move
    human_mark = session['human_mark']
    board.mark_space(position, human_mark)
    session['board'] = board.spaces
    
    response = {
        'board': board.spaces,
        'humanMove': position,
        'gameOver': False,
        'winner': None,
        'aiMove': None,
    }
    
    # Check if human won
    if board.has_win(human_mark):
        session['game_over'] = True
        session['winner'] = 'human'
        response['gameOver'] = True
        response['winner'] = 'human'
        return jsonify(response)
    
    # Check for draw
    if board.is_full():
        session['game_over'] = True
        session['winner'] = 'draw'
        response['gameOver'] = True
        response['winner'] = 'draw'
        return jsonify(response)
    
    # AI move
    ai_mark = session['ai_mark']
    ai = get_player(session['player_type'], ai_mark)
    ai_move = ai.get_move(board)
    board.mark_space(ai_move, ai_mark)
    session['board'] = board.spaces
    
    response['board'] = board.spaces
    response['aiMove'] = ai_move
    
    # Check if AI won
    if board.has_win(ai_mark):
        session['game_over'] = True
        session['winner'] = 'ai'
        response['gameOver'] = True
        response['winner'] = 'ai'
        return jsonify(response)
    
    # Check for draw
    if board.is_full():
        session['game_over'] = True
        session['winner'] = 'draw'
        response['gameOver'] = True
        response['winner'] = 'draw'
        return jsonify(response)
    
    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

