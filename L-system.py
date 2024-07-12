# This allows me to save turtle drawings as svg files.
# https://stackoverflow.com/questions/4071633/turtle-module-saving-an-image
from svg_turtle import SvgTurtle
import tkinter as tk
# Makes tkinter work with svg
# https://pypi.org/project/tksvg/
import tksvg
from random import randint

# I want to a call timeout for fractals that take too long, but the
# possible solutions I see involve asynchronous functions or multithreading.
# I could figure it out, but I think the help button along with a preset number of iterations
# provide a satisfactory solution until I can implement a better solution.


class Fractal:
    def __init__(self):
        self.artist = SvgTurtle(400, 400)
        self.artist.penup()
        self.artist.setpos(-100, 100)
        self.artist.pendown()
        self.start_heading = 0
        self.forward_dist = 10
        self.turn_angle = 90
        self.axiom = "F+F+F+F"
        self.replace_dict = {"F": "F+F-F-FF+F+F-F"}
        self.iterations = 2
        self.mirror = False
        self.line_length_scale_factor = 1

    def get_string(self):
        for i in range(int(self.iterations)):
            new_string = ""
            for char in self.axiom:
                try:
                    new_string += self.replace_dict[char]
                except KeyError:
                    new_string += char
            self.axiom = new_string

    def draw(self, filename="fractal.svg"):
        previous_path = []
        for char in self.axiom:
            if char == "F":
                self.artist.forward(self.forward_dist)
            elif char == "+":
                self.artist.right(self.turn_angle)
            elif char == "-":
                self.artist.left(self.turn_angle)
            elif char == "[":
                previous_path.append((self.artist.heading(), self.artist.pos()))
            elif char == "]":
                self.artist.penup()
                self.artist.goto((previous_path[-1][1][0], previous_path[-1][1][1]))
                self.artist.seth(previous_path[-1][0])
                previous_path.pop()
                self.artist.pendown()
            elif char == ">":
                self.forward_dist = self.forward_dist * self.line_length_scale_factor
            elif char == "<":
                self.forward_dist = self.forward_dist / self.line_length_scale_factor
        self.artist.save_as(filename)


class CustomFractal(Fractal):
    def __init__(self, axiom, dictionary, x, y, heading, angle, distance, iterations):
        super().__init__()
        self.artist = SvgTurtle(800, 700)
        self.forward_dist = distance
        self.iterations = iterations
        self.start_heading = heading
        self.artist.seth(self.start_heading)
        self.artist.penup()
        self.start_x = x
        self.start_y = y
        self.artist.setpos(self.start_x, self.start_y)
        self.artist.pendown()
        self.axiom = axiom
        self.turn_angle = angle
        self.replace_dict = dictionary


