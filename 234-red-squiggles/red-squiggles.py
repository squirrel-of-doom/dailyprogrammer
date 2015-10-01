class Trie:

    def __init__(self):
        self.MARKER = '<'
        self.isword = False
        self.children = {}

    def insert_word(self, word, pos=0):
        if pos == len(word):
            self.isword = True
            return
        key = word[:(pos + 1)]
        if key not in self.children:
            self.children[key] = Trie()
        self.children[key].insert_word(word, pos + 1)

    def check_word(self, word, pos=0):
        if pos == len(word):
            if self.isword:
                return word.upper()
            else:
                return word
        key = word[:(pos + 1)]
        if key not in self.children:
            return key + self.MARKER + word[(pos + 1):]
        else:
            return self.children[key].check_word(word, pos + 1)


trie = Trie()
with open('enable1.txt', 'r') as all_words:
    for word in all_words:
        trie.insert_word(word)

words = ['accomodate', 'acknowlegement', 'arguemint', 'comitmment',
         'deductabel', 'depindant', 'existanse', 'forworde', 'herrass',
         'inadvartent', 'judgemant', 'ocurrance', 'parogative', 'suparseed']
for w in words:
    print(trie.check_word(w))
