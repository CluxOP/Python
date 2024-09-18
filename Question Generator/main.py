# importing required modules 
import google.generativeai as genai
import json
from pdf2image import convert_from_path
from pypdf import PdfReader
import random
import shutil
import threading
import tkinter
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os

SCORE = 0

# GUI
class App(ctk.CTk):
    def __init__(self, title):

        # main setup
        super().__init__(fg_color="black")
        self.title(title)
        self.minsize(500, 500)       
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        # welcome page
        self.welcome_page = WelcomePage(self)

        # run
        self.mainloop()

    # confirm user to quit
    def on_quit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()


class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent):

        # main setup
        self.parent = parent
        super().__init__(parent, fg_color="black")
        self.file_path = None
        self.pack(expand=True)

        # welcome label
        ctk.CTkLabel(
            master=self, 
            text="Welcome to QuizMaker", 
            text_color="white",
            font=("Roboto", 28, "bold")).pack(expand=True, fill="x")
        
        # sub label
        ctk.CTkLabel(
            master=self,
            text="Get ready to test your brain! 🧠",
            text_color="#bebebe",
            font=("Roboto", 16)).pack(expand=True, fill="x", pady=(0, 100))
        
        # no. of questions label
        ctk.CTkLabel(
            master=self,
            text="Number of questions :",
            text_color="white",
            font=("Roboto", 16, "bold")).place(relx=0.25, rely=0.4)
        
        self.no_of_questions = tkinter.IntVar()
        self.no_of_questions.set(1)
        # slider value label
        ctk.CTkLabel(
            master=self,
            textvariable=self.no_of_questions,
            text_color="white",
            font=("Roboto", 16, "bold")).place(relx=0.67, rely=0.4)
        
        # question slider
        ctk.CTkSlider(
            master=self,
            variable=self.no_of_questions,
            width=425,
            height=20,
            from_=1,
            to=10,
            number_of_steps=11).pack(expand=True, pady=(30, 10))
    
        # choose a file button
        self.choose_file_button = ctk.CTkButton(
            master=self,
            text="Choose a file",
            font=("Roboto", 16, "bold"),
            width=200,
            height=34,
            corner_radius=14,
            fg_color="#1f6aa5",
            hover_color="#3d8fd4",
            command=self.open_file).pack(expand=True, fill="x", pady=(40, 0))

        # start button
        ctk.CTkButton(
            master=self,
            text="Start the Quiz",
            font=("Roboto", 16, "bold"),
            width=200,
            height=34,
            corner_radius=14,
            fg_color="#8310ee",
            hover_color="#51029c",
            command=self.start_quiz).pack(expand=True, fill="both", pady=(30, 50))
        
    # open filedialog to select a file
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=(("PDF File", "*.pdf"), ("All Files", "*.*")))

        if self.file_path:
            messagebox.showinfo(title="File Selected", message=f"{self.file_path.split("/")[-1]} selected")

    # initialize loading screen and start generating question
    def start_quiz(self):
        if self.file_path and os.path.exists(self.file_path):
            self.loading_page()
        else:
            messagebox.showerror(title="Input Error", message="File not selected.")
            return

        threading.Thread(target=self.generate_and_show_qa_page).start()

    # loading page
    def loading_page(self):

        # delete all widgets first
        for widget in self.winfo_children():
            widget.destroy()

        # loading label
        self.loading_label = ctk.CTkLabel(
            master=self,
            text="Loading. Please wait.",
            text_color="white",
            font=("Roboto", 24, "bold"))
        self.loading_label.pack(expand=True, fill="both")

    # helper function for switching to main thread
    def generate_and_show_qa_page(self):
        # Generate questions
        generataion = self.generate_questions(self.no_of_questions.get(), self.file_path)

        if generataion != 1:
            questions = generataion
        else:
            return

        # Switch to QA page on the main thread
        self.parent.after(0, lambda: self.show_qa_page(questions))

    # destroy welcome page & show qa page
    def show_qa_page(self, questions):
        # switch to qa page
        QAPage(self.parent, self.no_of_questions.get(), questions)
        self.destroy()

    # generate ai response
    def generate_questions(self, total_questions, file):

        # creating a pdf reader object 
        reader = PdfReader(file)

        self.loading_label.configure(text="Sending Generation request to AI.")

        # convert random pdf pages to jpeg
        random_page = random.randint(5, len(reader.pages))

        images_ppm = convert_from_path(self.file_path, poppler_path=os.path.abspath(os.path.join("Assets", "Release-24.02.0-0", "poppler-24.02.0", "Library", "bin")), first_page=random_page, last_page=random_page + 5)
        
        os.makedirs("images", exist_ok=True)

        for i, image in enumerate(images_ppm):
            image_path = os.path.join("images", f'page_{i+1}.png')
            image.save(image_path, 'PNG')

        print(f"Page No.{random_page} to {random_page + 5} selected")

        # creating an ai model
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        model = genai.GenerativeModel('gemini-1.5-flash',
                                      generation_config={"response_mime_type": "application/json"})


        self.loading_label.configure(text="Uploading.")

        # upload images to gemini
        images = os.listdir("images")

        for image in images:
            uploaded_images = genai.upload_file(path=os.path.abspath(os.path.join("images", image)),
                                                display_name=image)
            self.loading_label.configure(text=f"{round(images.index(image) / 5 * 100)}% Uploaded.")

        # delete images folder
        shutil.rmtree("images")

        self.loading_label.configure(text="Uploading Completed.")
        self.parent.after(2000, self.loading_label.configure(text="Generating Questions."))

        # generate response
        try:    
            response = model.generate_content([uploaded_images, f'''You are a College Professor teaching a student. Give user {total_questions} mcq based question with '4' options in which only and only 1 should be correct and also provide an answer based on the given prompt and some adjustments mentioned below, also don't use any word outside of the images there is an example below of how your questions should look and what should be its minimum length along with the professional word used in it. The question should not contain any traces of words like in this passage or paragraph and try to dont't use words repeatedly.
            Question Example: Question: Expenditure on most post -retirement benefits like provident fund, gratuity, etc. are
            covered by specific provisions. There are other post- retirem ent benefits offered by companies like medical benefits. Such benefits are covered by AS -15 for which no parallel ICDS has been notified. Whether provision for these liabilities are excluded from scope of ICDS X?
            SETTINGS: The json response given by you should be consistent and the options list should NOT contain any text like [a], [b], [c], or [d] and answer should be exact same as any correct option not containing other words or formatting.'''])

            self.loading_label.configure(text="Loading Questions.")

            return json.loads(response.text)
        
        except Exception as E:
            messagebox.showerror(title="Error from AI", message=E)
            return 1


