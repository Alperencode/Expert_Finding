from src import mongodb, fetch, search
from src.gui import ExpertSearchGUI
import tkinter as tk
from tkinter import messagebox
import threading

# Connect to the MongoDB collection
EXPERTS = list()
COLLECTION = mongodb.connect_db_collection(
    connection_string="mongodb://localhost:27018",
    db_string="openalexdb",
    collection_string="experts",
)


def search_experts_callback(topic):
    def fetch_and_update():
        global EXPERTS
        # Fetch works from OpenAlex API
        PARAMS = {
            "sort": "cited_by_count:DESC",
            "per_page": 50,
            "filter": f"display_name.search:{topic}"
        }
        works = fetch.fetch_works("https://api.openalex.org/works", PARAMS)

        if works:
            # Find experts
            EXPERTS = search.extract_experts(works, topic)
            if not EXPERTS:
                root.after(0, lambda: messagebox.showerror("Not Found", "Couldn't find any expert for this topic"))
                return

            # Add experts to MongoDB
            mongodb.add_topic_and_experts(COLLECTION, topic, EXPERTS)
            expert_names = [expert['name'] for expert in EXPERTS]

            # Update the combobox
            root.after(0, lambda: gui.update_expert_combobox(expert_names))
        else:
            root.after(0, lambda: messagebox.showerror("Error", "No works found or an error occurred."))

    # Start the fetching process in a separate thread
    threading.Thread(target=fetch_and_update).start()


def display_expert_info_callback(selected_expert_name):
    def fetch_expert_info():
        # Fetch expert information from the list (or database if needed)
        expert = next((expert for expert in EXPERTS if expert['name'] == selected_expert_name), None)

        if expert:
            expert_info = f"Name: {expert['name']}\nID: {expert['id']}\nWork ID: {expert['work_id']}"
        else:
            expert_info = "Expert not found."

        # Update the info label in the main UI thread
        root.after(0, lambda: gui.update_expert_info_label(expert_info))

    # Start the fetching process in a separate thread
    threading.Thread(target=fetch_expert_info).start()


if __name__ == "__main__":
    # TO-DO:
    # * Check MongoDB first for the topic
    # * If not, then use API
    # * Improve Author Information Display
    # * Improve expert finding formula

    # Set up the GUI
    root = tk.Tk()
    gui = ExpertSearchGUI(root, search_experts_callback, display_expert_info_callback)

    # Run the application
    root.mainloop()
