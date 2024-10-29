from src import mongodb, search, fetch, utils
from src.gui import ExpertSearchGUI
import tkinter as tk
from tkinter import messagebox
import threading
import time

# Connect to the MongoDB collection
EXPERTS = list()
COLLECTION = mongodb.connect_db_collection(
    connection_string="mongodb://localhost:27018",
    db_string="openalexdb",
    collection_string="experts",
)


def search_experts_callback(topic):
    def fetch_and_update():
        start_time = time.time()
        root.after(0, gui.update_expert_found_stats_label(
            "Experts found in: calculating..."
        ))
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
            root.after(0, gui.update_expert_combobox(expert_names))
            end_time = time.time()

        # If no experts found
        else:
            end_time = time.time()
            root.after(0, messagebox.showerror("Not Found", "Couldn't find any expert for this topic"))
            root.after(0, gui.update_expert_combobox([]))

        # Update expert found stats label
        elapsed_time = end_time - start_time
        root.after(0, gui.update_expert_found_stats_label(
            f"Experts found in: {elapsed_time:.2f} seconds"
        ))

    # Start the fetching process in a separate thread
    threading.Thread(target=fetch_and_update, daemon=True).start()


def display_expert_info_callback(selected_expert_name):
    def fetch_expert_info():
        start_time = time.time()
        root.after(0, gui.update_expert_info_label("Fetching author information..."))
        root.after(0, gui.update_author_information_stats_label(
            "Author information fetched in: calculating..."
        ))
        # Fetch expert information from the list (or database if needed)
        expert = next((expert for expert in EXPERTS if expert['name'] == selected_expert_name), None)

        if expert:
            # Author informations
            author = fetch.fetch_author(expert['id'])
            expert['author_cited_by_count'] = author['cited_by_count']
            expert['author_h_index'] = author['summary_stats']['h_index']

            # Update hyperlink buttons
            root.after(0, gui.set_see_expert_url(f"https://openalex.org/authors/{expert['id']}"))
            root.after(0, gui.set_see_work_url(f"https://openalex.org/works/{expert['work_id']}"))

            expert_info = utils.create_expert_display_string(expert)
        else:
            expert_info = "Expert not found."

        # Update the info label in the main UI thread
        root.after(0, gui.update_expert_info_label(expert_info))

        # Update author information stats label
        end_time = time.time()
        elapsed_time = end_time - start_time
        root.after(0, gui.update_author_information_stats_label(
            f"Author information fetched in: {elapsed_time:.2f} seconds"
        ))

    # Start the fetching process in a separate thread
    threading.Thread(target=fetch_expert_info, daemon=True).start()


if __name__ == "__main__":
    # TO-DO:
    # * Citation filter will be calculated dynamically
    # * Improve expert finding formula
    #   * Slowing the search down because of the Author request is not much of a deal for the main objective
    # * Add filters to UI to let user use search filters
    #   * Min publication year
    #   * Article language
    #   * Expert country (country_code)

    # Set up the GUI
    root = tk.Tk()
    gui = ExpertSearchGUI(root, search_experts_callback, display_expert_info_callback)

    # Run the application
    root.mainloop()
