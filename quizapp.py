import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog, font
import customtkinter as ctk
import pandas as pd
import json
import os
import sys


def resource_path(relative_path):
    """Get the absolute path to the resource, works for development and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


json_file = resource_path("questions.json")

questions_dict = []
try:
    with open(json_file, "r") as file:
        questions_dict = json.load(file)
except Exception as e:
    print(f"Failed to load questions.json: {e}")


class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Quiz App")
        
        # Initialize selected_certif to track the current selection
        self.selected_certif = None
        self.selected_answer = None
        self.main_menu_frame_height = 350
        self.questions_frame_height = 350
        self.answers_frame_height = 175
        self.font = "Made Tommy"
        self.font_lisible = "Consola Mono"
                        
        # Screen dimensions and window sizing
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        padding = 180
        self.width = screen_width - padding
        self.height = screen_height - padding
        self.geometry(f"{self.width}x{self.height}+{padding // 2}+{padding // 2}")
        self.minsize(self.width, self.height)
        print("width:", self.width, "height:", self.height)
     
        # DataFrame for questions
        self.questions_df = pd.DataFrame(questions_dict)
        
        # Initialize the main menu
        self.initialize_main_menu()
        
    def adjust_widget_sizes(self, event):
        # Adjust the width of frames to match the app's width
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        self.main_menu_frame.place_configure(
            width=current_width, 
            height=current_height)
        self.questions_frame.place_configure(
            width=current_width, 
            height=current_height - self.main_menu_frame_height)
        self.header.configure(
            width=current_width)
        self.certif_select_label.configure(
            width=current_width)
        self.question_count_label.configure(
            width=current_width)
            
    def initialize_main_menu_frame(self):
        # Main Menu Frame
        self.main_menu_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.main_menu_frame_height)
        self.main_menu_frame.place(x=0, y=0)
        self.main_menu_frame.configure(
            fg_color="#151515")
    
    def initialize_main_questions_frame(self):
        # Questions Frame
        self.questions_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.questions_frame_height)
        self.questions_frame.place(x=0, y=self.main_menu_frame_height)
        self.questions_frame.configure(
            fg_color="#151515")
    
    def initialize_main_answers_frame(self):
        # Questions Frame
        self.answers_frame = ctk.CTkFrame(self, width=1000, height=self.answers_frame_height)
        self.answers_frame.place(x=0, y=self.main_menu_frame_height+self.questions_frame_height, relx=0.5, anchor='n')
        self.answers_frame.configure(
            fg_color="#151515", 
            bg_color="#151515")
    
    def initialize_main_submission_frame(self):
        # Questions Frame
        self.submission_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=150)
        self.submission_frame.place(x=0, y=self.main_menu_frame_height+self.questions_frame_height+self.answers_frame_height, relx=0.5, anchor='n')
        self.submission_frame.configure(
            fg_color="#151515", 
            bg_color="#151515")

    def initialize_main_menu(self):
        
        self.initialize_main_menu_frame()
        self.initialize_main_questions_frame()
        self.initialize_main_answers_frame()
        self.initialize_main_submission_frame()
        
        self.display_header()
        self.display_certif_select_label()
        self.display_certif_combobox()
        self.display_question_count_label()
        self.display_start_button()
                       
        # To ensure the frame adjusts its width when the window is resized:
        self.bind("<Configure>", self.adjust_widget_sizes)
        # self.print_total_height_widgets_in_frame(self.main_menu_frame, "main_menu_frame")
        

    def optionmenu_callback(self, choice):           
        self.selected_certif = choice
        question_count = self.questions_df[self.questions_df['CertifCode'].str.upper() == choice]['QuestionID'].nunique()
        self.question_count_label.configure(
            text=f"NUMBER OF QUESTIONS: {question_count}")
        self.start_button.configure(
            fg_color="#E7E7E7", 
            bg_color="transparent",
            hover_color="#ff9898",
            state="normal",)
    
    def load_certifications_code(self):
        certif_codes = self.questions_df['CertifCode'].str.upper().unique().tolist()
        return certif_codes if certif_codes else ["No certifications found"]
         
    def load_questions(self):
        # Check if a certification has been selected
        if not self.selected_certif or self.selected_certif == "No certifications found":
            pass
        else:
            # Proceed with the action for the button since a certification has been selected
            self.questions_df = self.questions_df[self.questions_df["CertifCode"].str.upper() == self.selected_certif]
            self.display_question_text()
            self.answers_frame.configure(
                fg_color="#303030")
            self.ask_question()
            self.disable_certif_combobox()
            self.disable_start_button()
    
    def get_available_questions(self):
        available_questions = self.questions_df[self.questions_df["Counter"] == 0]
        return available_questions
    
    def pick_random_questions(self, available_questions):
        # pick a question from the list of questions randomly
        question_row = available_questions.sample(n=1).iloc[0]
        return question_row
            
    def ask_question(self):
        self.display_submission_button()
        self.display_stop_quiz_button()

        available_questions = self.get_available_questions()
        if available_questions.empty:
            messagebox.showinfo("End", "No more questions available.")
            return

        self.question_row = self.pick_random_questions(available_questions)
        self.question_type = self.question_row['QuestionType']
        self.current_question = self.question_row  # Update current_question for consistency in other methods

        # Update the method calls to use the newly assigned question_row and question_type
        self.display_question_type(self.question_type)

               
    def insert_question_text(self):    
        self.questions_display.configure(
            state="normal")  # Temporarily enable the widget to insert text
        self.questions_display.delete("1.0", tk.END)  # Clear existing text
        self.questions_display.insert("1.0", self.current_question['Question'])  # Insert the question
        self.questions_display.configure(
            state="disabled")  # Disable the widget to make it read-only
    
    def toggle_choice(self, choice):
        # Determine the question type
        question_type = self.current_question['QuestionType']

        if question_type == "multiplechoice":
            # Multiple selections allowed - simply add or remove choices
            if choice in self.selected_choices:
                self.selected_choices.remove(choice)
                self.choice_buttons[choice].configure(
                    fg_color="#202020", 
                    text_color="white", 
                    hover_color="#505050")
            else:
                self.selected_choices.add(choice)
                self.choice_buttons[choice].configure(
                    fg_color="#ff9898", 
                    text_color="black", 
                    hover_color="#ff9898")

        elif question_type == "yesno":
            # Single selection - deselect the other option when one is selected
            selected_key = next(iter(self.selected_choices)) if self.selected_choices else None
            if selected_key:
                self.choice_buttons[selected_key].configure(
                    fg_color="#202020", 
                    text_color="white", 
                    hover_color="#505050")
                self.selected_choices.clear()
            self.selected_choices.add(choice)
            self.choice_buttons[choice].configure(
                fg_color="#ff9898", 
                text_color="black", 
                hover_color="#ff9898")

        elif question_type == "hotspot":
            # Identify the sub-question index from the choice identifier
            sub_question_index, current_choice = choice.split('_')
            
            # Find and deselect the opposite choice for the same sub-question if it's already selected
            for selected_choice in list(self.selected_choices):
                if selected_choice.startswith(sub_question_index + '_'):
                    # Deselect the previous choice for this sub-question
                    self.selected_choices.remove(selected_choice)
                    self.choice_buttons[selected_choice].configure(
                        fg_color="#202020", 
                        text_color="white", 
                        hover_color="#505050")
        
        # Now select the new choice
        self.selected_choices.add(choice)
        self.choice_buttons[choice].configure(
            fg_color="#ff9898", 
            text_color="black", 
            hover_color="#ff9898")
   
    def check_and_update_choices(self):
        correct_answers = self.current_question['Answer']
        question_type = self.current_question['QuestionType']
        
        # Remove existing button and create new ones for next steps.
        self.submission_frame.winfo_children()[0].destroy()
        self.display_show_explanation_button()
        self.display_next_question_button()

        for choice, button in self.choice_buttons.items():
            button.configure(
                state='disabled')  # Disable all buttons first.

            if question_type == "hotspot":
                # Hotspot questions: Compare each sub-question's choice with the corresponding correct answer.
                choice_id, choice_value = choice.split('_')  # Splitting '1_Y' into ['1', 'Y']
                answer_index = int(choice_id) - 1  # Adjusting index to align with correct_answers (assuming it's 0-indexed)

                is_correct = (choice_value == correct_answers[answer_index])
            else:
                # For non-hotspot questions, check if the choice is in the list/set of correct answers.
                is_correct = choice in correct_answers
            
            # Now, determine the color based on correctness and selection.
            if is_correct and choice in self.selected_choices:
                button.configure(
                    fg_color="#3EB20C", 
                    text_color="white", 
                    text_color_disabled="white")  # Correctly selected.
            elif not is_correct and choice in self.selected_choices:
                button.configure(
                    fg_color="#ff4444", 
                    text_color="white", 
                    text_color_disabled="white")  # Incorrectly selected.
            elif is_correct:
                button.configure(
                    fg_color="#2B720C", 
                    text_color="white", 
                    text_color_disabled="white")  # Correct but not selected.
            else:
                button.configure(
                    fg_color="#202020", 
                    text_color="white", 
                    text_color_disabled="white")  # Default for non-selected/non-relevant.

    
    def stop_quiz(self):
        self.clear_questions_display()
        self.clear_choice_buttons_dict()
        
        self.destroy_choice_buttons()
        self.destroy_submission_buttons()
        self.destroy_question_text()
        
        self.answers_frame.configure(
            fg_color="#151515")
         
        # Reset the selected choices
        self.selected_choices = set()
        
        self.question_count_label.configure(
            text="NUMBER OF QUESTIONS: -")
        
        self.enable_certif_combobox()
        self.enable_start_button()
    
    def next_question(self):
        self.clear_questions_display()
        self.clear_choice_buttons_dict()
        
        self.destroy_explanation_window()
        self.destroy_choice_buttons()
        self.destroy_submission_buttons()
         
        # Reset the selected choices
        self.selected_choices = set()
        
        # Move to the next question
        self.ask_question()
    
    def show_explanation(self):
        self.destroy_explanation_window()
            
        # Create a new Toplevel window to display the explanation
        self.explanation_window = ctk.CTkToplevel(self)
        self.explanation_window.title("Explanation")
        self.explanation_window.attributes('-topmost', True)  # Make the window stay on top
        
        # Create a main frame inside the Toplevel window for content
        main_frame = ctk.CTkFrame(self.explanation_window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)  # Use padx and pady to simulate border spacing
        main_frame.configure(
            fg_color="#151515")
        
        # Get the explanation text from the current question
        explanation_text = self.current_question['Explanation']

        # Create a label inside the main_frame to display the explanation
        explanation_label = ctk.CTkLabel(main_frame, text=explanation_text, wraplength=600)
        explanation_label.pack(padx=20, pady=20)  # Internal padding for the label
        explanation_label.configure(
            fg_color="#151515", 
            text_color="#ff9898", 
            font=(self.font_lisible, 16),
            justify="left")
        
        # Set the Toplevel window to be resizable
        self.explanation_window.resizable(True, True)
        
    # ----------------------------------------------------------------------------------------------
    # DISPLAY QUESTION TYPE
    # ----------------------------------------------------------------------------------------------
    
    # Display the question based on the question type
    def display_question_type(self, question_type):
        # Now directly using self.question_type
        if self.question_type == 'yesno':
            self.display_yesno_question()
        elif self.question_type == 'hotspot':
            self.display_hotspot_question()
        elif self.question_type == 'draganddrop':
            self.display_draganddrop_question()
        elif self.question_type == 'multiplechoice':
            self.display_multiplechoice_question()
             
    def display_multiplechoice_question(self):
        self.selected_choices = set() # Store the selected choices
        self.choice_buttons = {} # Store the buttons in a dictionary to access them later
        self.correct_answer = set(self.current_question['Answer'])
        
        self.insert_question_text()
        self.set_answer_for_multiplechoice()
    
    def display_draganddrop_question(self):
        self.questions_display.configure(
            state="normal")  # Temporarily enable the widget to insert text
        self.questions_display.insert("1.0", self.current_question['Question'])  # Assume you insert a long question here
        self.questions_display.configure(
            state="disabled")  # Disable the widget to make it read-only
        pass
    
    def display_hotspot_question(self):
        self.selected_choices = set() # Store the selected choices
        self.choice_buttons = {} # Store the buttons in a dictionary to access them later
        self.correct_answer = set(self.current_question['Answer'])
        
        self.insert_question_text()
        self.set_answer_for_hotspot()
        pass    
    
    def display_yesno_question(self):
        self.selected_choices = set() # Store the selected choices
        self.choice_buttons = {} # Store the buttons in a dictionary to access them later
        self.correct_answer = set(self.current_question['Answer'])
        
        self.insert_question_text()
        self.set_answer_for_yesno()
        pass
    
    # ----------------------------------------------------------------------------------------------
    # SET ANSWER FOR QUESTION TYPE
    # ----------------------------------------------------------------------------------------------
    
    def set_answer_for_multiplechoice(self):
        # Starting row for choices
        choice_row = 1
        choice_column = 0

        for index, choice in enumerate(self.current_question['Choices']):
            choice_button = ctk.CTkButton(
                self.answers_frame,
                text=choice,
                command=lambda choice=choice: self.toggle_choice(choice),
                font=(self.font, 20, "bold"),
                text_color="white",
                fg_color="#202020",
                bg_color="transparent",
                hover_color="#505050",
                corner_radius=30)
            # Place the button in the grid
            if index % 5 == 0:
                choice_row += 1
                choice_column = 0
            choice_button.grid(row=choice_row, column=choice_column, padx=5, pady=5, sticky="nsew")
            self.choice_buttons[choice] = choice_button
            choice_column += 1

        # Configure the grid columns to distribute space evenly
        for col_index in range(len(self.current_question['Choices'])):
            self.questions_frame.grid_columnconfigure(col_index, weight=1)
    
    def set_answer_for_yesno(self):
        yes_button = ctk.CTkButton(
            self.answers_frame,
            text="Yes",
            font=(self.font, 20, "bold"),
            text_color="white",
            fg_color="#202020",
            bg_color="transparent",
            hover_color="#505050",
            corner_radius=30,
            command=lambda: self.toggle_choice("A"))
        yes_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.choice_buttons["A"] = yes_button

        no_button = ctk.CTkButton(
            self.answers_frame,
            text="No",
            font=(self.font, 20, "bold"),
            text_color="white",
            fg_color="#202020",
            bg_color="transparent",
            hover_color="#505050",
            corner_radius=30,
            command=lambda: self.toggle_choice("B"))
        no_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.choice_buttons["B"] = no_button
    
    def set_answer_for_hotspot(self):
        choice_row = 1
        for question_index in range(len(self.current_question['Answer'])):
            for choice_index, choice in enumerate(["Yes", "No"]):  # Assuming each sub-question has a Yes and No button
                choice_id = f"{question_index + 1}_{choice[0]}"  # Create IDs like "1_Y", "1_N", "2_Y", ...
                button = ctk.CTkButton(
                    self.answers_frame,
                    text=choice,
                    command=lambda c=choice_id: self.toggle_choice(c),
                    font=(self.font, 20, "bold"),
                    text_color="white",
                    fg_color="#202020",
                    hover_color="#505050",
                    corner_radius=30)
                button.grid(row=choice_row, column=choice_index, padx=5, pady=5, sticky="nsew")
                self.choice_buttons[choice_id] = button
            choice_row += 1
    
    # ----------------------------------------------------------------------------------------------
    # DISPLAY WIDGETS
    # ----------------------------------------------------------------------------------------------
    def display_header(self):
        self.header = ctk.CTkLabel(
            self.main_menu_frame, 
            text="QUIZZ APP", 
            font=(self.font, 40, "bold"), 
            fg_color="#ff9898", 
            text_color="black")
        self.header.pack()
        self.header.configure(
            height=100)
    
    def display_certif_select_label(self):
        self.certif_select_label = ctk.CTkLabel(
            self.main_menu_frame, 
            text="SELECT THE CERTIFICATION", 
            font=(self.font, 20, "bold"), 
            fg_color="#000000", 
            text_color="#ff9898")
        self.certif_select_label.pack()
        self.certif_select_label.configure(
            height=50)
    
    def display_certif_combobox(self):
        certif_codes = self.load_certifications_code()

        self.certif_select_combobox = ctk.CTkComboBox(
            self.main_menu_frame, 
            values=certif_codes, 
            command=self.optionmenu_callback, 
            font=(self.font, 20, "bold"))
        self.certif_select_combobox.pack(pady=(20, 0))
        self.certif_select_combobox.configure(
            width=200,
            text_color="white",
            button_color="black",
            dropdown_font=(self.font, 20, "bold"),
            dropdown_fg_color="white",
            dropdown_hover_color="black",
            dropdown_text_color="black",
            fg_color="#151515")
        self.certif_select_combobox.set("")
    
    def display_question_count_label(self):
        self.question_count_label = ctk.CTkLabel(
            self.main_menu_frame, 
            text="NUMBER OF QUESTIONS: -", 
            font=(self.font, 20, "bold"), 
            fg_color="#000000", 
            text_color="#ff9898")
        self.question_count_label.pack(pady=(20, 0))
        self.question_count_label.configure(
            height=50)
        
    def display_start_button(self):
        self.start_button = ctk.CTkButton(
            self.main_menu_frame,
            text="START QUIZ", 
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color="#202020", 
            bg_color="transparent",
            state="disabled",
            corner_radius=10,
            command=self.load_questions)
        self.start_button.pack(pady=(20, 0))
        self.start_button.configure(
            height=60, width=200)
    
    def display_question_text(self):
        self.questions_display = ctk.CTkTextbox(
            self.questions_frame,
            font=(self.font_lisible, 16, "bold"),
            fg_color="#303030",
            text_color="#ff9898",
            border_spacing=20,
            wrap="word",)
        self.questions_display.pack(pady=20, anchor='center')
        self.questions_display.configure(
            height=300, 
            width=1000)
    
    def display_stop_quiz_button(self):
        self.stop_button = ctk.CTkButton(
            self.submission_frame,
            text="STOP QUIZ", 
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color="#FE3E3E", 
            bg_color="transparent",
            hover_color="#B53131",
            corner_radius=10,
            command=self.stop_quiz)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.stop_button.configure(
            height=60, 
            width=200)
        
    def display_submission_button(self):
        submit_button = ctk.CTkButton(
            self.submission_frame,
            text="SUBMIT",
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color="#E7E7E7", 
            bg_color="transparent",
            hover_color="#ff9898",
            corner_radius=10,
            command=self.check_and_update_choices)
        submit_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        submit_button.configure(
            height=60, 
            width=200)
            
    def display_show_explanation_button(self):
        review_button = ctk.CTkButton(
            self.submission_frame,
            text="EXPLANATIONS",
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color="#E7E7E7", 
            bg_color="transparent",
            hover_color="#ff9898",
            corner_radius=10,
            command=self.show_explanation)
        review_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        review_button.configure(
            height=60, 
            width=200)
    
    def display_next_question_button(self):
        next_question_button = ctk.CTkButton(
            self.submission_frame,
            text="NEXT QUESTION",
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color="#E7E7E7", 
            bg_color="transparent",
            hover_color="#ff9898",
            corner_radius=10,
            command=self.next_question)
        next_question_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        next_question_button.configure(
            height=60, 
            width=200)


    # ----------------------------------------------------------------------------------------------
    # DISABLE WIDGETS
    # ----------------------------------------------------------------------------------------------
    
    def disable_certif_combobox(self):
        self.certif_select_combobox.configure(
            state="disabled")
        
    
    def disable_start_button(self):
        self.start_button.configure(
            text_color="black",
            fg_color="#202020",
            bg_color="transparent",
            state="disabled",)
    
    # ----------------------------------------------------------------------------------------------
    # ENABLE WIDGETS
    # ----------------------------------------------------------------------------------------------
    
    def enable_certif_combobox(self):
        self.certif_select_combobox.configure(
            width=200,
            text_color="white",
            button_color="black",
            dropdown_font=(self.font, 20, "bold"),
            dropdown_fg_color="white",
            dropdown_hover_color="black",
            dropdown_text_color="black",
            fg_color="#151515",
            state="normal")
        self.certif_select_combobox.set("")
    
    def enable_start_button(self):
        self.start_button.configure(
            text_color="black",
            fg_color="#202020",
            bg_color="transparent",
            state="enabled",)
        
        
    # ----------------------------------------------------------------------------------------------
    # DESTROY WIDGETS
    # ----------------------------------------------------------------------------------------------
    
    def destroy_start_button(self):
        self.start_button.destroy()
    
    def destroy_choice_buttons(self):
        for button in self.answers_frame.winfo_children():
            button.destroy()
    
    def destroy_submission_buttons(self):
        for button in self.submission_frame.winfo_children():
            button.destroy()
    
    def destroy_explanation_window(self):
        if hasattr(self, 'explanation_window'):
            self.explanation_window.destroy()
    
    def destroy_certif_combobox(self):
        self.certif_select_combobox.destroy()
    
    def destroy_certif_select_label(self):
        self.certif_select_label.destroy()
    
    def destroy_question_count_label(self):
        self.question_count_label.destroy()
    
    def destroy_header(self):
        self.header.destroy()
        
    def destroy_question_text(self):
        self.questions_display.destroy()
            
    # ----------------------------------------------------------------------------------------------
    # CLEAR WIDGETS
    # ----------------------------------------------------------------------------------------------
    
    def clear_questions_display(self):
        self.questions_display.configure(
            state="normal")
        self.questions_display.delete("1.0", tk.END)
        self.questions_display.configure(
            state="disabled")
    
    def clear_choice_buttons_dict(self):
        self.choice_buttons.clear()
        
# Create the main window (root)
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
