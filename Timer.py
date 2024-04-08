import tkinter
from tkinter import messagebox


class Timer:
    def __init__(self, window, label, entry, words, button):
        self.seconds = 60
        self.window = window
        self.label = label
        self.words = words
        self.entry = entry
        self.score = None
        self.accuracy = None
        self.button = button

    def accuracy_checker(self):
        final_entry = self.entry.get("0.0", 'end-1c').split()
        correct = 0
        for num in range(len(final_entry)):
            if final_entry[num] == self.words[num]:
                correct += 1
        self.accuracy = int(round(correct/len(final_entry), 2)*100)

    def score_finder(self):
        words = self.entry.get("0.0", 'end-1c').split()
        self.score = len(words)

    def label_changer(self):
        self.label.configure(text=f"{self.seconds}")

    def show_score(self):
        self.score_finder()
        self.accuracy_checker()
        tkinter.messagebox.showinfo(
            "Score", f"You typed {self.score} words per minute with an accuracy of {self.accuracy}%")

    def game_over(self):
        self.seconds = 0
        self.label_changer()
        self.window.update()
        self.entry.configure(state='disabled')
        self.window.after(2000, self.show_score)

    def countdown(self):
        self.button.configure(state="disabled")
        self.entry.focus()
        if self.seconds > 1:
            self.seconds += -1
            self.label_changer()
            self.window.update()
            self.window.after(1000, self.countdown)
        else:
            self.game_over()