class QAPage(ctk.CTkFrame,):

    # main setup
    def __init__(self, parent, total_questions, response):
        super().__init__(parent, fg_color="black")
        self.pack(expand=True, fill="both")
        self.response = {key.lower(): value for key, value in response.items()}
        self.question = None
        self.current_question = 0
        self.total_questions = total_questions

        # prints next question on the screen if there is one
        self.show_next_question()

        # next question button
        self.next_button = ctk.CTkButton(
            master=parent,
            text="Next ➤",
            height=50,
            width=50,
            font=("Helvatica", 24, "bold"),
            command=self.show_next_question)
        self.next_button.place(relx=0.944, rely=0.05, anchor="center")

    # prints next question on the screen
    def show_next_question(self):
        # first destroy if there is question on screen
        if self.question is not None:
            self.question.destroy()

        # check if there is any question left
        if self.current_question < self.total_questions:

            try:
                if self.total_questions == 1:
                    self.question = ShowQuestion(self,
                                    question_no=self.current_question + 1,
                                    question=self.response["question"],
                                    options=[self.response["options"][0],
                                            self.response["options"][1],
                                            self.response["options"][2],
                                            self.response["options"][3]],
                                    correct_answer=self.response["answer"])
                else:
                    self.question = ShowQuestion(self,
                                    question_no=self.current_question + 1,
                                    question=self.response["questions"][self.current_question]["question"],
                                    options=[self.response["questions"][self.current_question]["options"][0],
                                            self.response["questions"][self.current_question]["options"][1],
                                            self.response["questions"][self.current_question]["options"][2],
                                            self.response["questions"][self.current_question]["options"][3]],
                                    correct_answer=self.response["questions"][self.current_question]["answer"])

                self.current_question += 1
                
            except Exception:
                messagebox.showerror(title="Error in AI", message="There was an error in AI response. Please consider restarting the application.") 

        else:

            ctk.CTkLabel(
                master=self,
                text="Quiz Finished",
                bg_color="black",
                text_color="white",
                font=("Calibri", 32, "bold")
                ).place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                master=self,
                text=f"Score: {SCORE} / {self.total_questions}",
                bg_color="black",
                text_color="white",
                font=("Calibri", 24, "bold")
            ).place(relx=0.5, rely=0.8, anchor="center")

            ctk.CTkLabel(
                master=self,
                text=f"Percentage: {round(SCORE / self.total_questions * 100)}%",
                bg_color="black",
                text_color="white",
                font=("Calibri", 24, "bold")
            ).place(relx=0.5, rely=0.85, anchor="center")
            self.next_button.destroy()


