# pyrefly: ignore [missing-import]
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time
from model_loader import ModelLoader

# Apply global settings for a modern appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ChatbotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fake News Detector AI")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        
        # Instantiate model loader
        self.model_loader = ModelLoader()
        
        # History queue
        self.history = []

        # Configure main grid
        self.grid_columnconfigure(0, weight=1) # Sidebar
        self.grid_columnconfigure(1, weight=4) # Main Content
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        
        # Initial AI greeting
        self.add_ai_message("System initialized. Loading neural models...")
        self.after(1200, lambda: self.add_ai_message("Models loaded. Ready for analysis. Awaiting input..."))

    def create_sidebar(self):
        """Creates the sidebar containing the title, status, sample buttons, and history."""
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#121212")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1) # Push theme selector to bottom

        # App Title / Header
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🛡️ AI Detector", font=ctk.CTkFont(size=26, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        status_text = "Online (Fallback)" if self.model_loader.is_mock else "Online (ML Loaded)"
        status_color = "#FFA500" if self.model_loader.is_mock else "#00FF00"
        self.status_label = ctk.CTkLabel(self.sidebar_frame, text=f"Status: {status_text}", text_color=status_color, font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Sample Inputs
        self.sample_label = ctk.CTkLabel(self.sidebar_frame, text="Test Samples:", font=ctk.CTkFont(size=15, weight="bold"))
        self.sample_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")

        samples = [
            ("Real News Example", "The World Health Organization announced new guidelines for global pandemic preparedness today after an extensive study."),
            ("Fake News Example", "SHOCKING EXPOSED: Scientists discover that drinking motor oil cures all diseases! You won't believe it!"),
            ("Ambiguous Example", "Experts debate the future of the economy amid rising inflation and unexpected stock market volatility."),
            ("Antigravity Mode 🚀", "BREAKING: Scientists accidentally invented antigravity coffee. The coffee escaped the mug and is now orbiting the kitchen ceiling.")
        ]

        for i, (title, text) in enumerate(samples):
            btn = ctk.CTkButton(self.sidebar_frame, text=title, command=lambda t=text: self.load_sample(t),
                                fg_color="#2B2B2B", hover_color="#3D3D3D", border_width=1, border_color="#3A3A3A")
            btn.grid(row=3+i, column=0, padx=20, pady=5, sticky="ew")

        # History Area
        self.history_label = ctk.CTkLabel(self.sidebar_frame, text="Recent Analysis:", font=ctk.CTkFont(size=15, weight="bold"))
        self.history_label.grid(row=7, column=0, padx=20, pady=(30, 5), sticky="w")
        
        self.history_textbox = ctk.CTkTextbox(self.sidebar_frame, width=240, height=200, wrap="word", fg_color="#1E1E1E", border_width=1, border_color="#333333")
        self.history_textbox.grid(row=8, column=0, padx=20, pady=5, sticky="nsew")
        self.history_textbox.configure(state="disabled")

        # Theme Switch
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                               command=self.change_appearance_mode_event,
                                                               fg_color="#1F538D", button_color="#14375E", button_hover_color="#102C4A")
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=20, sticky="ew")

    def create_main_area(self):
        """Creates the main content area with chatbot UI, input field, and result display."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=3) # AI Chat
        self.main_frame.grid_rowconfigure(1, weight=1) # Input
        self.main_frame.grid_rowconfigure(2, weight=0) # Results

        # AI Chatbot Area
        self.chat_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#1E1E1E", border_width=1, border_color="#333333")
        self.chat_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        
        self.chat_textbox = ctk.CTkTextbox(self.chat_frame, font=ctk.CTkFont(family="Helvetica", size=15), wrap="word", fg_color="transparent")
        self.chat_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.chat_textbox.configure(state="disabled")
        self.chat_textbox.tag_config("ai_tag", foreground="#00BFFF")
        self.chat_textbox.tag_config("user_tag", foreground="#AAAAAA")

        # Input Area
        self.input_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#1E1E1E", border_width=1, border_color="#333333")
        self.input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)

        self.input_textbox = ctk.CTkTextbox(self.input_frame, height=120, font=ctk.CTkFont(size=15), wrap="word", fg_color="#252525")
        self.input_textbox.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")
        self.input_textbox.insert("0.0", "Paste article text, news excerpt, or headline here for analysis...")
        self.input_textbox.bind("<FocusIn>", self.clear_placeholder)
        
        # Button controls below input
        self.btn_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="e")
        
        self.clear_btn = ctk.CTkButton(self.btn_frame, text="Clear", width=100, command=self.clear_input,
                                       fg_color="transparent", border_width=1, border_color="#555555", hover_color="#333333")
        self.clear_btn.pack(side="left", padx=10)

        self.analyze_btn = ctk.CTkButton(self.btn_frame, text="Analyze Content 🔍", font=ctk.CTkFont(size=15, weight="bold"), 
                                         command=self.start_analysis, fg_color="#1F538D", hover_color="#14375E", width=160, height=35)
        self.analyze_btn.pack(side="left")

        # Results Dashboard
        self.results_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#202020", border_width=2, border_color="#444444")
        self.results_frame.grid(row=2, column=0, sticky="nsew")
        self.results_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.res_title = ctk.CTkLabel(self.results_frame, text="AI Analysis Report", font=ctk.CTkFont(size=18, weight="bold"), text_color="#DDDDDD")
        self.res_title.grid(row=0, column=0, columnspan=4, pady=(15, 5))

        self.pred_label = ctk.CTkLabel(self.results_frame, text="AWAITING INPUT", font=ctk.CTkFont(size=26, weight="bold"), text_color="#555555")
        self.pred_label.grid(row=1, column=0, padx=15, pady=(5, 20))
        
        self.conf_label = ctk.CTkLabel(self.results_frame, text="Confidence:\n--%", font=ctk.CTkFont(size=15))
        self.conf_label.grid(row=1, column=1, padx=15, pady=(5, 20))

        self.risk_label = ctk.CTkLabel(self.results_frame, text="Risk Level:\n--", font=ctk.CTkFont(size=15))
        self.risk_label.grid(row=1, column=2, padx=15, pady=(5, 20))

        self.exp_label = ctk.CTkLabel(self.results_frame, text="Explanation:\nPlease provide text to scan.", font=ctk.CTkFont(size=13), wraplength=280)
        self.exp_label.grid(row=1, column=3, padx=15, pady=(5, 20))

    def load_sample(self, text):
        self.input_textbox.delete("0.0", "end")
        self.input_textbox.insert("0.0", text)

    def clear_placeholder(self, event):
        current_text = self.input_textbox.get("0.0", "end").strip()
        if current_text == "Paste article text, news excerpt, or headline here for analysis...":
            self.input_textbox.delete("0.0", "end")

    def clear_input(self):
        self.input_textbox.delete("0.0", "end")
        self.reset_results()
        self.add_ai_message("Input cleared. Ready for next analysis.")

    def reset_results(self):
        self.pred_label.configure(text="AWAITING INPUT", text_color="#555555")
        self.conf_label.configure(text="Confidence:\n--%")
        self.risk_label.configure(text="Risk Level:\n--")
        self.exp_label.configure(text="Explanation:\nPlease provide text to scan.")
        self.results_frame.configure(border_color="#444444")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def add_ai_message(self, message, is_user=False):
        self.chat_textbox.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if is_user:
            self.chat_textbox.insert("end", f"[{timestamp}] You: ", "user_tag")
            self.chat_textbox.insert("end", f"{message}\n\n", "user_tag")
        else:
            self.chat_textbox.insert("end", f"[{timestamp}] AI Assistant: ", "ai_tag")
            self.chat_textbox.insert("end", f"{message}\n\n")
            
        self.chat_textbox.see("end")
        self.chat_textbox.configure(state="disabled")

    def update_history(self, pred, conf, text):
        timestamp = datetime.now().strftime("%H:%M")
        preview = (text[:35] + "...") if len(text) > 35 else text
        hist_entry = f"[{timestamp}] {pred} ({conf}%)\n\"{preview}\"\n\n"
        
        self.history.append(hist_entry)
        if len(self.history) > 12:
            self.history.pop(0)
            
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("0.0", "end")
        # Show newest first
        for h in reversed(self.history):
            self.history_textbox.insert("end", h)
        self.history_textbox.configure(state="disabled")

    def start_analysis(self):
        text = self.input_textbox.get("0.0", "end").strip()
        if not text or text == "Paste article text, news excerpt, or headline here for analysis...":
            messagebox.showwarning("Empty Input", "Please enter some text to analyze.")
            return

        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        self.reset_results()
        
        preview = (text[:40] + "...") if len(text) > 40 else text
        self.add_ai_message(f"Analyzing snippet: '{preview}'", is_user=True)
        self.add_ai_message("Scanning article credibility signals...")
        
        # Run backend prediction in a separate thread so UI doesn't freeze
        threading.Thread(target=self.run_prediction, args=(text,), daemon=True).start()

    def run_prediction(self, text):
        # Simulated delays to feel like a deep scan
        time.sleep(0.8)
        self.add_ai_message("Detecting emotional manipulation patterns and linguistic anomalies...")
        time.sleep(0.8)
        self.add_ai_message("Checking source reliability heuristics and cross-referencing structure...")
        time.sleep(0.8)
        
        result = self.model_loader.predict(text)
        
        # Safely update the GUI components from the main thread
        self.after(0, self.display_results, result, text)

    def display_results(self, result, text):
        pred = result["prediction"]
        conf = result["confidence"]
        risk = result["risk_level"]
        exp = result["explanation"]

        self.add_ai_message(f"Analysis complete. Verdict: {pred} | Confidence: {conf}%")

        # Update Result Dashboard
        if pred in ["REAL", "FAKE"]:
            self.pred_label.configure(text=f"{pred} NEWS")
        else:
            self.pred_label.configure(text=f"{pred}")
            
        self.conf_label.configure(text=f"Confidence:\n{conf}%")
        self.risk_label.configure(text=f"Risk Level:\n{risk}")
        self.exp_label.configure(text=f"Explanation:\n{exp}")

        # Visual Indicators (Colors)
        if pred == "REAL":
            self.pred_label.configure(text_color="#00FF00") # Bright Green
            self.results_frame.configure(border_color="#00FF00")
        elif pred == "FAKE":
            self.pred_label.configure(text_color="#FF3333") # Bright Red
            self.results_frame.configure(border_color="#FF3333")
        elif pred == "ANTIGRAVITY":
            self.pred_label.configure(text_color="#FF00FF") # Neon Pink/Purple
            self.results_frame.configure(border_color="#FF00FF")
            self.add_ai_message("🚀 ANTIGRAVITY DETECTED! Physics engine failing... Please remain seated.", is_user=False)
        else:
            self.pred_label.configure(text_color="#FFFF00") # Yellow
            self.results_frame.configure(border_color="#FFFF00")

        self.update_history(pred, conf, text)
        self.analyze_btn.configure(state="normal", text="Analyze Content 🔍")
