import random
from collections import defaultdict
import pickle

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.model = defaultdict(list)

    def train(self, text):
        words = text.split()
        if len(words) < self.order:
            return
        
        for i in range(len(words) - self.order):
            state = tuple(words[i:i + self.order])
            next_word = words[i+self.order]
            self.model[state].append(next_word)

    def predict_next(self, state):
        """Retrn probability distributio for next words."""
        candidates = self.model.get(state, [])
        if not candidates:
            return None
        total = len(candidates)
        # probs = {}
        # for word in candidates:
        #     probs[word] = probs.get(word, 0) + 1
        # for word in probs:
        #     probs[word] /= total
        # return probs
        freq = {}
        for w in candidates:
            freq[w] = freq.get(w,0) + 1
        
        return {word: count / total for word, count in freq.items()}
    
    def generate(self, start, length=50):
        state = tuple(start.split()[-self.order:])
        result = list(state)

        for _ in range(length):
            next_words = self.model.get(state, [])
            if not next_words:
                break
            next_word = random.choice(next_words)
            result.append(next_word)
            state = tuple(result[-self.order:])
        return " ".join(result)
    
    def save(self, path="model.pkl"):
        with open(path, "wb") as f:
            pickle.dump((self.order, self.model), f)

    def load(self, path="model.pkl"):
        with open(path, "rb") as f:
            self.order, self.model = pickle.load(f)