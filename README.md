# Tic-Tac-Toe App

A web-based Tic-Tac-Toe game where you can play against various AI opponents of different difficulty levels.

## Features

- **5 AI Opponents** ranked by difficulty:
  1. **Random** - Picks moves randomly (easiest)
  2. **Goal-Based** - Wins if possible, blocks your wins, otherwise random
  3. **Utility-Based** - Evaluates board positions using a utility function
  4. **Minimax** - Uses the minimax algorithm for optimal play
  5. **Alpha-Beta** - Minimax with alpha-beta pruning (hardest/most efficient)

- Choose who goes first (you or AI)
- Dark-themed UI with neon accents
- Responsive design

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Open your browser to `http://localhost:5000`

## Project Structure

```
├── app.py              # Flask web server
├── game.py             # Core game logic and AI players
├── index.html          # Web UI
├── requirements.txt    # Python dependencies
```