# Defined in a function, my new image was in a different scope than my window and would not show up.
# Putting it into a class fixes that and improves organization.
# https://stackoverflow.com/questions/16424091/why-does-tkinter-image-not-show-up-if-created-in-a-function
class WindowManager:
    def __init__(self):
        self.window = tk.Tk()
        self.svg_image = tksvg.SvgImage(file='fractal.svg')
        self.custom_axiom = ''
        self.custom_replacements = {}
        self.fractal_parameter_entries = []
        self.elements_to_remove = []
        self.row = 4
        self.to_save = []
        self.axiom_entry = None
        self.axiom_label = None
        self.fractal_image = None
        self.char_label = None
        self.char_entry = None
        self.char_submit = None
        self.fractal_submit = None
        self.save_button = None
        self.starting_window()

    def starting_window(self):
        self.axiom_label = tk.Label(text="Axiom")
        self.axiom_label.grid(row=0, column=0, sticky='E', padx=20, pady=(30, 0))
        self.axiom_entry = tk.Entry()
        self.axiom_entry.grid(row=0, column=1, padx=20, sticky="W", pady=(30, 0))
        self.fractal_image = tk.Label(image=self.svg_image)
        self.fractal_image.grid(row=0, column=4, rowspan=20, columnspan=3)
        reset_button = tk.Button(text='Reset', command=self.reset)
        reset_button.grid(row=21, column=4, sticky="E", padx=5, pady=5)
        help_button = tk.Button(text="Help", command=self.help)
        help_button.grid(row=21, column=5, sticky="W", padx=5, pady=5)
        self.save_button = tk.Button(text='Save', command=self.save, state=tk.DISABLED)
        self.save_button.grid(row=21, column=6, padx=5, pady=5, sticky='W')

        self.char_label = tk.Label(text="Substitutions")
        self.char_entry = tk.Entry()
        # to pass arguments into a command through a button
        # https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
        self.char_submit = tk.Button(text="Submit", command=lambda: self.get_replacements(self.char_entry.get()))
        self.char_submit.grid(row=2, column=2, sticky="N", padx=(30, 0))
        self.char_label.grid(row=0, column=2, sticky="N", padx=(30, 0), pady=(30, 0))
        self.char_entry.grid(row=1, column=2, sticky="N", padx=(30, 0))

        x_label = tk.Label(text="Starting x")
        y_label = tk.Label(text="Starting y")
        heading_label = tk.Label(text="Starting Angle")
        turn_label = tk.Label(text="Turn Angle")
        forward_label = tk.Label(text="Forward Distance")
        iter_label = tk.Label(text="Iterations")

        x_entry = tk.Entry()
        x_entry.insert(0, "0")
        y_entry = tk.Entry()
        y_entry.insert(0, "0")
        heading_entry = tk.Entry()
        heading_entry.insert(0, "0")
        turn_entry = tk.Entry()
        turn_entry.insert(0, "90")
        forward_entry = tk.Entry()
        forward_entry.insert(0, "10")
        iter_entry = tk.Entry()
        iter_entry.insert(0, "3")
        row = 1
        for label, entry in [(x_label, x_entry), (y_label, y_entry), (heading_label, heading_entry),
                             (turn_label, turn_entry), (forward_label, forward_entry), (iter_label, iter_entry)]:
            label.grid(row=row, column=0, sticky="E", padx=5)
            entry.grid(row=row, column=1)
            self.fractal_parameter_entries.append(entry)
            row += 1
        self.fractal_submit = tk.Button(text="Generate", command=self.create_fractal, state=tk.DISABLED)
        self.fractal_submit.grid(row=row, column=1, sticky="N")

    def get_replacements(self, entry):
        to_replace = []
        for char in entry:
            if char.isalpha() and char not in to_replace:
                to_replace.append(char)
        if len(to_replace) > 20:
            # don't accept
            self.char_label.configure(text="Substitutions (keep under 20)")
            return
        self.char_label.destroy()
        self.char_entry.destroy()
        self.char_submit.destroy()
        row_num = 1
        replacements = []
        for i in range(len(to_replace)):
            column = 2
            letter_label = tk.Label(text=f"{to_replace[i]} -->")
            replacement_entry = tk.Entry()
            replacements.append(replacement_entry)
            letter_label.grid(row=row_num, column=column, sticky="E")
            replacement_entry.grid(row=row_num, column=column+1, sticky="W")
            row_num += 1
            self.elements_to_remove.append(letter_label)
            self.elements_to_remove.append(replacement_entry)
        for i in range(len(to_replace)):
            self.custom_replacements[to_replace[i]] = replacements[i]
        replace_submit = tk.Button(text="Submit", command=self.get_params)
        replace_submit.grid(row=row_num, column=3)
        self.elements_to_remove.append(replace_submit)

    def get_params(self):
        self.fractal_submit['state'] = tk.ACTIVE
        label_text = ""
        for key in self.custom_replacements.keys():
            self.custom_replacements[key] = self.custom_replacements[key].get()
            corrected = ''
            for let in self.custom_replacements[key]:
                if not let.isnumeric():
                    corrected += let
            self.custom_replacements[key] = corrected
            label_text += f"{key}-->{self.custom_replacements[key]}\n"
        label_for_replacements = tk.Label(text=label_text)

        for item in self.elements_to_remove[::]:
            item.destroy()
            self.elements_to_remove.remove(item)
        label_for_replacements.grid(row=2, column=2, sticky="NW", padx=20)

    def create_fractal(self):
        self.custom_axiom = self.axiom_entry.get()
        if not self.custom_axiom:
            self.axiom_label.config(text="Axiom (Required)")
            return
        parameters = [self.custom_axiom, self.custom_replacements]
        for entry in self.fractal_parameter_entries:
            try:
                value = float(entry.get())
                parameters.append(value)
            except ValueError:
                return
        self.to_save = parameters
        new_fractal = CustomFractal(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4],
                                    parameters[5], parameters[6], parameters[7])
        new_fractal.get_string()
        new_fractal.draw(filename="fractal.svg")
        self.svg_image = tksvg.SvgImage(file='fractal.svg')
        self.fractal_image.config(image=self.svg_image)
        self.save_button['state'] = tk.ACTIVE

    def reset(self):
        for element in self.window.winfo_children():
            element.destroy()
        self.fractal_parameter_entries.clear()
        self.starting_window()

    @staticmethod
    def help():
        HelpWindow()

    def save(self):
        save_string = ""
        for i in range(len(self.to_save)):
            if i == 1:
                dict_string = ""
                for key in self.to_save[i].keys():
                    dict_string += f"{key}:{self.to_save[i][key]},"
                self.to_save[i] = dict_string.strip(',')
            save_string += f"{self.to_save[i]}, "
        with open("saved_fractals.txt", 'a') as f:
            f.write(f"\n{save_string.strip(', ')}")
        self.save_button['state'] = tk.DISABLED


