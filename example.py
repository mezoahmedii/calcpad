import tkinter as tk

def on_selection_changed(selection):
    # This function will be called when the selection in the dropdown menu is changed
    # You can add your desired code here to handle the selection change
    print(f"Selected: {selection}")

# Create the main window
main_window = tk.Tk()

# Create a list of options for the dropdown menu
options = ["Option 1", "Option 2", "Option 3"]

# Create a variable to store the selected option
selected_option = tk.StringVar(main_window)
selected_option.set(options[0])  # Set the initial selected option

# Create the dropdown menu
dropdown_menu = tk.OptionMenu(main_window, selected_option, *options, command=on_selection_changed)
dropdown_menu.pack()

# Start the Tkinter event loop
main_window.mainloop()