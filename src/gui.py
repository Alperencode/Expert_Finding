import tkinter as tk
from tkinter import ttk, messagebox


class ExpertSearchGUI:
    def __init__(self, root, search_experts_callback, display_expert_info_callback):
        self.root = root
        self.search_experts_callback = search_experts_callback
        self.display_expert_info_callback = display_expert_info_callback

        root.title("Expert Search")

        # Search box for topic
        self.topic_label = tk.Label(root, text="Enter Topic:")
        self.topic_label.pack(pady=5)

        self.topic_entry = tk.Entry(root)
        self.topic_entry.pack(pady=5)

        # Search button
        self.search_button = tk.Button(root, text="Search", command=self.search_experts)
        self.search_button.pack(pady=5)

        # Combobox for expert names
        self.expert_label = tk.Label(root, text="Select Expert:")
        self.expert_label.pack(pady=5)

        self.expert_combobox = ttk.Combobox(root)
        self.expert_combobox.bind("<<ComboboxSelected>>", self.display_expert_info)
        self.expert_combobox.pack(pady=5)
        self.expert_combobox.config(state="disabled")  # Disabled initially

        # Label to display expert information
        self.info_label = tk.Label(root, text="")
        self.info_label.pack(pady=10)

    def search_experts(self):
        # Disable the search button to prevent multiple clicks
        self.search_button.config(state="disabled")
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Warning", "Please enter a topic.")
            self.search_button.config(state="normal")  # Re-enable button if no topic is entered
            return
        self.search_experts_callback(topic)

    def display_expert_info(self, event):
        selected_expert_name = self.expert_combobox.get()
        if not selected_expert_name:
            return
        self.display_expert_info_callback(selected_expert_name)

    def update_expert_combobox(self, expert_names):
        self.expert_combobox.config(state="normal")  # Enable combobox when data is available
        self.expert_combobox['values'] = expert_names
        self.expert_combobox.set('')

        # Re-enable the search button after the search process completes
        self.search_button.config(state="normal")

    def update_expert_info_label(self, expert_info):
        self.info_label.config(text=expert_info)