class ShowQuestion(ctk.CTkFrame):

    # main setup
    def __init__(self, parent, question_no, question, options, correct_answer):
        super().__init__(parent, fg_color="black")
        self.options = options
        self.correct_answer = correct_answer
        self.first_answer = True

        self.pack(expand=True, fill="both")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)
        self.rowconfigure(5, weight=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        # question no label
        ctk.CTkLabel(
            master=self,
            text=f"Question No. {question_no}",
            text_color="white",
            font=("Helvatica", 28, "bold")).grid(row=0, column=1, sticky="w", padx=20, pady=5)

        # question label
        ctk.CTkLabel(
            master=self,
            text=question,
            wraplength=1450,
            fg_color="#2e2e2e",
            text_color="white",
            corner_radius=10,
            font=("Calibri", 24, "bold"),
            justify="left").grid(row=1, column=1, sticky="nsew", padx=20, pady=5)
        
        # options A button
        self.optionA = self.create_option(f"(A) {self.options[0]}", 2)
        self.optionA.configure(command=lambda: self.check_answer(self.optionA, self.options[0]))

        # options B button
        self.optionB = self.create_option(f"(B) {self.options[1]}", 3)
        self.optionB.configure(command=lambda: self.check_answer(self.optionB, self.options[1]))

        # options C button
        self.optionC = self.create_option(f"(C) {self.options[2]}", 4)
        self.optionC.configure(command=lambda: self.check_answer(self.optionC, self.options[2]))

        # options D button
        self.optionD = self.create_option(f"(D) {self.options[3]}", 5)
        self.optionD.configure(command=lambda: self.check_answer(self.optionD, self.options[3]))

    # returns a option button
    def create_option(self, text, row):
        button = ctk.CTkButton(
            master=self,
            text=text,
            text_color="white",
            width=500,
            corner_radius=10,
            border_spacing=10,
            anchor="w",
            font=("Calibri", 24),
            fg_color="black",
            hover_color="#3e3e3e",
            border_width=2,
            border_color="#7309b0")
        
        button._text_label.configure(wraplength=1850, justify="left")
        button.grid(row=row, column=1, sticky="ew", padx=20, pady=5)
        
        return button
    
    # checks the answer
    def check_answer(self, option, user_answer):
        global SCORE

        if user_answer == self.correct_answer:
            if self.first_answer:
                SCORE += 1
            self.optionA.configure(state="disabled")
            self.optionB.configure(state="disabled")
            self.optionC.configure(state="disabled")
            self.optionD.configure(state="disabled")
            option.configure(border_color="green")
        else:
            self.first_answer = False
            option.configure(border_color="red")

        self.master.update_idletasks()


app = App(title="QuizMaker")