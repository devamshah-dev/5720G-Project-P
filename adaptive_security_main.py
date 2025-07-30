# adaptive_security_main.py
import tkinter as tk
from tkinter import font
import sys
import time

import data_loader
import auth_model

class AdaptiveSecurityGUI:
    def __init__(self, master, scenarios):
        self.master = master
        self.scenarios = scenarios
        master.title("Adaptive Security Simulation")
        master.geometry("500x600")
        master.configure(bg="#f0f0f0")

        self.user_profile = {
            "name": "Dev",
            "usual_location": "Home",
            "usual_location": "Ontario Tech University",
            "usual_time_start": 8,
            "usual_time_end": 20,
            "touch_pattern_similarity": 0.5,
        }
        self.current_scenario_index = 0
        self.security_level = "Low"
        self.app_locked = True
        self.risk_reason = "Context-Aware Application Initializing..."

        # GUI
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=10)
        self.status_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.title_label = tk.Label(master, text="Adaptive Security & Continuous Authentication", font=self.title_font, bg="#f0f0f0")
        self.title_label.pack(pady=10)
        self.scenario_label = tk.Label(master, text="", font=self.header_font, bg="#f0f0f0", fg="#00008B")
        self.scenario_label.pack(pady=10)
        context_frame = tk.LabelFrame(master, text="Current Context", font=self.header_font, padx=10, pady=10, bg="#f0f0f0")
        context_frame.pack(pady=10, padx=20, fill="x")
        self.location_label = tk.Label(context_frame, text="Location:", font=self.label_font, bg="#f0f0f0")
        self.location_label.grid(row=0, column=0, sticky="w", pady=2)
        self.location_value = tk.Label(context_frame, text="", font=self.label_font, bg="#f0f0f0")
        self.location_value.grid(row=0, column=1, sticky="w")
        self.time_label = tk.Label(context_frame, text="Time:", font=self.label_font, bg="#f0f0f0")
        self.time_label.grid(row=1, column=0, sticky="w", pady=2)
        self.time_value = tk.Label(context_frame, text="", font=self.label_font, bg="#f0f0f0")
        self.time_value.grid(row=1, column=1, sticky="w")
        self.touch_label = tk.Label(context_frame, text="Touch Similarity:", font=self.label_font, bg="#f0f0f0")
        self.touch_label.grid(row=2, column=0, sticky="w", pady=2)
        self.touch_value = tk.Label(context_frame, text="", font=self.label_font, bg="#f0f0f0")
        self.touch_value.grid(row=2, column=1, sticky="w")
        status_frame = tk.LabelFrame(master, text="Security Status", font=self.header_font, padx=10, pady=10, bg="#f0f0f0")
        status_frame.pack(pady=10, padx=20, fill="x")
        self.security_level_label = tk.Label(status_frame, text="Security Level:", font=self.status_font, bg="#f0f0f0")
        self.security_level_label.pack()
        self.security_level_value = tk.Label(status_frame, text="", font=self.title_font, width=20, relief="sunken", bd=2)
        self.security_level_value.pack(pady=5)
        self.app_status_label = tk.Label(status_frame, text="Smartphone Status:", font=self.status_font, bg="#f0f0f0")
        self.app_status_label.pack()
        self.app_status_value = tk.Label(status_frame, text="", font=self.title_font, width=20, relief="sunken", bd=2)
        self.app_status_value.pack(pady=5)
        self.reason_label = tk.Label(status_frame, text="", font=self.label_font, bg="#f0f0f0", wraplength=450)
        self.reason_label.pack(pady=5)
        self.run_button = tk.Button(master, text="Run Next Scenario", command=self.run_simulation_step, font=self.header_font)
        self.run_button.pack(pady=20)

        # initialize first state
        self.run_simulation_step()

    def evaluate_context(self, context):
        risk_score = 0
        reasons = []
        if context["location"] != self.user_profile["usual_location"]:
            risk_score += 1
            reasons.append("Unusual location detected.")
        if not (self.user_profile["usual_time_start"] <= context["time"] <= self.user_profile["usual_time_end"]):
            risk_score += 1
            reasons.append("Access at an unusual time.")
        if context["touch_pattern"] < self.user_profile["touch_pattern_similarity"]:
            risk_score += 2
            reasons.append("Abnormal touch pattern detected (potential unauthorized user).")

        if risk_score == 0:
            self.security_level = "Low"
            self.app_locked = False
            self.risk_reason = "Context is normal. Access granted."
        elif risk_score <= 1:
            self.security_level = "Medium"
            self.app_locked = True
            self.risk_reason = "Slightly unusual context. Re-authentication would be required. " + " ".join(reasons)
        else:
            self.security_level = "High"
            self.app_locked = True
            self.risk_reason = "High-risk context detected! Access locked. " + " ".join(reasons)

    def update_gui(self, context):
        self.scenario_label.config(text=context["scenario_text"])
        self.location_value.config(text=context["location"])
        self.time_value.config(text=f"{context['time']}:00")
        self.touch_value.config(text=f"{context['touch_pattern']:.2f}")
        self.security_level_value.config(text=self.security_level)
        self.app_status_value.config(text="LOCKED" if self.app_locked else "UNLOCKED")
        self.reason_label.config(text=f"Reason: {self.risk_reason}")

        color_map = {"Low": "#90EE90", "Medium": "#FFD700", "High": "#F08080"}
        text_color = "black" if self.security_level != "High" else "white"
        bg_color = color_map.get(self.security_level, "white")
        self.security_level_value.config(bg=bg_color, fg=text_color)
        self.app_status_value.config(bg=bg_color, fg=text_color)

        if self.current_scenario_index >= len(self.scenarios):
            self.run_button.config(text="Restart Simulation", command=self.restart_simulation)

    def run_simulation_step(self):
        if self.current_scenario_index < len(self.scenarios):
            base_scenario = self.scenarios[self.current_scenario_index]
            current_context = base_scenario.copy()
            
            # auth_model to get a simulated touch pattern
            base_touch = base_scenario['touch_pattern_base']
            simulated_touch = auth_model.analyze_touch(base_touch)
            current_context['touch_pattern'] = simulated_touch
            
            self.evaluate_context(current_context)
            self.update_gui(current_context)
            self.current_scenario_index += 1

    def restart_simulation(self):
        self.current_scenario_index = 0
        self.run_button.config(text="Run Next Scenario", command=self.run_simulation_step)
        self.run_simulation_step()

if __name__ == "__main__":
    # load scenarios from the external file first
    scenarios_from_csv = data_loader.load_scenarios()
    
    # scenarios loaded successfully, start the app
    if scenarios_from_csv:
        root = tk.Tk()
        my_gui = AdaptiveSecurityGUI(root, scenarios_from_csv)
        root.mainloop()
    else:
        # Exit if the data file could not be loaded
        sys.exit(1)