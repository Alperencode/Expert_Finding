from src import mongodb, search
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

        # Search database for the topic
        EXPERTS = mongodb.get_topic_experts_using_db(COLLECTION, topic)

        # If topic doesn't exists in database, use API
        if not EXPERTS:
            print("Topic doesn't exists in database, using API...")
            EXPERTS = search.extract_experts_using_api(topic)
            if EXPERTS:
                # Add experts to database
                mongodb.add_topic_and_experts(COLLECTION, topic, EXPERTS)

        # If experts found
        if EXPERTS:
            # Update combobox with expert names
            expert_names = [expert['name'] for expert in EXPERTS]
            root.after(0, lambda: gui.update_expert_combobox(expert_names))

        # If no experts found
        else:
            root.after(0, lambda: messagebox.showerror("Not Found", "Couldn't find any expert for this topic"))
            root.after(0, lambda: gui.update_expert_combobox([]))

    # Start the fetching process in a separate thread
    threading.Thread(target=fetch_and_update).start()


def display_expert_info_callback(selected_expert_name):
    def fetch_expert_info():
        # Fetch expert information from the list (or database if needed)
        expert = next((expert for expert in EXPERTS if expert['name'] == selected_expert_name), None)

        if expert:
            # Update hyperlink buttons
            root.after(0, lambda: gui.set_see_expert_url(f"https://openalex.org/authors/{expert['id']}"))
            root.after(0, lambda: gui.set_see_work_url(f"https://openalex.org/works/{expert['work_id']}"))

            expert_info = f"Name: {expert['name']}\nID: {expert['id']}\nWork ID: {expert['work_id']}"
        else:
            expert_info = "Expert not found."

        # Update the info label in the main UI thread
        root.after(0, lambda: gui.update_expert_info_label(expert_info))

    # Start the fetching process in a separate thread
    threading.Thread(target=fetch_expert_info).start()


if __name__ == "__main__":
    # TO-DO:
    # * Improve Author Information Display
    # * Improve expert finding formula

    # Set up the GUI
    root = tk.Tk()
    gui = ExpertSearchGUI(root, search_experts_callback, display_expert_info_callback)

    # Run the application
    root.mainloop()
