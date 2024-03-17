import tkinter as tk
from tkinter import font as tkfont, Tk
from customtkinter import CTkFont
from tkinter import messagebox, Toplevel, filedialog, font
import customtkinter as ctk
import pandas as pd
from screeninfo import get_monitors
import json
import os
import ctypes
import sys
import re


"""
TODO:
- Fix answer of the question 372/46
- Add custom fonts
"""

def get_user_data_path():
    home_dir = os.path.expanduser('~')  # Get the user's home directory
    app_data_dir = os.path.join(home_dir, '.quizzapp')  # Path for your app's data
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)  # Create the directory if it doesn't exist
    return os.path.join(app_data_dir, 'quizzapp.json')

def resource_path(relative_path):
    """Get the absolute path to the resource, works for development and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

bundled_data_path = resource_path("questions.json")

def initialize_user_data():
    # If the file doesn't exist, create it and populate with data from questions.json
    bundled_data_path = resource_path("questions.json")
    if os.path.exists(bundled_data_path):
        user_data_path = get_user_data_path()
        with open(bundled_data_path, "r") as bundled_file, open(user_data_path, "w") as user_file:
            data = json.load(bundled_file)
            json.dump(data, user_file)
        return data
    else:
       print("questions.json not found. Please ensure the file is in the correct location.")
   
def save_state(data):
    user_data_path = get_user_data_path()
    with open(user_data_path, 'w') as file:
        json.dump(data, file)

questions_dict = initialize_user_data()


class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Quiz App")
        
        self.current_monitor                    = self.get_current_monitor()  
        self.screen_scaling_factor              = self.get_screen_scaling_factor()
        self.screen_width, self.screen_height   = self.get_actual_screen_dimensions()
        self.size_reference                     = 1000
    
        # height of frame and widgets
        self.initialize_widgets_height(self.screen_width, self.screen_height, self.size_reference, self.screen_scaling_factor)
  
        # Screen dimensions and window sizing
        self.width  = self.screen_width  - self.padding
        self.height = self.screen_height - self.padding
        self.geometry(f"{self.width}x{self.height}+{self.padding//2}+{self.padding//2}")
        self.minsize(self.width, self.height)
 
        
        # Initialize selected_certif to track the current selection
        self.selected_certif    = None
        self.selected_answer    = None
        self.name_app           = "EZ CERTIF"
        self.font               = "Tw Cen MT" 
        self.font_lisible       = "Consolas"
        self.family_font_header = "Tw Cen MT Condensed Extra Bold"
        self.font_header        = ctk.CTkFont(family=self.family_font_header, size=70, weight="bold")#, slant="italic")
        
        # global variables
        self.test_color             = False
        self.test_question          = False
        self.question_picked        = 100 # 124/457/249 drag and drop / 97/112 longue question / 100 hotspot / 365 multiple choice / 195 yesno / bug 137 171 249 *187
        self.correct_answer_time    = 50
        self.green                  = "#3EB20C" # Correctly selected
        self.dark_green             = "#2B720C" # Correct but not selected
        self.red                    = "#ff4444" # Incorrectly selected
        self.dark_grey              = "#151515"
        self.light_grey             = "#303030"
        self.white_grey             = "#E7E7E7"
        self.hover_grey             = "#505050"
        self.mid_grey               = "#202020"
        self.pink                   = "#ff9898"
        self.dark_pink              = "#ff59c7"
        self.darker_grey            = "#080808"
        
        # DataFrame for questions
        self.questions_df = pd.DataFrame(questions_dict)
        
        # Initialize the main menu
        self.initialize_main_menu()
                
        if self.test_color is True:
            self.use_test_color()

    def get_current_monitor(self):
        # Get the current position of the window
        window_x = self.winfo_x()
        window_y = self.winfo_y()
        for m in get_monitors():
            if m.x <= window_x <= m.x + m.width and m.y <= window_y <= m.y + m.height:
                return m  # This is the monitor where the window is located
        return None  # In case the window is not found in any monitor bounds
    
    # Screen dimension
    def get_actual_screen_dimensions(self):
        actual_screen_width, actual_screen_height = self.get_current_monitor().width, self.get_current_monitor().height
        return actual_screen_width, actual_screen_height

    # Screen scaling factor
    def get_screen_scaling_factor(self):
        scaling_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        return scaling_factor
    
    def initialize_widgets_height(self, screen_width, screen_height, size_reference, screen_scaling_factor):
        if screen_width == 1920 and screen_height == 1080 and screen_scaling_factor == 1:
            # Height of frame and widgets
            self.main_menu_frame_height         = 242   /size_reference *screen_height
            self.header_height                  = 80    /size_reference *screen_height
            self.certif_select_combobox_height  = 29    /size_reference *screen_height
            self.certif_select_label_height     = 44    /size_reference *screen_height
            self.question_count_label_height    = 44    /size_reference *screen_height
            
            self.start_and_reset_frame_height   = 80    /size_reference *screen_height
            self.start_button_height            = 58    /size_reference *screen_height
            
            self.question_space                 = 0
            self.questions_frame_height         = 235   /size_reference *screen_height
            self.questions_text_height          = 235   /size_reference *screen_height
            
            self.answers_frame_height           = 102   /size_reference *screen_height
            self.second_answer_frame_height     = 102   /size_reference *screen_height
            self.answer_space                   = 110
            self.second_answer_frame_space      = 25
            
            self.submission_space               = 160
            self.submission_frame_height        = 88    /size_reference *screen_height
            self.stop_button_height             = 58    /size_reference *screen_height
            self.submission_button_height       = 58    /size_reference *screen_height
            
            # Padding            
            self.padding = 180
            self.vertical_padding_combobox = 20/self.screen_scaling_factor
            self.horizontal_padding_combobox = 0/self.screen_scaling_factor
            self.vertical_padding_count_label = 20/self.screen_scaling_factor
            self.horizontal_padding_count_label = 0/self.screen_scaling_factor
    
    
    def adjust_widget_sizes(self, event):
        # Adjust the width of frames to match the app's size
        current_width   = self.winfo_width()
        current_height  = self.winfo_height()
            
        self.main_menu_frame.place_configure(
            width   = current_width, 
            height  = current_height)
        self.start_and_reset_frame.place_configure(
            height  = self.start_and_reset_frame_height)
        self.questions_frame.place_configure(
            width   = current_width, 
            height  = current_height - self.main_menu_frame_height)
        self.submission_frame.place_configure(
            height  = self.submission_frame_height)
        self.header.configure(
            width   = current_width)
        self.certif_select_label.configure(
            width   = current_width)
        self.question_count_label.configure(
            width   = current_width)
       
    def initialize_main_menu_frame(self):
        # Main Menu Frame
        self.main_menu_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.main_menu_frame_height)
        self.main_menu_frame.place(x=0, y=0)
        self.main_menu_frame.configure(
            fg_color=self.dark_grey)
    
    def initialize_start_and_reset_frame(self):
        # Questions Frame
        self.start_and_reset_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.start_and_reset_frame_height)
        self.start_and_reset_frame.place(x=0, y=self.main_menu_frame_height, relx=0.5, anchor='n')
        self.start_and_reset_frame.configure(
            fg_color=self.dark_grey,
            bg_color=self.dark_grey)
    
    def initialize_main_questions_frame(self):
        # Questions Frame
        self.questions_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.questions_frame_height)
        self.questions_frame.place(x=0, y=self.main_menu_frame_height+self.start_and_reset_frame_height+self.question_space)
        self.questions_frame.configure(
            fg_color=self.dark_grey)
    
    def initialize_main_answers_frame(self):
        # Questions Frame
        self.answers_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.answers_frame_height)
        self.answers_frame.configure(
            fg_color=self.light_grey,
            bg_color=self.dark_grey)
    
    def initialize_second_answers_frame(self):
        # Questions Frame
        self.second_answer_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.second_answer_frame_height)
        self.second_answer_frame.configure(
            fg_color=self.light_grey,
            bg_color=self.dark_grey)
             
    def initialize_main_submission_frame(self):
        # Questions Frame
        self.submission_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.submission_frame_height)
        self.submission_frame.place(x=0, y=self.main_menu_frame_height+self.questions_frame_height+self.answers_frame_height+self.submission_space, relx=0.5, anchor='n')
        self.submission_frame.configure(
            fg_color=self.dark_grey,
            bg_color=self.dark_grey)

    def initialize_main_menu(self):
        self.initialize_main_menu_frame()
        self.initialize_start_and_reset_frame()
        self.initialize_main_questions_frame()
        self.initialize_main_answers_frame()
        self.initialize_second_answers_frame()
        self.initialize_main_submission_frame()
        
        self.display_header()
        self.display_certif_select_label()
        self.display_certif_combobox()
        self.display_question_count_label()
        self.display_start_button()
        self.display_reset_button()
                           
        # To ensure the frame adjusts its width when the window is resized:
        self.bind("<Configure>", self.adjust_widget_sizes)
        
        if self.test_color is True or self.test_question is True:
            print("current_monitor:", self.current_monitor)
            print("screen_scaling_factor:", self.screen_scaling_factor)
            print("screen_width:", self.screen_width, "screen_height:", self.screen_height)
            print("width:", self.width, "height:", self.height)
    
    def use_test_color(self):
        self.main_menu_frame.configure(
            fg_color="red")
        self.start_and_reset_frame.configure(
            fg_color="orange")
        self.questions_frame.configure(
            fg_color="blue")
        self.answers_frame.configure(
            fg_color="green")
        self.second_answer_frame.configure(
            fg_color="pink")
        self.submission_frame.configure(
            fg_color="yellow")
    
    def count_questions_certif(self, choice):
        question_count = self.questions_df[self.questions_df['CertifCode'].str.upper() == choice]['QuestionID'].nunique()
        return question_count

    def count_correct_answers_certif(self, choice):
        correct_answers_count = self.questions_df[(self.questions_df['CertifCode'].str.upper() == choice) & (self.questions_df['Counter'] != 0)].shape[0]
        return correct_answers_count

    def update_question_count_label(self, choice):
        self.question_count_label.configure(
            text=f"NUMBER OF QUESTIONS: {self.count_questions_certif(choice)} ({self.count_correct_answers_certif(choice)})")
    
    def optionmenu_callback(self, choice):           
        self.selected_certif = choice
        self.question_count_label.configure(
            text=self.update_question_count_label(choice))
        self.enable_start_button()
        self.enable_reset_button()
        
        
    # ----------------------------------------------------------------------------------------------
    # START QUIZ
    # ----------------------------------------------------------------------------------------------
    
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
            self.ask_question()
            self.disable_certif_combobox()
            self.disable_start_button()
    
    def reset_questions(self):
        # reset all counter to 0
        self.questions_df['Counter'] = 0
        # update question_count_label_height
        self.update_question_count_label(self.selected_certif)
        save_state(self.questions_df.to_dict('records'))
        print("saved!")
    
    def get_available_questions(self):
        available_questions = self.questions_df[self.questions_df["Counter"] == 0]
        return available_questions
    
    def pick_random_questions(self, available_questions):
        # pick a question from the list of questions randomly
        
        if self.test_question is True:
            question_row = available_questions[available_questions["QuestionID"] == self.question_picked].iloc[0]
        else:
            question_row = available_questions.sample(n=1).iloc[0]
        
        if self.test_question is True or self.test_color is True:
            print("id:", question_row["QuestionID"])
            print("counter:", question_row["Counter"])
            print("certif:", question_row["CertifCode"])
            print("type:", question_row["QuestionType"])
            print("answer:", question_row["Answer"])
            print("choices:", question_row["Choices"])
        else:
            print("id:", question_row["QuestionID"], "certif:", question_row["CertifCode"])
       
        return question_row
    
    # Decrease counter for all questions that have been answered correctly previously
    def decrease_counter(self):
        self.questions_df.loc[self.questions_df['Counter'] != 0, 'Counter'] -= 1
            
    def ask_question(self):
        self.display_submission_button()
        self.display_stop_quiz_button()
        self.decrease_counter()

        available_questions = self.get_available_questions()
        if available_questions.empty:
            messagebox.showinfo("End", "No more questions available.")
            return

        self.question_row = self.pick_random_questions(available_questions)
        self.question_type = self.question_row['QuestionType']
        self.current_question = self.question_row  # Update current_question for consistency in other methods

        if self.question_type == 'draganddrop':
            self.show_main_answers_frame()
            self.show_second_answers_frame() 
        else:
            self.show_main_answers_frame()
            self.hide_second_answers_frame() 

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
            self.update_choice_selection_and_appearance(choice)
            
        elif question_type == "yesno":
            # Single selection - deselect the other option when one is selected
            selected_key = next(iter(self.selected_choices)) if self.selected_choices else None
            if selected_key:
                self.selected_choices.remove(selected_key)
                self.reset_button_appearance(selected_key)
            self.selected_choices.add(choice)
            self.highlight_button_appearance(choice)

        elif question_type == "hotspot":
            # Identify the sub-question index from the choice identifier
            sub_question_index, current_choice = choice.split('_')
            
            # Find and deselect the opposite choice for the same sub-question if it's already selected
            for selected_choice in list(self.selected_choices):
                if selected_choice.startswith(sub_question_index + '_'):
                    # Deselect the previous choice for this sub-question
                    self.selected_choices.remove(selected_choice)
                    self.reset_button_appearance(selected_choice)
            self.selected_choices.add(choice)
            self.highlight_button_appearance(choice)
        
        elif question_type == "draganddrop":
            self.handle_drag_and_drop_choice(choice)
                
            
    # ----------------------------------------------------------------------------------------------
    # CHECK ANSWERS
    # ----------------------------------------------------------------------------------------------
        
    def check_and_update_choices(self):
        self.cleanup_before_checking_answers()
        question_type = self.current_question['QuestionType']

        if question_type == "draganddrop":
            is_full_correct = self.check_drag_and_drop_answers()
        elif question_type == "hotspot":
            is_full_correct = self.check_hotspot_answers()
        else:
            is_full_correct = self.check_standard_answers()

        self.finalize_answer_check(is_full_correct, question_type)

    def cleanup_before_checking_answers(self):
        # Remove the submit button and display the next question and explanation buttons
        self.submission_frame.winfo_children()[0].destroy()
        self.display_show_explanation_button()
        self.display_next_question_button()
        
    def correct_answer_drag_and_drop(self, string):
        pairs = re.findall(r'[A-Za-z]\d', string)
        pairs_set = set(pairs)
        return pairs_set

    def check_drag_and_drop_answers(self):
        correct_answers = self.correct_answer_drag_and_drop(self.current_question['Answer'])
        created_pairs = {button.cget("text") for choice, button in self.choice_buttons.items() if choice.isdigit() and len(button.cget("text")) == 2}
                
        is_full_correct = created_pairs == correct_answers
        
        for choice, button in self.choice_buttons.items():
            if choice.isdigit():
                button_value = button.cget("text")
                is_correct = button_value in correct_answers and len(button_value) == 2
                self.update_button_appearance_after_check_for_drag_and_drop(button, is_correct)
        
        return is_full_correct


    def check_hotspot_answers(self):
        correct_answers = self.current_question['Answer']
        is_full_correct = True  # Assume true until a mismatch is found
        
        if len(self.selected_choices) != len(correct_answers):
            is_full_correct = False

        for choice, button in self.choice_buttons.items():
            choice_id, choice_value = choice.split('_')
            answer_index = int(choice_id) - 1
            is_selected = choice in self.selected_choices 
            is_correct = choice_value == correct_answers[answer_index]
            self.update_button_appearance_after_check(button, is_correct, is_selected)
    
            # Update the overall correctness
            if (not is_correct and is_selected):
                is_full_correct = False
            
        return is_full_correct

    def check_standard_answers(self):
        correct_answers = set(self.current_question['Answer'])
        selected_correct_answers = {choice for choice in self.selected_choices if choice in correct_answers}
        selected_incorrect_answers = set(self.selected_choices) - correct_answers

        is_full_correct = len(selected_correct_answers) == len(correct_answers) and not selected_incorrect_answers

        for choice, button in self.choice_buttons.items():
            is_selected = choice in self.selected_choices
            is_correct = choice in correct_answers
            self.update_button_appearance_after_check(button, is_correct, is_selected)
        
        return is_full_correct

    
    def update_button_appearance_after_check_for_drag_and_drop(self, button, is_correct):
        if is_correct:
            button.configure(fg_color=self.green, text_color="white", text_color_disabled="white")
        else:
            button.configure(fg_color=self.red, text_color="white", text_color_disabled="white")


    def update_button_appearance_after_check(self, button, is_correct, is_selected):
        if is_correct and is_selected:
            button.configure(fg_color=self.green, text_color="white", text_color_disabled="white")
        elif is_correct and not is_selected:
            button.configure(fg_color=self.dark_green, text_color="white", text_color_disabled="white")
        elif not is_correct and is_selected:
            button.configure(fg_color=self.red, text_color="white", text_color_disabled="white")
        else:
            button.configure(fg_color=self.mid_grey, text_color="white", text_color_disabled="white")

    def finalize_answer_check(self, is_full_correct, question_type):
        if is_full_correct:
            self.questions_df.loc[self.questions_df['QuestionID'] == self.current_question['QuestionID'], 'Counter'] += self.correct_answer_time
            self.update_question_count_label(self.selected_certif)
            self.set_frame_color(self.green, question_type)
        else:
            self.set_frame_color(self.red, question_type)
        
        save_state(self.questions_df.to_dict('records'))
        print("saved!")

    def set_frame_color(self, color, question_type):
        if question_type == "draganddrop":
            self.second_answer_frame.configure(border_width=2, border_color=color)
        else:
            self.answers_frame.configure(border_width=2, border_color=color)
            

    # ----------------------------------------------------------------------------------------------
    # STOP QUIZ OR MOVE TO NEXT QUESTION
    # ----------------------------------------------------------------------------------------------     
    
    def stop_quiz(self):
        self.clear_questions_display()
        self.clear_choice_buttons_dict()
        
        self.destroy_choice_buttons()
        self.destroy_submission_buttons()
        self.destroy_question_text()
        
        # Remove the border color from the answers frame and the second answers frame
        self.answers_frame.configure(border_width = 0, border_color = "black")
        self.second_answer_frame.configure(border_width = 0, border_color = "black")
        
        self.hide_main_answers_frame()
        self.hide_second_answers_frame()
         
        # Reset the selected choices
        self.selected_choices = set()
        
        self.question_count_label.configure(
            text="NUMBER OF QUESTIONS: -")
        
        self.enable_certif_combobox()
    
    def next_question(self):
        self.clear_questions_display()
        self.clear_choice_buttons_dict()
        
        self.destroy_explanation_window()
        self.destroy_choice_buttons()
        self.destroy_submission_buttons()
     
        # Reset the selected choices
        self.selected_choices = set()
        
        # Remove the border color from the answers frame and the second answers frame
        self.answers_frame.configure(border_width = 0, border_color = "black")
        self.second_answer_frame.configure(border_width = 0, border_color = "black")
        
        # Move to the next question
        self.ask_question()
     
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
        self.selected_choices = set() # Store the selected choices
        self.choice_buttons = {} # Store the buttons in a dictionary to access them later
        self.correct_answer = set(self.current_question['Answer'])
        
        self.insert_question_text()
        self.set_answer_for_draganddrop()
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
        max_columns = 5
        
        if len(self.current_question['Choices']) > 5:
            max_columns = 7

        for index, choice in enumerate(self.current_question['Choices']):
            choice_button = ctk.CTkButton(
                self.answers_frame,
                text=choice,
                command=lambda choice=choice: self.toggle_choice(choice),
                font=(self.font, 20, "bold"),
                text_color="white",
                fg_color=self.mid_grey,
                bg_color="transparent",
                hover_color=self.hover_grey,
                corner_radius=30)
            # Place the button in the grid
            if index % max_columns == 0:
                choice_row += 1
                choice_column = 0
            choice_button.grid(row=choice_row, column=choice_column, padx=8, pady=8, sticky="nsew")
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
            fg_color=self.mid_grey,
            bg_color="transparent",
            hover_color=self.hover_grey,
            corner_radius=30,
            command=lambda: self.toggle_choice("A"))
        yes_button.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
        self.choice_buttons["A"] = yes_button

        no_button = ctk.CTkButton(
            self.answers_frame,
            text="No",
            font=(self.font, 20, "bold"),
            text_color="white",
            fg_color=self.mid_grey,
            bg_color="transparent",
            hover_color=self.hover_grey,
            corner_radius=30,
            command=lambda: self.toggle_choice("B"))
        no_button.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
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
                    fg_color=self.mid_grey,
                    hover_color=self.hover_grey,
                    corner_radius=30)
                button.grid(row=choice_row, column=choice_index, padx=8, pady=8, sticky="nsew")
                self.choice_buttons[choice_id] = button
            choice_row += 1
            
    def set_answer_for_draganddrop(self):
        letter_row = 1
        number_row = 2
        
        letter_choices, number_choices = self.separate_letter_number(self.current_question['Choices'])
        
        # for each letter, create a button
        for index, choice in enumerate(letter_choices):
            letter_button = ctk.CTkButton(
                    self.answers_frame,
                    text=choice,
                    command=lambda choice=choice: self.toggle_choice(choice),
                    font=(self.font, 20, "bold"),
                    text_color="white",
                    fg_color=self.mid_grey,
                    bg_color="transparent",
                    hover_color=self.hover_grey,
                    corner_radius=30)
            letter_button.grid(row=letter_row, column=index, padx=8, pady=8, sticky="nsew")
            self.choice_buttons[choice] = letter_button  # Store button with choice as the key
            
        # for each number, create a button
        for index, choice in enumerate(number_choices):
            number_button = ctk.CTkButton(
                self.second_answer_frame,
                text=choice,
                command=lambda choice=choice: self.toggle_choice(choice),
                font=(self.font, 20, "bold"),
                text_color="white",
                fg_color=self.mid_grey,
                bg_color="transparent",
                hover_color=self.hover_grey,
                corner_radius=30)
            number_button.grid(row=number_row, column=index, padx=8, pady=8, sticky="nsew")
            self.choice_buttons[choice] = number_button  # Store button with choice as the key
            
    # ----------------------------------------------------------------------------------------------
    # DRAG AND DROP FUNCTIONS
    # ----------------------------------------------------------------------------------------------
    
    def handle_drag_and_drop_choice(self, choice):       
        if choice.isalpha():
            self.process_alpha_choice(choice)
        else:
            self.process_digit_choice(choice)

        # Check if we have one letter and one number selected to form a pair.
        if len(self.selected_choices) == 2:
            self.form_and_display_pair()

    def process_alpha_choice(self, choice):
        self.update_drag_and_drop_choice(choice, is_alpha=True)

    def process_digit_choice(self, choice):
        self.update_drag_and_drop_choice(choice, is_alpha=False)

    def update_drag_and_drop_choice(self, choice, is_alpha):
        # Extract letters and digits for further processing.
        letter_choices, digit_choices = self.extract_letters_and_digits_from_selected()
        
        # If the choice is already selected, deselect it.
        if choice in self.selected_choices:
            self.deselect_choice(choice)
        elif (is_alpha and letter_choices) or (not is_alpha and digit_choices):
            # If an item of the same type (letter/number) is already selected, replace it.
            self.replace_existing_choice(choice, letter_choices if is_alpha else digit_choices)
        else:
            # Add the new choice and update the button appearance.
            self.select_new_choice(choice)

    def form_and_display_pair(self):
        # Create a pair from the selected letter and number and display it.
        letters, digits = self.extract_letters_and_digits_from_selected()
        match = ''.join(letters) + ''.join(digits)

        # Update the text of the number button to show the pair and reset the appearance of the letter button.
        for selected_choice in list(self.selected_choices):
            if selected_choice.isdigit():
                self.choice_buttons[selected_choice].configure(text=match)
            self.reset_button_appearance(selected_choice)
        self.selected_choices.clear()

    def extract_letters_and_digits_from_selected(self):
        letters = {choice for choice in self.selected_choices if choice.isalpha()}
        digits = {choice for choice in self.selected_choices if choice.isdigit()}
        return letters, digits

    def deselect_choice(self, choice):
        self.selected_choices.remove(choice)
        self.reset_button_appearance(choice)

    def select_new_choice(self, choice):
        self.selected_choices.add(choice)
        self.choice_buttons[choice].configure(
            fg_color=self.pink, 
            text_color="black", 
            hover_color=self.pink)

    def replace_existing_choice(self, choice, existing_choices):
        # Deselect the existing choice of the same type (letter or digit).
        existing_choice = existing_choices.pop()
        self.deselect_choice(existing_choice)
        # Select the new choice.
        self.select_new_choice(choice)

    def update_choice_selection_and_appearance(self, choice):
        if choice in self.selected_choices:
            self.selected_choices.remove(choice)
            self.reset_button_appearance(choice)
        else:
            self.selected_choices.add(choice)
            self.highlight_button_appearance(choice)
    
    def reset_button_appearance(self, choice):
        self.choice_buttons[choice].configure(fg_color=self.mid_grey, text_color="white", hover_color=self.hover_grey)
    
    def highlight_button_appearance(self, choice):
        self.choice_buttons[choice].configure(
            fg_color=self.pink, 
            text_color="black", 
            hover_color=self.pink)
            
        
    # ----------------------------------------------------------------------------------------------
    # DISPLAY WIDGETS
    # ----------------------------------------------------------------------------------------------
    
    def display_header(self):
        self.header = ctk.CTkLabel(
            self.main_menu_frame, 
            text=self.name_app, 
            font=self.font_header, 
            fg_color=self.pink, 
            text_color="black")
        self.header.pack()
        self.header.configure(
            height=self.header_height)
    
    def display_certif_select_label(self):
        self.certif_select_label = ctk.CTkLabel(
            self.main_menu_frame, 
            text="SELECT THE CERTIFICATION", 
            font=(self.font, 25, "bold"), 
            fg_color="#000000", 
            text_color=self.pink)
        self.certif_select_label.pack()
        self.certif_select_label.configure(
            height=self.certif_select_label_height)
    
    def display_certif_combobox(self):
        certif_codes = self.load_certifications_code()

        self.certif_select_combobox = ctk.CTkComboBox(
            self.main_menu_frame, 
            values=certif_codes, 
            command=self.optionmenu_callback, 
            font=(self.font, 20, "bold"))
        self.certif_select_combobox.pack(pady=(self.vertical_padding_combobox, self.horizontal_padding_combobox))
        self.certif_select_combobox.configure(
            width=200,
            text_color="white",
            button_color="black",
            dropdown_font=(self.font, 20, "bold"),
            dropdown_fg_color="white",
            dropdown_hover_color="black",
            dropdown_text_color="black",
            fg_color=self.dark_grey)
        self.certif_select_combobox.set("")
    
    def display_question_count_label(self):
        self.question_count_label = ctk.CTkLabel(
            self.main_menu_frame, 
            text="NUMBER OF QUESTIONS: -", 
            font=(self.font, 25, "bold"), 
            fg_color="#000000", 
            text_color=self.pink)
        self.question_count_label.pack(pady=(self.vertical_padding_count_label, self.horizontal_padding_count_label))
        self.question_count_label.configure(
            height=self.question_count_label_height)
        
    def display_start_button(self):
        self.start_button = ctk.CTkButton(
            self.start_and_reset_frame,
            text="START QUIZ", 
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color=self.mid_grey, 
            bg_color="transparent",
            state="disabled",
            corner_radius=10,
            command=self.load_questions)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.start_button.configure(
            height=self.start_button_height,
            width=200)
    
    def display_reset_button(self):
        self.reset_button = ctk.CTkButton(
            self.start_and_reset_frame,
            text="RESET", 
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color=self.mid_grey, 
            bg_color="transparent",
            state="disabled",
            corner_radius=10,
            command=self.reset_questions)
        self.reset_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.reset_button.configure(
            height=self.start_button_height,
            width=200)
    
    def display_question_text(self):
        self.questions_display = ctk.CTkTextbox(
            self.questions_frame,
            font=(self.font_lisible, 20),
            fg_color=self.darker_grey,
            text_color=self.white_grey,
            border_spacing=20,
            wrap="word",)
        self.questions_display.pack(pady=0, anchor='center')
        self.questions_display.configure(
            height=self.questions_text_height,
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
            height=self.stop_button_height,
            width=200)
        
    def display_submission_button(self):
        submit_button = ctk.CTkButton(
            self.submission_frame,
            text="SUBMIT",
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color=self.white_grey,
            bg_color="transparent",
            hover_color=self.pink,
            corner_radius=10,
            command=self.check_and_update_choices)
        submit_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        submit_button.configure(
            height=self.submission_button_height, 
            width=200)
            
    def display_show_explanation_button(self):
        review_button = ctk.CTkButton(
            self.submission_frame,
            text="EXPLANATIONS",
            font=(self.font, 20, "bold"),
            text_color="black",
            fg_color=self.white_grey,
            bg_color="transparent",
            hover_color=self.pink,
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
            fg_color=self.white_grey,
            bg_color="transparent",
            hover_color=self.pink,
            corner_radius=10,
            command=self.next_question)
        next_question_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        next_question_button.configure(
            height=60, 
            width=200)
    
    def show_explanation(self):
        self.destroy_explanation_window()
            
        # Create a new Toplevel window to display the explanation
        self.explanation_window = ctk.CTkToplevel(self)
        self.explanation_window.title("Explanation")
        self.explanation_window.attributes('-topmost', True)  # Make the window stay on top
        
        # Create a main frame inside the Toplevel window for content
        main_frame = ctk.CTkFrame(self.explanation_window)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)  # Use padx and pady to simulate border spacing
        main_frame.configure(
            fg_color=self.darker_grey)
        
        # Get the explanation text from the current question
        explanation_text = self.current_question['Explanation']

        # Create a label inside the main_frame to display the explanation
        explanation_label = ctk.CTkLabel(main_frame, text=explanation_text, wraplength=600)
        explanation_label.pack(padx=20, pady=20)  # Internal padding for the label
        explanation_label.configure(
            fg_color=self.darker_grey,
            text_color=self.white_grey, 
            font=(self.font_lisible, 20),
            justify="left")
        
        # Set the Toplevel window to be resizable
        self.explanation_window.resizable(True, True)
    
    # ----------------------------------------------------------------------------------------------
    # SHOW AND HIDE FRAMES
    # ----------------------------------------------------------------------------------------------
        
    def show_main_answers_frame(self):
        self.answers_frame.place(x=0, y=self.main_menu_frame_height+self.questions_frame_height+self.answer_space, relx=0.5, anchor='n')
        
    def hide_main_answers_frame(self):
        self.answers_frame.place_forget()
        
    def show_second_answers_frame(self):
        self.second_answer_frame.place(x=0, y=self.main_menu_frame_height+self.questions_frame_height+self.answers_frame_height+self.second_answer_frame_space, relx=0.5, anchor='n')
    
    def hide_second_answers_frame(self):
        self.second_answer_frame.place_forget()
        

    # ----------------------------------------------------------------------------------------------
    # DISABLE WIDGETS
    # ----------------------------------------------------------------------------------------------
    
    def disable_certif_combobox(self):
        self.certif_select_combobox.configure(
            state="disabled")
        
    
    def disable_start_button(self):
        self.start_button.configure(
            text_color="black",
            fg_color=self.mid_grey,
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
            fg_color=self.dark_grey,
            state="normal")
        self.certif_select_combobox.set("")
    
    def enable_start_button(self):
        self.start_button.configure(
            fg_color=self.white_grey,
            bg_color="transparent",
            hover_color=self.pink,
            state="normal",)
    
    def enable_reset_button(self):
        self.reset_button.configure(
            fg_color=self.white_grey,
            bg_color="transparent",
            hover_color=self.pink,
            state="normal",)
        
        
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
        
    def destroy_answers_frame(self):
        self.answers_frame.destroy()
    
    def destroy_second_answers_frame(self):
        self.second_answer_frame.destroy()
    
       
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
    
    
    # ----------------------------------------------------------------------------------------------
    # SET VARIABLES
    # ----------------------------------------------------------------------------------------------
    
    def set_correct_answer_time(self, time):
        self.correct_answer_time = time
        
    # ----------------------------------------------------------------------------------------------
    # USEFUL FUNCTIONS
    # ----------------------------------------------------------------------------------------------
    
    def separate_letter_number(self, choice):
        letter_choice = ""
        number_choice = ""
        for index, char in enumerate(choice):
            if char.isalpha():
                letter_choice += char
            elif char.isdigit():
                number_choice += char
        return letter_choice, number_choice
    
    def count_letters_and_numbers(self, input_set):
        letters = sum(str(elem).isalpha() for elem in input_set)
        numbers = sum(str(elem).isdigit() for elem in input_set)
        return letters, numbers

    def remove_letters_from_set(self, input_set):
        # Using set comprehension to remove letters and create a new set
        return {item for item in input_set if not item.isalpha()}

    def remove_digits_from_set(self, input_set):
        # Using list comprehension to remove digits and create a new list
        return {item for item in input_set if not item.isdigit()}

        
# Create the main window (root)
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
