import tkinter as tk
from tkinter import messagebox
import random


# Questions Data

questions_data = [
    ["What NBA team has the most championships?","Boston Celtics","Los Angeles Lakers","Chicago Bulls","San Antonio Spurs","A"],
    ["Which country won the FIFA World Cup in 2018?","France","Croatia","Brazil","Germany","A"],
    ["Which planet is known as the Red Planet?","Mars","Venus","Jupiter","Saturn","A"],
    ["In which country were the first modern Olympic Games held?","Greece","Italy","France","UK","A"],
    ["The Great Barrier Reef is off the coast of which country?","Australia","New Zealand","South Africa","Philippines","A"],
    ["Which boxer was known as \"The Greatest\" and \"The Louisville Lip\"?","Muhammad Ali","Mike Tyson","Floyd Mayweather","Joe Frazier","A"],
    ["Who wrote the novel 1984?","George Orwell","Aldous Huxley","Ray Bradbury","Kurt Vonnegut","A"],
    ["Which country is home to the ancient city of Petra?","Jordan","Egypt","Morocco","Turkey","A"],
    ["Which scientist developed the theory of general relativity?","Albert Einstein","Isaac Newton","Nikola Tesla","Galileo Galilei","A"],
    ["What is the main ingredient in traditional Japanese miso soup?","Soybeans","Rice","Seaweed","Tofu","A"],
    ["What year did the Titanic sink on its maiden voyage?","1912","1905","1915","1900","A"],
    ["In golf, what term describes a score of three under par on a single hole?","Albatross","Birdie","Eagle","Hole-in-one","A"],
    ["What is the chemical symbol for gold?","Au","Ag","Fe","Cu","A"],
    ["What is the longest river in Asia?","Yangtze River","Ganges","Yellow River","Mekong","A"],
    ["What is the name of the deepest known point in the Earth's oceans?","Challenger Deep","Mariana Trench","Tonga Trench","Puerto Rico Trench","A"]
]


# Classes

class Question:
    def __init__(self, text, choices, correct_letter):
        self.text = text
        self.choices = choices.copy()
        correct_answer = choices[ord(correct_letter) - ord('A')]
        random.shuffle(self.choices)
        self.answer = "ABCD"[self.choices.index(correct_answer)]

    def check_answer(self, choice):
        return choice.upper() == self.answer.upper()

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.lifelines_used = {"50/50": False, "Phone": False, "Audience": False}


# Game Logic