class HelpWindow:
    def __init__(self):
        # Toplevel allows you to display a window over another window.
        # https://geeksforgeeks.org/python-tkinter-toplevel-widget/
        self.top = tk.Toplevel()
        self.top.geometry("300x300")
        self.top.title("Help")
        self.page_one()

    def page_one(self):
        heading = tk.Label(self.top, text="How to make it work!", justify='center')
        heading.place(x=90, y=10)
        question1 = tk.Label(self.top, justify='left', text="Nothing showing up?")
        question1.place(x=30, y=35)
        answer1 = tk.Label(self.top, justify='left',
                           text="Fill the Axiom and Replacement fields.\nMake sure all other fields are numbers only.\n"
                                "Try some examples (see help page 3).", font=('TkDefaultFont', 8))
        answer1.place(x=40, y=60)
        question2 = tk.Label(self.top, justify='left', text='Is the image too large?')
        question2.place(x=30, y=115)
        answer2 = tk.Label(self.top, justify='left', font=('TkDefaultFont', 8), wraplength=200,
                           text='Adjust starting x and y to position the image in the frame.\n'
                                'Make the forward distance smaller to decrease size.')
        answer2.place(x=40, y=140)
        meanings = tk.Label(self.top, justify='left', wraplength=250, font=('TkDefaultFont', 8),
                            text="F --> Forward\n(+) --> Turn right by turn angle\n(-) --> Turn left by turn angle\n"
                                 "[  ] --> pause and draw what's inside before continuing on.")
        meanings.place(x=30, y=205)
        left = tk.Button(self.top, text='<', state=tk.DISABLED)
        right = tk.Button(self.top, text='>', command=lambda: self.get_page(2))
        left.place(x=4, y=270)
        right.place(x=278, y=270)

    def page_two(self):
        heading = tk.Label(self.top, text="General Tips")
        heading.place(x=115, y=10)
        tip1 = tk.Label(self.top, justify='left', text="Start with a small number of iterations and go slowly as "
                                                       "fractals can get exponentially larger.", wraplength=275)
        tip1.place(x=30, y=55)
        tip2 = tk.Label(self.top, justify='left',
                        text="Try out different Turn Angles. 60, 90, and 120 seem to work best.", wraplength=260)
        tip2.place(x=30, y=105)
        tip3 = tk.Label(self.top, justify='left', wraplength=250,
                        text="Make sure at least one letter from the axiom has a replacement.")
        tip3.place(x=30, y=155)
        tip4 = tk.Label(self.top, justify='left', wraplength=250, text='Small changes can make a huge difference!')
        tip4.place(x=30, y=200)
        tip5 = tk.Label(self.top, justify='left', wraplength=250, text='X values range from -400 to 400\n'
                                                                       'Y values range from -350 to 350')
        tip5.place(x=30, y=230)
        left = tk.Button(self.top, text='<', command=lambda: self.get_page(1))
        right = tk.Button(self.top, text='>', command=lambda: self.get_page(3))
        left.place(x=4, y=270)
        right.place(x=278, y=270)

    def page_three(self):
        heading = tk.Label(self.top, text="Examples")
        heading.place(x=115, y=10)
        example1 = tk.Label(self.top, justify='left', font=('TkDefaultFont', 8),
                            text="Name: Koch Snowflake\nAxiom: F++F++F\nSubstitution: F --> F-F++F-F\nTurn Angle: 60")
        example1.place(x=30, y=40)
        example2 = tk.Label(self.top, justify='left', font=('TkDefaultFont', 8),
                            text="Name: Spiky Sierpinski\nAxiom: F\n"
                                 "Substitution: F --> F+F+F+F-\nTurn Angle: 120\nIterations: 6\n"
                                 "(Try turn angle of 160 for a C-3PO Cactus thing)")
        example2.place(x=30, y=110)
        resources = tk.Label(self.top, justify='left', font=('TkDefaultFont', 8),
                             text="Find more examples at\nhttps://paulbourke.net/fractals/lsys/")
        resources.place(x=30, y=210)
        left = tk.Button(self.top, text='<', command=lambda: self.get_page(2))
        right = tk.Button(self.top, text='>', state=tk.DISABLED)
        left.place(x=4, y=270)
        right.place(x=278, y=270)

    def get_page(self, page):
        widgets = self.top.winfo_children()
        for widget in widgets:
            widget.destroy()
        if page == 1:
            self.page_one()
        if page == 2:
            self.page_two()
        if page == 3:
            self.page_three()


