# 2048-Python-Bot
My attempt at playing 2048 with a bot written in Python. Uses screen grabbing to determine the game state and a basic tree search to calculate moves.

During tree search, the computer is simulated as an opponent that aims to create tiles in the worst possible location, and the bot picks the move that minimizes the risk of bad random placements.

Simple heuristics are used to reward good behaviors, such as keeping the top row full and keeping numbers in order so they can be combined easily.

Currently reaches 2048 a little under 50% of the time.

Screen grabbing code is taken from this excellent example, and you'll have to calculate the game coordinates to match your screen size!

http://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

