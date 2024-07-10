import random
from flask import Flask, render_template
import tkinter as tk

app = Flask(__name__)


class PrizeController:
    def __init__(self, prize_dict):
        self.prize_dict = prize_dict

    def get_random_prize(self):
        prize_type = random.choice(list(self.prize_dict.keys()))
        quantity = self.prize_dict[prize_type]
        if quantity >= 1:
            return f'Congratulations on getting {prize_type}'
        else:
            return 'Opps, Participation Prize~'


@app.route('/')


def index():
    prizes = dict(input('What for prize this section: (a dict expected):'))
    prize_control = PrizeController(prizes)
    ans = prize_control.get_random_prize()
    print(ans)
    return render_template('index.html', winner=ans)


if __name__ == "__main__":
    print("hey guys")
    app.run()
