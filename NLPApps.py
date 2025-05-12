import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import nlpcloud
import mysql.connector

 #API Key
API_KEY = "00404077a862ccf5a0fe77ff075c785d4520b7cd"
MODEL = "finetuned-llama-3-70b"

class NLPAppGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("NLP Application")
        self.root.geometry("800x500")

        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="nlp_app"
        )
        self.cursor = self.conn.cursor()
        self.create_user_table()

        # Load background image
        self.bg_image = Image.open("nlp.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((800, 500)))
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.login_frame = tk.Frame(self.root, bg="#001f33", padx=20, pady=20, bd=5, relief=tk.RIDGE)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.main_menu()

    def create_user_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                name VARCHAR(255) NOT NULL,
                                email VARCHAR(255) PRIMARY KEY,
                                password VARCHAR(255) NOT NULL)''')
        self.conn.commit()

    def clear_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.login_frame, text="Welcome to NLP App", font=("Arial", 18, "bold"), fg="#00ffe5", bg="#001f33").pack(pady=10)
        tk.Button(self.login_frame, text="Register", width=20, bg="#4CAF50", fg="white", font=("Arial", 12), command=self.register).pack(pady=5)
        tk.Button(self.login_frame, text="Login", width=20, bg="#2196F3", fg="white", font=("Arial", 12), command=self.login).pack(pady=5)
        tk.Button(self.login_frame, text="Exit", width=20, bg="#f44336", fg="white", font=("Arial", 12), command=self.root.quit).pack(pady=5)

    def register(self):
        self.clear_frame()
        tk.Label(self.login_frame, text="Register", font=("Arial", 16, "bold"), fg="#ffffff", bg="#001f33").pack(pady=10)

        tk.Label(self.login_frame, text="Name", fg="white", bg="#001f33", font=("Arial", 12)).pack()
        name_var = tk.StringVar()
        tk.Entry(self.login_frame, textvariable=name_var, width=30, font=("Arial", 12)).pack(pady=5)

        tk.Label(self.login_frame, text="Email", fg="white", bg="#001f33", font=("Arial", 12)).pack()
        email_var = tk.StringVar()
        tk.Entry(self.login_frame, textvariable=email_var, width=30, font=("Arial", 12)).pack(pady=5)

        tk.Label(self.login_frame, text="Password", fg="white", bg="#001f33", font=("Arial", 12)).pack()
        pass_var = tk.StringVar()
        tk.Entry(self.login_frame, textvariable=pass_var, show="*", width=30, font=("Arial", 12)).pack(pady=5)

        def submit():
            name = name_var.get()
            email = email_var.get()
            password = pass_var.get()

            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showerror("Error", "Invalid email format")
                return

            self.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already exists")
                return

            self.cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.main_menu()

        tk.Button(self.login_frame, text="Submit", bg="#4CAF50", fg="white", font=("Arial", 12), command=submit).pack(pady=10)
        tk.Button(self.login_frame, text="Back", bg="#9E9E9E", fg="white", font=("Arial", 12), command=self.main_menu).pack()

    def login(self):
        self.clear_frame()
        tk.Label(self.login_frame, text="Login", font=("Arial", 16, "bold"), fg="#ffffff", bg="#001f33").pack(pady=10)

        tk.Label(self.login_frame, text="Email", fg="white", bg="#001f33", font=("Arial", 12)).pack()
        email_var = tk.StringVar()
        tk.Entry(self.login_frame, textvariable=email_var, width=30, font=("Arial", 12)).pack(pady=5)

        tk.Label(self.login_frame, text="Password", fg="white", bg="#001f33", font=("Arial", 12)).pack()
        pass_var = tk.StringVar()
        tk.Entry(self.login_frame, textvariable=pass_var, show="*", width=30, font=("Arial", 12)).pack(pady=5)

        def submit():
            email = email_var.get()
            password = pass_var.get()
            self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            if self.cursor.fetchone():
                messagebox.showinfo("Success", "Login successful")
                self.nlp_menu()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.login_frame, text="Login", bg="#2196F3", fg="white", font=("Arial", 12), command=submit).pack(pady=10)
        tk.Button(self.login_frame, text="Back", bg="#9E9E9E", fg="white", font=("Arial", 12), command=self.main_menu).pack()

    def nlp_menu(self):
        self.clear_frame()
        tk.Label(self.login_frame, text="NLP Operations", font=("Arial", 16), fg="#ffffff", bg="#001f33").pack(pady=10)
        tk.Button(self.login_frame, text="Named Entity Recognition", width=30, command=self.ner).pack(pady=5)
        tk.Button(self.login_frame, text="Sentiment Analysis", width=30, command=self.sentiment).pack(pady=5)
        tk.Button(self.login_frame, text="Language Detection", width=30, command=self.language).pack(pady=5)
        tk.Button(self.login_frame, text="Logout", width=30, command=self.main_menu).pack(pady=5)

    def ner(self):
        self.clear_frame()
        para = tk.Text(self.login_frame, height=5, width=50)
        tk.Label(self.login_frame, text="Enter Paragraph:", bg="#001f33", fg="#ffffff").pack()
        para.pack()

        entity_var = tk.StringVar()
        tk.Label(self.login_frame, text="Entity to search (e.g. location, person):", bg="#001f33", fg="#ffffff").pack()
        tk.Entry(self.login_frame, textvariable=entity_var).pack()

        def analyze():
            try:
                client = nlpcloud.Client(MODEL, API_KEY, gpu=True)
                response = client.entities(para.get("1.0", tk.END), searched_entity=entity_var.get())
                if response:
                    messagebox.showinfo("Result", str(response))
                else:
                    messagebox.showerror("Error", "No response received from NLP Cloud.")
            except Exception as e:
                messagebox.showerror("API Error", f"An error occurred:\n{str(e)}")

        tk.Button(self.login_frame, text="Analyze", command=analyze).pack(pady=10)
        tk.Button(self.login_frame, text="Back", command=self.nlp_menu).pack()

    def sentiment(self):
        self.clear_frame()
        para = tk.Text(self.login_frame, height=5, width=50)
        tk.Label(self.login_frame, text="Enter Paragraph:", bg="#001f33", fg="#ffffff").pack()
        para.pack()

        def analyze():
            try:
                client = nlpcloud.Client(MODEL, API_KEY, gpu=True)
                response = client.sentiment(para.get("1.0", tk.END))
                scored = response.get("scored_labels", [])
                if scored:
                    label = max(scored, key=lambda x: x["score"])["label"]
                    messagebox.showinfo("Sentiment", f"Detected Sentiment: {label}")
                else:
                    messagebox.showwarning("Warning", "No sentiment detected.")
            except Exception as e:
                messagebox.showerror("API Error", f"An error occurred:\n{str(e)}")

        tk.Button(self.login_frame, text="Analyze", command=analyze).pack(pady=10)
        tk.Button(self.login_frame, text="Back", command=self.nlp_menu).pack()

    def language(self):
        self.clear_frame()
        para = tk.Text(self.login_frame, height=5, width=50)
        tk.Label(self.login_frame, text="Enter Paragraph:", bg="#001f33", fg="#ffffff").pack()
        para.pack()

        def detect():
            try:
                client = nlpcloud.Client("python-langdetect", API_KEY, gpu=False)
                # Corrected the method call below:
                response = client.langdetection(para.get("1.0", tk.END))  # Removed the labels parameter
                detected_language = response.get("language", {}).get("language_name", "Unknown")
                messagebox.showinfo("Language Detected", f"Language: {detected_language}")
            except Exception as e:
                messagebox.showerror("API Error", f"An error occurred:\n{str(e)}")

        tk.Button(self.login_frame, text="Detect", command=detect).pack(pady=10)
        tk.Button(self.login_frame, text="Back", command=self.nlp_menu).pack()

# Start App
if __name__ == "__main__":
    root = tk.Tk()
    app = NLPAppGUI(root)
    root.mainloop()
