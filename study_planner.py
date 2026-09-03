# SMART STUDY PLANNER
# Author: JESSE BYABAGAMBI
# Purpose: Track, review and analyze study sessions over a semester

import os

# Global list to store all the study session dictionaries
sessions = []
FILE_NAME = "study_log.txt"


def classify_session(duration):
    """
    Part (c): Classifies a session based on minutes.
    Must be reused whenever a session is displayed on screen.
    """
    # Simple if-elif-else layout that is easy to read
    if duration < 30:
        return "Short"
    elif duration >= 30 and duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session():
    """
    Part (b): Prompts user for details and validates duration.
    """
    print("\n--- ENTER NEW STUDY SESSION ---")
    
    # Gathering basic string details
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date_label = input("Enter date or day label (e.g. Monday, 2026-05-12): ").strip()
    
    # Loop until the user types a correct, positive number for duration
    while True:
        duration_input = input("Enter duration in minutes: ").strip()
        
        # Check if it's numeric first to prevent the program from crashing
        if duration_input.isdigit():
            duration = int(duration_input)
            if duration > 0:
                break # Valid input, exit the while loop
            else:
                print("Invalid! Duration must be greater than 0.")
        else:
            print("Invalid input! Please enter a whole positive number.")
            
    # Bundling the data into a standard dictionary
    session_dict = {
        "subject": subject,
        "topic": topic,
        "date_label": date_label,
        "duration": duration
    }
    
    # Adding it to our global list
    sessions.append(session_dict)
    print("Success! Your session has been added.")


def view_sessions():
    """
    Part (d): Displays all sessions in a clean, hand-spaced table.
    """
    # Quick check if the list is completely empty
    if len(sessions) == 0:
        print("\nNo sessions found. Go add some first!")
        return
        
    print("\n" + "-" * 75)
    # Using standard string formatting with manually assigned column widths
    print("{:<15} | {:<20} | {:<12} | {:<8} | {:<10}".format("Subject", "Topic", "Date/Day", "Minutes", "Class"))
    print("-" * 75)
    
    # Loop through each item and call the classification function
    for s in sessions:
        category = classify_session(s["duration"])
        print("{:<15} | {:<20} | {:<12} | {:<8} | {:<10}".format(
            s["subject"], s["topic"], s["date_label"], s["duration"], category
        ))
    print("-" * 75)


def search_by_subject():
    """
    Part (e): Case-insensitive search by subject name.
    """
    if len(sessions) == 0:
        print("\nThere are no sessions in the system to search.")
        return
        
    search_term = input("\nEnter the subject name to find: ").strip().lower()
    
    # Trackers for our search findings
    found_any = False
    total_minutes = 0
    
    print("\n" + "-" * 75)
    print("{:<15} | {:<20} | {:<12} | {:<8} | {:<10}".format("Subject", "Topic", "Date/Day", "Minutes", "Class"))
    print("-" * 75)
    
    # Loop and look for matches using .lower() for case insensitivity
    for s in sessions:
        if s["subject"].lower() == search_term:
            found_any = True
            total_minutes += s["duration"]
            category = classify_session(s["duration"])
            print("{:<15} | {:<20} | {:<12} | {:<8} | {:<10}".format(
                s["subject"], s["topic"], s["date_label"], s["duration"], category
            ))
            
    print("-" * 75)
    
    # Display the final summary or a clean error message if nothing matched
    if found_any:
        print(f"Total time spent on this subject: {total_minutes} minutes.")
    else:
        # Clear out the unneeded empty table headers printed above if nothing matched
        print(f"No sessions were found matching the subject: '{search_term}'.")


def study_statistics():
    """
    Part (f): Calculates overall hours, subject totals, weakest area, and longest session.
    """
    if len(sessions) == 0:
        print("\nNo statistics available. Please add data first!")
        return
        
    # 1. Calculate overall hours
    total_mins = 0
    for s in sessions:
        total_mins += s["duration"]
    overall_hours = total_mins / 60
    
    # 2. Track maximum duration session
    longest_session = sessions[0]
    for s in sessions:
        if s["duration"] > longest_session["duration"]:
            longest_session = s
            
    # 3. Track times per subject using a dictionary accumulator loop
    subject_map = {}
    for s in sessions:
        subj = s["subject"]
        if subj in subject_map:
            subject_map[subj] += s["duration"]
        else:
            subject_map[subj] = s["duration"]
            
    # 4. Find the minimum time spent (weakest area)
    # Using a basic human loop to find the minimum instead of complex built-ins
    weakest_subj = None
    min_time = 999999999 # Large placeholder number to start comparing
    
    for subj in subject_map:
        if subject_map[subj] < min_time:
            min_time = subject_map[subj]
            weakest_subj = subj
            
    # Printing out the final stats screen cleanly
    print("\n========================================")
    print("           OVERALL STATISTICS           ")
    print("========================================")
    print(f"Total Time Studied: {overall_hours:.2f} hours")
    print(f"Longest Session: {longest_session['subject']} - {longest_session['duration']} mins ({longest_session['topic']})")
    print(f"Weakest Area (Least Time): {weakest_subj} with {min_time} mins total")
    print("\nBreakdown Per Subject:")
    for subj in subject_map:
        hours_spent = subject_map[subj] / 60
        print(f" - {subj}: {hours_spent:.2f} hours ({subject_map[subj]} mins)")
    print("========================================")


def save_sessions():
    """
    Part (g): Saves files using simple text formatting lines.
    Saves each session field separated by a special divider symbol (||).
    """
    try:
        file = open(FILE_NAME, "w")
        for s in sessions:
            # Writing fields on a single line separated by a clear delimiter
            line = f"{s['subject']}||{s['topic']}||{s['date_label']}||{s['duration']}\n"
            file.write(line)
        file.close()
        print("Data successfully saved to study_log.txt.")
    except:
        print("Error: Could not save the data to the file.")


def load_sessions():
    """
    Part (g): Safely opens and parses data from study_log.txt if it exists.
    """
    # Check if file exists so the app doesn't crash on the first run
    if os.path.exists(FILE_NAME):
        try:
            file = open(FILE_NAME, "r")
            for line in file:
                # Strip out the newline character at the end
                clean_line = line.strip()
                if clean_line:
                    # Split the line back into individual parts using our delimiter
                    parts = clean_line.split("||")
                    # Re-build the dictionary maps from the file strings
                    session_dict = {
                        "subject": parts[0],
                        "topic": parts[1],
                        "date_label": parts[2],
                        "duration": int(parts[3]) # Convert back to a number
                    }
                    sessions.append(session_dict)
            file.close()
            print(f"Welcome back! Loaded {len(sessions)} previous study sessions.")
        except:
            print("Notice: Log file was unreadable or corrupt. Starting clean.")
    else:
        print("First time running the app! Created a brand new study log.")


def main():
    """
    Part (a): Main driver program loop with menu interface.
    """
    # Load old data before showing the menu
    load_sessions()
    
    while True:
        print("\n===== SMART STUDY PLANNER MAIN MENU =====")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            search_by_subject()
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Exiting application. Good luck with your studies!")
            break # Breaks out of the while loop completely to close the script
        else:
            # Rejecting invalid choices cleanly without crashing
            print("Invalid selection! Please enter a valid number from 1 to 5.")


# Standard execution block
if __name__ == "__main__":
    main()
