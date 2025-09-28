import threading
import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox
import customtkinter as ctk
import time
import database
import main

#The user form to take imputs
def submitForm():

    #Get the user inputs
    name = nameEntry.get()
    age = ageEntry.get()
    skill = skillScale.get()
    sessionNumber = sessionNumberEntry.get()
    sessionLength = sessionLengthEntry.get()
    sport = sportCombobox.get().strip().lower()

    #Check if feedback box is there
    if feedbackTextBox.winfo_ismapped():

        #get user feedback
        feedback = feedbackTextBox.get("1.0", tk.END).strip()
    else:

        #Set to ""
        feedback = ""

    #Validates the users inputs
    error, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation(name, age, skill, sessionNumber, sessionLength, sport, feedback)

    #If there are no erroes
    if error == "":

        #Once all checks complete change label to let user know its working on the plan
        statusLabel.configure(text="Processing...")

        #Disable the submit button while processing
        submitButton.configure(state="disabled")

        #Runs the algorithm on a new thread
        threading.Thread(target=runAlgorithm, args=(name, age, skill, sessionNumber, sessionLength, sport, feedback)).start()
        
    else:

        #Show user the error
        messagebox.showerror("Error", error)

        return

#Runs the algorithm
def runAlgorithm(name, age, skill, sessionNumber, sessionLength, sport, feedback):

    #Add user to the people table in the database
    database.insertPeopleData(name, age, skill, sessionNumber, sessionLength, sport)

    #Create the session split of stretches and exercises based on time
    stretchNumber, exerciseNumber, workoutPlan, totalNumber = main.sessionSplit(sessionNumber, sessionLength)

    #Saves start time
    startTime = time.perf_counter()

    #Choose which algorithm to use
    #bestPlan, bestFitness = main.geneticAlgorithm(workoutPlan, stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback)
    #bestPlan, bestFitness = main.simulatedAnnealing(stretchNumber, exerciseNumber, sport, totalNumber,skill, feedback, workoutPlan)
    bestPlan, bestFitness = main.antColonyOptimization(stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, sessionNumber)

    #Saves end time
    endTime = time.perf_counter()

    #Calculates time taken
    executionTime = endTime - startTime

    print(executionTime, bestPlan)

    #Update label to tell user the algorithm is complete
    statusLabel.configure(text="Complete!")

    #Update the GUI
    root.after(0, updateGUI, bestPlan)

#Updates the GUI once the algorithm has been run
def updateGUI(bestPlan):
    
    root.geometry("800x750")

    #Creates feedback box
    feedbackLabel.pack(pady=5)
    feedbackTextBox.pack(pady=10)
    resubmit.pack(pady=5)

    #Create result window for plan
    resultWindow = ctk.CTkToplevel(root)
    resultWindow.geometry("800x300")
    resultWindow.title("Results")

    ctk.CTkLabel(resultWindow, text="Workout", font=("Verdana", 25, "bold")).pack(pady=10)

    #Create a Treeview for showing the workout plan
    treeFrame = ctk.CTkFrame(resultWindow)
    treeFrame.pack(pady=10, fill="both", expand=True)
    tree = ttk.Treeview(treeFrame, show="headings", height=10)
    tree.pack(fill="both", expand=True)

    #treeFrame.pack(pady=10, fill="both", expand=True)

    #Change status label and re-enable submit button
    statusLabel.configure(text="Complete!")
    submitButton.configure(state="normal")

    #Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    #Find the max number of exercises per day
    maxExercises = max(len(exercises) for exercises in bestPlan.values())

    #Insert the headers into the treeview from the columns
    tree["columns"] = list(bestPlan.keys())

    #Goes through each column
    for col in tree["columns"]:

        #Sets headings as the day from the plan
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    #Goes through each day
    for i in range(maxExercises):

        #Create new list of exercises
        rowData = []

        #Goes through each exercise
        for exercises in bestPlan.values():

            #Adds exercise to the row
            rowData.append(exercises[i] if i < len(exercises) else "")
        
        #Adds rows to the treeview
        tree.insert("", "end", values=rowData)

#Saves sports from database under variable
sportsList = database.getSports()

#Create the main window

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()

root.geometry("800x600")

font.families()

ctk.CTkLabel(root, text="User Form", font=("Verdana", 25, "bold")).pack(pady=10)

#Create name label and input box
ctk.CTkLabel(root, text="What is your name?", font=("Verdana", 12, "bold")).pack(pady=1)
nameEntry = ctk.CTkEntry(root)
nameEntry.pack(pady=(0, 10))

#Create age label and input box
ctk.CTkLabel(root, text="How old are you?", font=("Verdana", 12, "bold")).pack(pady=1)
ageEntry = ctk.CTkEntry(root)
ageEntry.pack(pady=(0, 10))

#Create skill label and scale from 1-5
ctk.CTkLabel(root, text="Experience in the gym (1-5)", font=("Verdana", 12, "bold")).pack(pady=1)
skillScale = ctk.CTkSlider(root, from_=1, to=5, number_of_steps=4)
skillScale.pack(pady=(0, 10))

#Create session number label and input box
ctk.CTkLabel(root, text="How many sessions can you do each week?", font=("Verdana", 12, "bold")).pack(pady=1)
sessionNumberEntry = ctk.CTkEntry(root)
sessionNumberEntry.pack(pady=(0, 10))

#Create session length label and input box
ctk.CTkLabel(root, text="How long will these sessions be (in minutes)?", font=("Verdana", 12, "bold")).pack(pady=1)
sessionLengthEntry = ctk.CTkEntry(root)
sessionLengthEntry.pack(pady=(0, 10))

#Create sport label and combobox, taking from the sportsList variable
ctk.CTkLabel(root, text="What sport are you training for?", font=("Verdana", 12, "bold")).pack()
sportCombobox = ctk.CTkComboBox(root, values=sportsList)
sportCombobox.set("Select a sport")
sportCombobox.pack(pady=(0, 15))

#Create status label to let users know the status
statusLabel = ctk.CTkLabel(root, text="Click 'Submit' to begin", font=("Verdana", 12, "bold"))
statusLabel.pack(pady=(0, 10))

#Create submit button which starts the submitForm function
submitButton = ctk.CTkButton(root, text="Submit", font=("Verdana", 12, "bold"), command=submitForm)
submitButton.pack(pady=(0, 10))

feedbackLabel = ctk.CTkLabel(root, text="Workout Feedback box", font=("Verdana", 12, "bold"))

feedbackTextBox = ctk.CTkTextbox(root, height=100, width=500)

resubmit = ctk.CTkLabel(root, text="Click the submit button again to regenertate workout with feedback!", font=("Verdana", 12, "bold"))

#Run the Tkinter event loop
root.mainloop()
