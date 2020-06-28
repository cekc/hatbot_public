from collections import Counter
import texts


class Move:
    """ Implements standard Hat algorithm. """

    def __init__(self, players):
        self.players = players
        self.lead = 0
        self.target = 1

    def __next__(self):
        m = len(self.players)
        ret = (self.players[self.lead], self.players[self.target])
        self.lead = (self.lead + 1) % m
        self.target = (self.target + 1) % m
        if self.lead == 0:
            self.target = (self.target + 1) % m
            if self.target == self.lead:
                self.target = (self.target + 1) % m
        return ret

    def __iter__(self):
        return self


class Round:
    def __init__(self, word_collection, players):
        """ Word collection must implement get_word and add_word. """
        self.word_collection = word_collection
        self.players = players
        self.points = Counter()
        self.explained_points = Counter()
        self.guessed_points = Counter()
        self.move = Move(self.players)
        self._timer = None

    def start_game(self):
        if len(self.players) > 1:
            return self.__next_move()

    def start_move(self, player):
        if player == self.lead:
            return self.__next_word(player)
        else:
            return texts.not_your_turn_message

    def guessed(self, player):
        """ Increments player's points. """
        if player == self.lead:
            self.points[player] += 1
            self.explained_points[player] += 1
            self.points[self.target] += 1
            self.guessed_points[self.target] += 1
            return self.__next_word(player)
        else:
            return texts.not_your_turn_message

    def failed(self, player):
        """ Passes the turn to the next player. """
        if player == self.lead:
            return self.__next_move()
        else:
            return texts.not_your_turn_message

    def time_ran_out(self, player):
        """ Puts the word back and passes the turn. """
        if player == self.lead:
            if self.word:
                self.word_collection.add_word(self.word, player)
            return self.__next_move()
        else:
            return texts.not_your_turn_message

    def pretty_scores(self):
        most_common = self.points.most_common(len(self.players))
        player_scores = []
        for player, total_score in most_common:
            player_scores.append([player, total_score, self.explained_points[player], self.guessed_points[player]])
        return player_scores

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, timer):
        self._timer = timer

    def __next_move(self):
        """ Starts next move and returns players' names. """
        self.lead, self.target = next(self.move)
        return self.lead, self.target

    def __next_word(self, player):
        """ Returns the next word to explain. """
        if player == self.lead:
            self.word = self.word_collection.get_word()
            if self.word is None:
                return texts.no_more_words_message
            return self.word
        else:
            return texts.not_your_turn_message
