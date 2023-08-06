# Pop-ups to get input from the user - tkinter 

## pip install tkinteruserinput

### Tested against Windows 10 / Python 3.10 / Anaconda 




```python

from tkinteruserinput import get_user_input, get_user_input_varbuttons, get_user_input_checkbox, get_user_input_radio, \
    show_info, show_error, show_warning

if __name__ == '__main__':
    ################################################

    user_input = get_user_input(
        linesinputbox=1,
        size="300x150",
        title="Input Box Example",
        textabovebox="Enter your text below:",
        submitbutton="Submit",
        regexcheck=r"\d+",
        showerror=("Error", "This is not a number! Try again!"),
        showinfo=None,
        showwarning=None,
        icon=r"C:\Users\hansc\Pictures\regiondf.ico",
    )
    print("User input:", user_input)

    ################################################

    options = ["Option 1", "Option 2", "Option 3"]
    user_input = get_user_input_varbuttons(
        options=options,
        size="300x350",
        title="Your input",
        textabovebox="Click a button",
        buttonwidth=15,
        buttonheight=3,
        icon=r"C:\Users\hansc\Pictures\regiondf.ico"

    )
    print("User input:", user_input)
    ################################################

    user_input = get_user_input_checkbox(
        checkbox_options=("Option 1", "Option 2", "Option 3", "Option 4"),
        size="300x350",
        title="Your input",
        textabovebox="Select checkboxes:",
        submitbutton="Submit",
        icon=r"C:\Users\hansc\Pictures\regiondf.ico"

    )
    print("User input:", user_input)
    ################################################
    user_input = get_user_input_radio(
        radio_options=("Option 1", "Option 2", "Option 3", "Option 4"),
        indexdefault=0,
        size="300x350",
        title="Your input",
        textabovebox="Select a radio button",
        submitbutton="Submit",
        icon=r"C:\Users\hansc\Pictures\regiondf.ico"
    )
    print("User input:", user_input)
    ################################################
    show_info("Titel", "Message")
    show_error("Titel", "Message")
    show_warning("Titel", "Message")



```
![](https://github.com/hansalemaos/screenshots/blob/main/tkinteruserinput/textinput1.png?raw=true)


![](https://github.com/hansalemaos/screenshots/blob/main/tkinteruserinput/textinput2.png?raw=true)


![](https://github.com/hansalemaos/screenshots/blob/main/tkinteruserinput/checkboxes.png?raw=true)


![](https://github.com/hansalemaos/screenshots/blob/main/tkinteruserinput/clickabutton.png?raw=true)


![](https://github.com/hansalemaos/screenshots/blob/main/tkinteruserinput/radiobutton.png?raw=true)
