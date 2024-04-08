import Test_Library
from random import choice


class WordManager:
    def __init__(self, entry, first_label, word_label, window):
        self.first = 0
        self.last = 7
        self.words = choice(Test_Library.story_list).split()
        self.entry = entry
        self.label1 = first_label
        self.label2 = word_label
        self.window = window

    def start_up(self):
        self.label2.configure(text=self.words[self.first:self.last], font=("Serif", 15))

    def get_text(self):
        text = self.entry.get("0.0", 'end-1c').split()  # [-7:]
        return text

    def new_words(self, entry):
        line_num = (len(self.get_text())-1)//7
        self.first = 7*line_num
        self.last = self.first + 7
        self.label1.configure(text=self.words[self.first:self.last])
        self.label2.configure(text=self.words[self.first+7:self.last+7])
        self.window.update()
