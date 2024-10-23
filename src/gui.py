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
        self.expert_combobox.config(state="disabled")

        # Frame to wrap the Text widget and add padding
        self.info_frame = tk.Frame(root, padx=10, pady=20)
        self.info_frame.pack(pady=10)

        # Text widget to display expert information
        self.info_text = tk.Text(self.info_frame,  font=("Arial", 15), height=7, width=50, wrap="word")
        self.info_text.pack(expand=True)
        self.info_text.config(state="disabled")

        # Configure text tag to center-align the text
        self.info_text.tag_configure("center", justify="center")

    def search_experts(self):
        # Disable the search button to prevent multiple clicks
        self.search_button.config(state="disabled")
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Warning", "Please enter a topic.")
            # Re-enable button if no topic is entered
            self.search_button.config(state="normal")
            return
        self.search_experts_callback(topic)

    def display_expert_info(self, event):
        selected_expert_name = self.expert_combobox.get()
        if not selected_expert_name:
            return
        self.display_expert_info_callback(selected_expert_name)

    def update_expert_combobox(self, expert_names):
        # Enable combobox when data is available
        self.expert_combobox.config(state="normal")
        self.expert_combobox['values'] = expert_names
        self.expert_combobox.set('')

        # Re-enable the search button after the search process completes
        self.search_button.config(state="normal")

    def update_expert_info_label(self, expert_info):
        # Enable the text widget to insert the new expert info, then make it read-only again
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, expert_info)

        # Apply the 'center' tag to center-align all the text
        self.info_text.tag_add("center", 1.0, "end")

        self.info_text.config(state="disabled")
