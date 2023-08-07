

import random
import time


class Game:

    def __init__(self, n_rounds: int = 2):
        self.n_rounds = n_rounds

    def play(self):
        self.start_game()

        for i in range(self.n_rounds):
            self.play_one_round()

        self.end_game()

    def get_word(self):
        words = """
        Differences with the United Kingdom meant France faced the War of the Third Coalition by 1805. Napoleon shattered this coalition with victories in the Ulm campaign, and at the Battle of Austerlitz, which led to the dissolution of the Holy Roman Empire. In 1806, the Fourth Coalition took up arms against him. Napoleon defeated Prussia at the battles of Jena and Auerstedt, marched the Grande Armée into Eastern Europe, and defeated the Russians in June 1807 at Friedland, forcing the defeated nations of the Fourth Coalition to accept the Treaties of Tilsit. Two years later, the Austrians challenged the French again during the War of the Fifth Coalition, but Napoleon solidified his grip over Europe after triumphing at the Battle of Wagram.
        """.replace(".", "").replace(",", "").lower().split(" ")
        return random.choice(words)

    def get_word_longer_than(self, n=0):
        word = ""
        while not(len(word) > n):
            word = self.get_word()
        return word

    def collect_word(self, word_target: str):
        print("Slovo k opsani je:", word_target)
        collected_word = ""
        while collected_word != word_target:
            collected_word = input("Zadejte slovo:")
        return collected_word

    def end_game(self):
        print("Gratulujeme, vyhral jste!")
        print("Trvalo vam to", time.time() - self.t0)

    def start_game(self):
        print("Vitejte v nasi hre, good luck")
        self.t0 = time.time()

    def play_one_round(self):
        word = self.get_word_longer_than(5)
        self.collect_word(word)
