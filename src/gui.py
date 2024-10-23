import tkinter as tk
from tkinter import ttk, messagebox
import threading


class ExpertSearchGUI:
    def __init__(self, root, search_experts_callback, display_expert_info_callback):
        self.root = root
        self.search_experts_callback = search_experts_callback
        self.display_expert_info_callback = display_expert_info_callback
        self.see_expert_url = ""
        self.see_work_url = ""

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

        # Buttons to see expert and expert's work
        self.see_expert_button = tk.Button(root, text="See Expert", command=self.see_expert)
        self.see_expert_button.pack(pady=5)
        self.see_expert_button.config(state="disabled")

        self.see_work_button = tk.Button(root, text="See Expert's Work", command=self.see_expert_work)
        self.see_work_button.pack(pady=5)
        self.see_work_button.config(state="disabled")

        # Frame to wrap the Text widget and add padding
        self.info_frame = tk.Frame(root, padx=10, pady=10)
        self.info_frame.pack()

        # Text widget to display expert information
        self.info_text = tk.Text(self.info_frame,  font=("Arial", 15), height=7, width=50, wrap="word")
        self.info_text.pack(expand=True)
        self.info_text.config(state="disabled")

        # Configure text tag to center-align the text
        self.info_text.tag_configure("center", justify="center")

        # Stats label
        self.expert_found_stats_label = tk.Label(root, text="")
        self.expert_found_stats_label.pack()

        # Stats label
        self.author_information_stats_label = tk.Label(root, text="")
        self.author_information_stats_label.pack()

    def update_expert_found_stats_label(self, text):
        self.expert_found_stats_label.config(text=text)

    def update_author_information_stats_label(self, text):
        self.author_information_stats_label.config(text=text)

    def search_experts(self):
        # Disable the search button to prevent multiple clicks
        self.search_button.config(state="disabled")
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Warning", "Please enter a topic.")
            # Re-enable button if no topic is entered
            self.search_button.config(state="normal")
            return
        threading.Thread(target=self.search_experts_callback, args=(topic,), daemon=True).start()

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

    def see_expert(self):
        threading.Thread(target=self.open_url, args=(self.see_expert_url,), daemon=True).start()

    def see_expert_work(self):
        threading.Thread(target=self.open_url, args=(self.see_work_url,), daemon=True).start()

    def set_see_expert_url(self, url):
        self.see_expert_url = url
        self.see_expert_button.config(state="normal")

    def set_see_work_url(self, url):
        self.see_work_url = url
        self.see_work_button.config(state="normal")

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