class Game:
    def __init__(self, root, questions):
        self.root = root
        self.root.title("Who Wants to Be a Millionaire")
        self.questions = questions
        self.current_index = 0
        self.player = None
        self.prizes = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
        self.guaranteed = {5: 1000, 10: 32000}
        self.current_choices = []
        self.money_label = None
        self.ladder_labels = []
        self.btn_5050 = None
        self.btn_phone = None
        self.btn_audience = None
        self.create_intro()


    # GUI: Intro Screen

    def create_intro(self):
        self.clear_window()
        tk.Label(self.root, text="Who Wants to Be a Millionaire", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=10)
        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        self.player = Player(name)
        self.show_question()

    
    # GUI: Question Screen

    def show_question(self):
        self.clear_window()
        if self.current_index >= len(self.questions):
            self.end_game(win=True)
            return

        self.current_question = self.questions[self.current_index]

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        ladder_frame = tk.Frame(main_frame)
        ladder_frame.pack(side=tk.RIGHT, padx=10)

        question_frame = tk.Frame(main_frame)
        question_frame.pack(side=tk.LEFT, padx=10)

        # Money Ladder
     
        self.ladder_labels.clear()
        for i in range(len(self.prizes)-1, -1, -1):
            color = "white"
            if i == self.current_index:
                color = "yellow"  
            elif i < self.current_index:
                color = "green"  
            if (i+1) in self.guaranteed:
                if color == "white":
                    color = "blue"
            label = tk.Label(ladder_frame, text=f"${self.prizes[i]}", width=10, bg=color)
            label.pack(pady=1)
            self.ladder_labels.append(label)

        self.money_label = tk.Label(question_frame, text=f"Current Money: ${self.player.score}", font=("Arial", 14))
        self.money_label.pack(pady=5)

        tk.Label(question_frame, text=f"Question {self.current_index+1}", font=("Arial", 16)).pack(pady=5)
        tk.Label(question_frame, text=self.current_question.text, wraplength=400, font=("Arial", 14)).pack(pady=10)

        # Choices Buttons
        self.current_choices = []
        letters = ["A","B","C","D"]
        for i, choice in enumerate(self.current_question.choices):
            btn = tk.Button(question_frame, text=f"{letters[i]}: {choice}", width=40,
                            command=lambda c=letters[i]: self.answer_question(c))
            btn.pack(pady=3)
            self.current_choices.append(btn)

        # Lifelines (greyed out after use)
        lifeline_frame = tk.Frame(question_frame)
        lifeline_frame.pack(pady=10)

        self.btn_5050 = tk.Button(lifeline_frame, text="50/50", command=self.lifeline_5050)
        self.btn_5050.grid(row=0, column=0, padx=5)
        if self.player.lifelines_used["50/50"]:
            self.btn_5050.config(state=tk.DISABLED)

        self.btn_phone = tk.Button(lifeline_frame, text="Phone a Friend", command=self.lifeline_phone)
        self.btn_phone.grid(row=0, column=1, padx=5)
        if self.player.lifelines_used["Phone"]:
            self.btn_phone.config(state=tk.DISABLED)

        self.btn_audience = tk.Button(lifeline_frame, text="Ask the Audience", command=self.lifeline_audience)
        self.btn_audience.grid(row=0, column=2, padx=5)
        if self.player.lifelines_used["Audience"]:
            self.btn_audience.config(state=tk.DISABLED)

        tk.Button(question_frame, text="Take Money and Quit", command=self.take_money_prompt).pack(pady=10)

    # Lifelines
  
    def lifeline_5050(self):
        if self.player.lifelines_used["50/50"]:
            messagebox.showinfo("50/50", "You have already used this lifeline.")
            return
        self.player.lifelines_used["50/50"] = True
        self.btn_5050.config(state=tk.DISABLED)
        letters = ["A","B","C","D"]
        correct_index = letters.index(self.current_question.answer)
        wrong_indices = [i for i in range(4) if i != correct_index]
        to_disable = random.sample(wrong_indices, 2)
        for i in to_disable:
            self.current_choices[i]["state"] = tk.DISABLED

    def lifeline_phone(self):
        if self.player.lifelines_used["Phone"]:
            messagebox.showinfo("Phone a Friend", "You have already used this lifeline.")
            return
        self.player.lifelines_used["Phone"] = True
        self.btn_phone.config(state=tk.DISABLED)
        correct_choice = self.current_question.answer
        choices = ["A","B","C","D"]
        suggested = correct_choice if random.random() < 0.7 else random.choice([c for c in choices if c != correct_choice])
        messagebox.showinfo("Phone a Friend", f"Your friend thinks the answer is {suggested}.")

    def lifeline_audience(self):
        if self.player.lifelines_used["Audience"]:
            messagebox.showinfo("Ask the Audience", "You have already used this lifeline.")
            return
        self.player.lifelines_used["Audience"] = True
        self.btn_audience.config(state=tk.DISABLED)

        correct_index = ["A","B","C","D"].index(self.current_question.answer)
        votes = [random.randint(0, 100) for _ in range(4)]
        votes[correct_index] += random.randint(30, 50)
        total = sum(votes)
        votes = [int(v / total * 100) for v in votes]
        diff = 100 - sum(votes)
        votes[correct_index] += diff
        result = "\n".join([f"{l}: {votes[i]}%" for i,l in enumerate(["A","B","C","D"])])
        messagebox.showinfo("Ask the Audience", f"Audience Poll:\n{result}")


    # Answer Handling (Simplified)
    
    def answer_question(self, choice):
        if self.current_question.check_answer(choice):
            self.player.score = self.prizes[self.current_index]
            self.next_question()
        else:
            guaranteed_prize = 0
            for q_index in sorted(self.guaranteed.keys()):
                if self.current_index >= q_index:
                    guaranteed_prize = self.guaranteed[q_index]
            self.end_game(win=False)


    # Next Question Helper
    
    def next_question(self):
        self.current_index += 1
        if self.current_index in self.guaranteed:
            self.mandatory_quit_prompt()
        else:
            self.show_question()

    
    #Quit / Take Money
    
    def take_money_prompt(self):
        prize = self.prizes[self.current_index-1] if self.current_index > 0 else 0
        if self.current_index in self.guaranteed:
            self.mandatory_quit_prompt()
            return
        choice = messagebox.askyesno("Take Money?", f"Do you want to take ${prize} and quit?")
        if choice:
            self.end_game(win=True)
        else:
            self.show_question()

    def mandatory_quit_prompt(self):
        prize = self.guaranteed[self.current_index]
        choice = messagebox.askyesno("Guaranteed Money", f"You've reached ${prize} guaranteed. Do you want to continue?")
        if not choice:
            self.end_game(win=True)
        else:
            self.show_question()

    
    # End Game
    
    def end_game(self, win=False):
        self.clear_window()
        if win:
            message = f"Congratulations! You take home ${self.player.score}!"
        else:
            guaranteed_prize = 0
            for q_index in sorted(self.guaranteed.keys()):
                if self.current_index >= q_index:
                    guaranteed_prize = self.guaranteed[q_index]
            message = f"Game Over! You take home ${guaranteed_prize}."

        tk.Label(self.root, text=message, font=("Arial", 16), wraplength=500).pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Play Again", width=15, command=self.play_again).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Exit", width=15, command=self.root.destroy).pack(side=tk.RIGHT, padx=10)

    
    # Play Again Logic
    
    def play_again(self):
        self.current_index = 0
        self.player.score = 0
        self.player.lifelines_used = {"50/50": False, "Phone": False, "Audience": False}
        self.questions = [Question(q[0],[q[1],q[2],q[3],q[4]],q[5]) for q in questions_data]
        self.show_question()

    
    # Helper
   
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize Game

if __name__ == "__main__":
    root = tk.Tk()
    question_objects = [Question(q[0],[q[1],q[2],q[3],q[4]],q[5]) for q in questions_data]
    game = Game(root, question_objects)
    root.mainloop()