try:
    with open('saved_fractals.txt') as file:
        lines = file.readlines()
# initializes some fractals for first load up. User will be able to add to file later on.
except FileNotFoundError:
    with open("saved_fractals.txt", "w") as file:
        file.write('F+F+F+F, F:F+F-F-FF+F+F-F, -100, 100, 0, 90, 10, 2\n'
                   'X, X:F-[[X]+X]+F[+FX]-X,F:FF, 0, -400, 90, 22.5, 9, 5\n'
                   'F+F+F+F, F:FF+F-F+F+FF, 50, 0, 0, 90, 15, 3\n'
                   'Y, X:X[-FFF][+FFF]FX,Y:YFX[+Y][-Y], 0, -300, 90, 25.7, 5, 6')
    with open("saved_fractals.txt") as file:
        lines = file.readlines()
finally:
    frac = lines[randint(0, len(lines) - 1)].split(", ")
    frac_dict = {}
    for string in frac[1].split(','):
        parts = string.split(':')
        frac_dict[parts[0]] = parts[1]
    for num in range(len(frac[2:])):
        # noinspection PyTypeChecker
        frac[2 + num] = float(frac[2 + num].strip('\n'))

    initial_image = CustomFractal(frac[0], frac_dict, frac[2], frac[3], frac[4], frac[5], frac[6], frac[7])
    initial_image.get_string()
    initial_image.draw()

window = WindowManager()
window.window.mainloop()
