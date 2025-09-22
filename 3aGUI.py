import tkinter as tk
from tkinter import filedialog as fd, messagebox
import random
from imu_win import open_imu_window
from motor_win import open_motor_window
from LC_win import open_lc_window


#class NSATApp:
    #def __init__(self, root):
        #self.root = root

# global variables
imuWindow = None
imuCanvas = None
motorWindow = None
motorCanvas = None
lcWindow = None
lcCanvas = None
staticWindow = None
staticCanvas = None
dynamicWindow = None
dynamicCanvas = None

# FIXME: idk if this is right (initialization of entry variables)
pull_accel_val = None
pull_decel_val = None
pull_rot_val = None
pull_speed_val = None

dark = True # start program in dark mode

FONTCOLOR = "#E0E0E0"
BUTTONCOLOR = "#444444"
WINDOWCOLOR = "#121212"

# initialize status rectangle colors as grey, will be changed immediately on startup based on connection status
imu_color = BUTTONCOLOR 
motor_color = BUTTONCOLOR
lc_color = BUTTONCOLOR

# declare dictionaries for storing element configs
rects = {} 
lines = {} 
texts = {}
buttons = {}
entries = {}
labels = {}
imuButtons = {}
imuLabels = {}
imuTexts = {}
motorButtons = {}
motorLabels = {}
lcButtons = {}
lcLabels = {}
lcTexts = {}


root = tk.Tk() # create root window
canvas = tk.Canvas(root, width = 1280, height = 720, bg = WINDOWCOLOR, highlightthickness = 0) # create canvas

#=============function definitions=============
def disable_close(): # disable closing with [x]
    messagebox.showinfo("Notice", "Please use the Exit button to close this window.")

def exitFunction(): # exit button's function
    # TODO Release all comm ports, send whatever is needed to each device to power down, close windows etc.
    root.destroy() 

def create_window(title, width, height):
    window = tk.Toplevel()
    window.title(f"{title}")
    window.geometry(f"{width}x{height}")
    window.resizable(width = False, height = False)
    window.configure(bg = WINDOWCOLOR)
    canvas = tk.Canvas(window,
        width = width, 
        height = height, 
        bg = WINDOWCOLOR, 
        highlightthickness = 3)
    canvas.pack()
            
    def disable_close():
        pass
    window.protocol("WM_DELETE_WINDOW", disable_close)

    return window, canvas

def create_button(parent, text, command, width = 10, height = 1, relief = "solid", 
                  bd = 1, bg = BUTTONCOLOR, activebackground = WINDOWCOLOR, 
                  activeforeground = FONTCOLOR, font = ("Courier", 14)):
    
    return tk.Button(
        parent,
        text = text,
        command = command,
        width = width,
        height = height,
        relief = relief,
        bd = bd,
        bg = bg,
        fg = FONTCOLOR,
        activebackground = activebackground,
        activeforeground =  activeforeground,
        font = font,
        cursor = "hand2"
    )

def create_radiobutton(parent, text, variable, value, width=10,
                       bg=WINDOWCOLOR, activebackground=WINDOWCOLOR,
                       activeforeground="white", fg=FONTCOLOR,
                       selectcolor=BUTTONCOLOR, font=("Courier", 14)):
    """
    Creates a styled Tkinter Radiobutton.
    """
    return tk.Radiobutton(
        parent,
        text=text,
        variable=variable,
        value=value,
        width=width,
        bg=bg,
        activebackground=activebackground,
        activeforeground=activeforeground,
        fg=fg,
        selectcolor=selectcolor,
        font=font,
        cursor="hand2"
    )

def create_entry(parent, textvar, width):
    return tk.Entry(
            master = parent, 
            textvariable = textvar, 
            width = width, 
            font = ("Courier", 14), 
            bg = BUTTONCOLOR, 
            fg = FONTCOLOR, 
            insertbackground = FONTCOLOR, 
            relief = "solid", 
            bd = 1
        )

def anticipated():
    global dynamicWindow
    global dynamicCanvas
    if (dynamicWindow is None or not dynamicWindow.winfo_exists()) and (staticWindow is None or not staticWindow.winfo_exists()): # if staticWindow / dynamicWindow aren't open 
            # configure window
            try:
                time_window = int(time_window_val.get())
                post_log = int(log_time_post_val.get())
            except ValueError: # TODO: need to catch for non-entered motor controls too
                messagebox.showerror("Error", "Enter integer values into both \n\"Time Window\" and \"Log Time Post\".")
                return
            
            dynamicWindow, dynamicCanvas = create_window("Dynamic Anticipated", 500, 500)

            texts["dynamic_header"] = dynamicCanvas.create_text(250, 70, text = "Pull In:", font = ("Courier", 30, "bold underline"), fill = FONTCOLOR)
            texts["dynamic_timer"] = dynamicCanvas.create_text(250, 250, font = ("Courier", 50, "bold"), fill = FONTCOLOR)
            texts["recording"] = dynamicCanvas.create_text(260, 330, text = "Recording...", font = ("Courier", 20, "bold"), fill = FONTCOLOR)
            
            def countdown():
                nonlocal time_window
                if time_window > 0 and dynamicWindow.winfo_exists(): 
                    dynamicCanvas.itemconfig(texts["dynamic_timer"], text = str(time_window))
                    time_window -= 1
                    dynamicWindow.after(1000, countdown)
                else: # after countdown
                    dynamicCanvas.itemconfig(texts["dynamic_header"], text = "Pull!")
                    post_log_time()

            def post_log_time():
                nonlocal post_log
                if post_log > 0 and dynamicWindow.winfo_exists(): 
                    dynamicCanvas.itemconfig(texts["dynamic_timer"], text = str(post_log))
                    post_log -= 1
                    dynamicWindow.after(1000, post_log_time)
                else: # after countdown
                    dynamicWindow.destroy()         

            countdown()

def unanticipated():
   global dynamicWindow
   global dynamicCanvas
   count_to_rand = 0 # start random pull counter at 0
   post_counter = 1 # start counting at 1 after random pull

   if (dynamicWindow is None or not dynamicWindow.winfo_exists()) and (staticWindow is None or not staticWindow.winfo_exists()): # if staticWindow / dynamicWindow aren't open 
            # configure window
            try:
                time_window = int(time_window_val.get())
                post_log = int(log_time_post_val.get())
                pre_log = int(log_time_pre_val.get())

            except ValueError: # TODO: need to catch for non-entered motor controls too
                messagebox.showerror("Error", "Enter integer values into \n\"Time Window\", \"Log Time Pre\", and \"Log Time Post\".")
                return
            
            if pre_log + post_log > time_window:
                messagebox.showerror("Error", "The sum of \"Log Time Post\" and \"Log Time Pre\" are greater than \"Time Window\".")
                return
            
            dynamicWindow, dynamicCanvas = create_window("Dynamic Unanticipated", 500, 500)

            rand_pulltime = random.randint(0, time_window)
            texts["dynamic_timer"] = dynamicCanvas.create_text(250, 250, font = ("Courier", 50, "bold"), fill = FONTCOLOR)
            texts["recording"] = dynamicCanvas.create_text(260, 350, text = "Recording...", font = ("Courier", 20, "bold"), fill = FONTCOLOR)
                
            def post_countup():
                nonlocal post_counter
                if post_counter <= post_log:
                    dynamicCanvas.itemconfig(texts["dynamic_timer"], text = post_counter)
                    post_counter += 1
                    dynamicWindow.after(1000, post_countup)  
                else:
                    dynamicWindow.destroy()

            def random_count():
                nonlocal count_to_rand
                
                if count_to_rand < rand_pulltime + pre_log:
                    dynamicCanvas.itemconfig(texts["dynamic_timer"], text = "Relax")
                    count_to_rand += 1
                    dynamicWindow.after(1000, random_count)
                else:
                    post_countup()
             
            random_count()

def darkLight(): # change visual mode
    global dark, FONTCOLOR, BUTTONCOLOR, WINDOWCOLOR

    dark = not dark # toggle boolean 
    
    if dark:  
        FONTCOLOR = "#E0E0E0"
        BUTTONCOLOR = "#444444"
        WINDOWCOLOR = "#121212"
        buttons["darkButton"].config(text = "⏾")
    else:
        FONTCOLOR = "black"
        BUTTONCOLOR = "#ffffff"
        WINDOWCOLOR = "#eeeeee"
        buttons["darkButton"].config(text = "☀")

    # update window and canvas
    root.configure(bg = WINDOWCOLOR)
    canvas.configure(bg = WINDOWCOLOR)

    # update IMU window's elements
    if imuWindow is not None and imuWindow.winfo_exists():

        imuWindow.configure(bg = WINDOWCOLOR)
        imuCanvas.configure(bg = WINDOWCOLOR)

        for button in imuButtons.values():
            button.config(bg = WINDOWCOLOR, activebackground = BUTTONCOLOR, fg = FONTCOLOR, activeforeground = FONTCOLOR)
            
        for label in imuLabels.values():
            label.config(fg = FONTCOLOR, bg = BUTTONCOLOR)

        for text in imuTexts.values():
            imuCanvas.itemconfig(text, fill = FONTCOLOR)

    # update motor window's elements
    if motorWindow is not None and motorWindow.winfo_exists():
        motorWindow.configure(bg = WINDOWCOLOR)
        motorCanvas.configure(bg = WINDOWCOLOR)

        for key, button in motorButtons.items():
            if key not in ("accel_entry", "decel_entry", "speed_entry", "rotation_entry"):
                button.config(bg = WINDOWCOLOR, activebackground = BUTTONCOLOR, fg = FONTCOLOR, activeforeground = FONTCOLOR)
            else:
                button.config(bg = WINDOWCOLOR, fg = FONTCOLOR, insertbackground = FONTCOLOR)

        for label in motorLabels.values():
            label.config(fg = FONTCOLOR, bg = BUTTONCOLOR)

        for text in motorTexts.values():
            motorCanvas.itemconfig(text, fill = FONTCOLOR)
    
    # update load cell window's elements
    if lcWindow is not None and lcWindow.winfo_exists():
        lcWindow.configure(bg = WINDOWCOLOR)
        lcCanvas.configure(bg = WINDOWCOLOR)

        for button in lcButtons.values():
            button.config(bg = WINDOWCOLOR, activebackground = BUTTONCOLOR, fg = FONTCOLOR, activeforeground = FONTCOLOR)
            
        for label in lcLabels.values():
            label.config(fg = FONTCOLOR, bg = BUTTONCOLOR)

        for text in lcTexts.values():
            lcCanvas.itemconfig(text, fill = FONTCOLOR)

    # update static window's elements
    if staticWindow is not None and staticWindow.winfo_exists():
        staticWindow.configure(bg = WINDOWCOLOR)
        staticCanvas.configure(bg = WINDOWCOLOR, highlightbackground = FONTCOLOR)
        staticCanvas.itemconfig(texts["static_timer"], fill = FONTCOLOR)
        staticCanvas.itemconfig(texts["timer_header"], fill = FONTCOLOR)
        try:
            staticCanvas.itemconfig(texts["recording"], fill = FONTCOLOR)
        except:
            pass

    # update rectangles
    for name, rect in rects.items(): 
        if name in ("imu", "motor", "lc"):
            continue # skip the status rectangles
        canvas.itemconfig(rect, fill = BUTTONCOLOR)

    # update texts
    for text in texts.values():
        canvas.itemconfig(text, fill = FONTCOLOR)

    # update buttons, reloadbutton, entries, and radiobuttons need separate updates
    for name, button in buttons.items():
        if name == "reloadButton": # reload button should have transparent background
            button.config(bg = WINDOWCOLOR, activebackground = WINDOWCOLOR, fg = FONTCOLOR, activeforeground = BUTTONCOLOR)
        elif name.endswith("_entry"):
            button.config(bg = BUTTONCOLOR, fg = FONTCOLOR, insertbackground = FONTCOLOR)
        elif name.startswith("static_") or name.startswith("dynamic_") or name in ("anticipated", "unanticipated"):
            button.config(bg = WINDOWCOLOR, activebackground = WINDOWCOLOR, activeforeground = FONTCOLOR, fg = FONTCOLOR, selectcolor = BUTTONCOLOR)
        else:
            button.config(bg = BUTTONCOLOR, fg = FONTCOLOR, activebackground = WINDOWCOLOR, activeforeground = FONTCOLOR)
    
    #update labels
    for label in labels.values():
            label.config(fg = FONTCOLOR, bg = BUTTONCOLOR)

    for line in lines.values():
        canvas.itemconfig(line, fill = FONTCOLOR)

def imu_status(): # imu connection confirmation TODO: implement
    return random.choice([True, False])
def motor_status():# motor connection confirmation TODO: implement
    return random.choice([True, False])
def lc_status():# load cell connection confirmation TODO: implement
    return random.choice([True, False])
 
def reloadConnections(): # update each rectangle's fill color depending on connection status
    imu_color = "green" if imu_status() else "red"
    motor_color = "green" if motor_status() else "red"
    lc_color = "green" if lc_status() else "red"

    canvas.itemconfig(rects["imu"], fill=imu_color)
    canvas.itemconfig(rects["motor"], fill=motor_color)
    canvas.itemconfig(rects["lc"], fill=lc_color)

def standaloneIMU(): # open IMU window
    global imuWindow, imuCanvas, imuExit, imuButtons, imuLabels, imuTexts
    if canvas.itemcget(rects["imu"], "fill") == "green":
        if (imuWindow is None or not imuWindow.winfo_exists()): # if imuWindow isn't open
            imuWindow, imuCanvas, imuButtons, imuLabels, imuTexts = open_imu_window(WINDOWCOLOR, BUTTONCOLOR, FONTCOLOR) # unpack + pass current color for its colors
        else:
            imuWindow.lift() 
    else:
        messagebox.showerror("IMU Error", "IMU not connected.")

    #TODO create IMU graph, make start button work, read IMU data correctly

def standaloneMotor():# open motor window
    global motorWindow, motorCanvas, motorButtons, motorTexts
    if canvas.itemcget(rects["motor"], "fill") == "green":
        if motorWindow is None or not motorWindow.winfo_exists(): 
            motorWindow, motorCanvas, motorButtons, motorTexts = open_motor_window(WINDOWCOLOR, BUTTONCOLOR, FONTCOLOR)
        else:
            motorWindow.lift() 
    else:
        messagebox.showerror("Motor Error", "Motor not connected.")
    #TODO direct control
    pass

def standalonelc(): # open load cell window
    global lcWindow, lcCanvas, lcButtons, lcLabels, lcTexts
    if canvas.itemcget(rects["lc"], "fill") == "green":
        if lcWindow is None or not lcWindow.winfo_exists(): 
            lcWindow, lcCanvas, lcButtons, lcLabels, lcTexts = open_lc_window(WINDOWCOLOR, BUTTONCOLOR, FONTCOLOR)
        else:
            lcWindow.lift() 
    else:
        messagebox.showerror("Load Cell Error", "Load cell not connected.")
    #TODO live readings
    pass

def chooseFolder(): # choose root folder
    folder_path = fd.askdirectory(title = "Select a Root Folder", initialdir = '/') # prompt user to choose folder, opens new window
    
    if not folder_path:
        return None
    
    # truncate path if too long
    if len(folder_path) <= 33: 
        truncated_path = folder_path  
    else:
        truncated_path = folder_path[:33] + "..." 

    if "path" not in texts: # if first time
        texts["path"] = canvas.create_text(790, 81, text = truncated_path, font = ("Courier", 11), fill = FONTCOLOR, anchor = "nw") # print truncated path
    else:
        canvas.itemconfig(texts["path"], text = truncated_path) # replace old text with new 

    return folder_path

def startStatic(): #TODO: implement data output
    global staticWindow
    global staticCanvas
    time_left_down = 5
    time_left_up = 1
    try:
        pulltime = int(pulltime_val.get())
    except ValueError:
        messagebox.showerror("Error", "Enter an integer value into \"Pull Time\".")
        return

    if ((staticWindow is None or not staticWindow.winfo_exists()) and (dynamicWindow is None or not dynamicWindow.winfo_exists())): # if staticWindow and dynamicWindow isn't open 
        staticWindow, staticCanvas = create_window("Static Test", 500, 500)

            # create text
        texts["static_header"] = staticCanvas.create_text(250, 70, text = "Starting in:", font = ("Courier", 30, "bold underline"), fill = FONTCOLOR)
        texts["static_timer"] = staticCanvas.create_text(250, 250, font = ("Courier", 50, "bold"), fill = FONTCOLOR)

        def countdown(): # countdown from 5, display amt. of time left on screen
            nonlocal time_left_down
            if time_left_down > 0 and staticWindow.winfo_exists(): 
                staticCanvas.itemconfig(texts["static_timer"], text = str(time_left_down))
                time_left_down -= 1
                staticWindow.after(1000, countdown)
            else: # after countdown
                staticCanvas.itemconfig(texts["static_header"], text = "Start Pull:")
                texts["recording"] = staticCanvas.create_text(257, 330, text = "Recording...", font = ("Courier", 20, "bold"), fill = FONTCOLOR)
                countup()

            def countup(): # count up to pulltime, close window
                    nonlocal time_left_up
                    if time_left_up <= pulltime:
                        staticCanvas.itemconfig(texts["static_timer"], text = time_left_up)
                        time_left_up += 1
                        staticWindow.after(1000, countup)
                    else: # after count up
                        staticWindow.destroy()
            countdown()

def startDynamic(): #TODO: implement data output
    if anticipation.get() == "anticipated":
        anticipated()
    if anticipation.get() == "unanticipated":
        unanticipated()

def canvasElements(): # define and place all canvas elements
    # lines
    lines[1] = canvas.create_line(10, 150, 1270, 150, fill = FONTCOLOR, width = 2)
    lines[2] = canvas.create_line(300, 10, 300, 140, fill = FONTCOLOR, width = 1)
    lines[3] = canvas.create_line(780, 10, 780, 140, fill = FONTCOLOR, width = 1)
    lines[4] = canvas.create_line(780, 160, 780, 325, fill = FONTCOLOR, width = 1) 
    lines[5] = canvas.create_line(10, 335, 1270, 335, fill = FONTCOLOR, width = 2)
    lines[6] = canvas.create_line(381, 400, 381, 465, fill = FONTCOLOR, width = 1)
    lines[7] = canvas.create_line(780, 345, 780, 710, fill = FONTCOLOR, width = 1)
    # connection info
    texts["connection_info"] = canvas.create_text(125, 24, text = "Component Status", font = ("Courier", 16, "underline"), fill = FONTCOLOR)
    texts["imu_status"] = canvas.create_text(88, 60, text = "IMU", font = ("Courier", 14), fill = FONTCOLOR) 
    rects["imu"] = canvas.create_rectangle(40, 53, 55, 68, fill = imu_color, outline = "black", width = 2) # imu_color = red/green depending on connection
    texts["motor_status"] = canvas.create_text(100, 90, text = "Motor", font = ("Courier", 14), fill = FONTCOLOR) 
    rects["motor"] = canvas.create_rectangle(40, 83, 55, 98, fill = motor_color, outline = "black", width = 2) # motor_color = red/green depending on connection
    texts["load_cell_status"] = canvas.create_text(122, 120, text = "Load Cell", font = ("Courier", 14), fill = FONTCOLOR) 
    rects["lc"] = canvas.create_rectangle(40, 113, 55, 128, fill = lc_color, outline = "black", width = 2) # lc_color = red/green depending on connection

    # standalone tests
    texts["component_testing"] = canvas.create_text(535, 24, text = "Component Testing", font = ("Courier", 16, "underline"), fill = FONTCOLOR)

    # choose directory
    texts["choose_directory"] = canvas.create_text(1010, 24, text = "Choose Directory", font = ("Courier", 16, "underline"), fill = FONTCOLOR)
    rects["path_rect"] = canvas.create_rectangle(795, 74, 1140, 103, fill = BUTTONCOLOR, width = 1)
    texts["folder_symbol"] = canvas.create_text(1126, 88, text = "📁", font = ("Courier", 16), fill = FONTCOLOR)

    # static assessment
    texts["static_assessment"] = canvas.create_text(20, 165, text = "Static Assessment", font = ("Courier", 16, "underline"), fill = FONTCOLOR, anchor = "nw")
    texts["pull_time"] = canvas.create_text(120, 232, text = "Pull time (sec):", font = ("Courier", 14), fill = FONTCOLOR)

    # static results
    texts["static_results"] = canvas.create_text(800, 165, text = "Static Results", font = ("Courier", 16, "underline"), fill = FONTCOLOR, anchor = "nw")
    texts["avg_force"] = canvas.create_text(883, 230, text = "Avg. Force (N):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["max_force"] = canvas.create_text(1130, 230, text = "Max Force (N):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["static_log_file"] = canvas.create_text(877, 280, text = "Log File Name:", font = ("Courier", 14), fill = FONTCOLOR)
    texts["static_folder_extension"] = canvas.create_text(1215, 281, text = ".csv", font = ("Courier", 11), fill = FONTCOLOR)
    labels["avg_force"] = tk.Label(root, textvariable = avg_force, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["avg_force"].place(x = 976, y = 218)
    labels["max_force"] = tk.Label(root, textvariable = max_force, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_force"].place(x = 1215, y = 218)

    # dynamic assessment
    texts["dynamic_assessment"] = canvas.create_text(136, 370, text = "Dynamic Assessment", font = ("Courier", 16, "underline"), fill = FONTCOLOR)
    texts["time_window"] = canvas.create_text(187, 520, text = "Time Window / Countdown (sec):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["log_time_pre"] = canvas.create_text(247, 560, text = "Log Time Pre (sec):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["log_time_post"] = canvas.create_text(242, 600, text = "Log Time Post (sec):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["pull_accel"] = canvas.create_text(570, 520, text = "Pull Accel. (m/sec^2):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["pull_decel"] = canvas.create_text(570, 560, text = "Pull Decel. (m/sec^2):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["pull_rot"] = canvas.create_text(604, 600, text = "Pull Rot. (deg):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["pull_speed"] = canvas.create_text(598, 640, text = "Pull Speed (RPM):", font = ("Courier", 14), fill = FONTCOLOR)

    # dynamic results
    texts["dynamic_results"] = canvas.create_text(896, 370, text = "Dynamic Results", font = ("Courier", 16, "underline"), fill = FONTCOLOR)
    texts["dynamic_log_file"] = canvas.create_text(877, 428, text = "Log File Name:", font = ("Courier", 14), fill = FONTCOLOR)
    texts["dynamic_folder_extension"] = canvas.create_text(1215, 428, text = ".csv", font = ("Courier", 11), fill = FONTCOLOR)
    texts["ang_disp"] = canvas.create_text(916, 520, text = "Max Ang. Disp. (deg):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["max_vel"] = canvas.create_text(938, 560, text = "Max Vel. (m/sec):", font = ("Courier", 14), fill = FONTCOLOR)
    texts["max_accel"] = canvas.create_text(916, 600, text = "Max Accel. (m/sec^2):", font = ("Courier", 14), fill = FONTCOLOR)
    texts['x'] = canvas.create_text(1077, 490, text = "X", font = ("Courier", 14,), fill = FONTCOLOR)
    texts['y'] = canvas.create_text(1151, 490, text = "Y", font = ("Courier", 14), fill = FONTCOLOR)
    texts['z'] = canvas.create_text(1227, 490, text = "Z", font = ("Courier", 14), fill = FONTCOLOR)

    labels["ang_disp_x"] = tk.Label(root, textvariable = ang_disp_x, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["ang_disp_x"].place(x = 1045, y = 507)
    labels["ang_disp_y"] = tk.Label(root, textvariable = ang_disp_y, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["ang_disp_y"].place(x = 1045, y = 547)
    labels["ang_disp_z"] = tk.Label(root, textvariable = ang_disp_z, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["ang_disp_z"].place(x = 1045, y = 587)
    labels["max_vel_x"] = tk.Label(root, textvariable = max_vel_x, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_vel_x"].place(x = 1120, y = 507)
    labels["max_vel_y"] = tk.Label(root, textvariable = max_vel_y, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_vel_y"].place(x = 1120, y = 547)
    labels["max_vel_z"] = tk.Label(root, textvariable = max_vel_z, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_vel_z"].place(x = 1120, y = 587)
    labels["max_accel_x"] = tk.Label(root, textvariable = max_accel_x, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_accel_x"].place(x = 1195, y = 507)
    labels["max_accel_y"] = tk.Label(root, textvariable = max_accel_y, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_accel_y"].place(x = 1195, y = 547)
    labels["max_accel_z"] = tk.Label(root, textvariable = max_accel_z, font = ("Courier", 14), fg = FONTCOLOR, bg = BUTTONCOLOR, bd = 1, relief = "solid", width = 5, height = 1)
    labels["max_accel_z"].place(x = 1195, y = 587)
    
 
def placeButtons(): # place all buttons
    buttons["reloadButton"].place(x = 260, y = 3)
    buttons["standaloneIMUbutton"].place(x = 325, y = 70)
    buttons["standaloneMotorButton"].place(x = 475, y = 70)
    buttons["standalonelcButton"].place(x = 625, y = 70)
    buttons["fileLocationButton"].place(x = 1150, y = 75)
    buttons["exitButton"].place(x = 1225, y = 8)
    buttons["pulltime_entry"].place(x = 215, y = 220)
    buttons["static_extension"].place(x = 310, y = 205)
    buttons["static_left_lateral"].place(x = 460, y = 205)
    buttons["static_flexion"].place(x = 300, y = 235)
    buttons["static_right_lateral"].place(x = 460, y = 235)
    buttons["start_static"].place(x = 30, y = 280)
    buttons["static_log_entry"].place(x = 966, y = 270)
    buttons["darkButton"].place(x = 1225, y = 675)
    buttons["anticipated"].place(x = 20, y = 400) 
    buttons["unanticipated"].place(x = 190, y = 400)
    buttons["dynamic_extension"].place(x = 400, y = 400)
    buttons["dynamic_left_lateral"].place(x = 560, y = 400)
    buttons["dynamic_flexion"].place(x = 390, y = 430)
    buttons["dynamic_right_lateral"].place(x = 560, y = 430)
    buttons["time_window_entry"].place(x = 370, y = 507)
    buttons["log_time_pre_entry"].place(x = 370, y = 547)
    buttons["log_time_post_entry"].place(x = 370, y = 587)
    buttons["pull_accel_entry"].place(x = 710, y = 507)
    buttons["pull_decel_entry"].place(x = 710, y = 547)
    buttons["pull_rot_entry"].place(x = 710, y = 587)
    buttons["pull_speed_entry"].place(x = 710, y = 627)
    buttons["start_dynamic"].place(x = 30, y = 660)
    buttons["dynamic_log_entry"].place(x = 966, y = 417)

def setupWindow(): # window setup information
    root.title("NSAT Prototype 3a")
    root.geometry("1280x720")
    root.resizable(width = False, height = False)
    root.configure(bg = WINDOWCOLOR)
    root.protocol("WM_DELETE_WINDOW", disable_close)

    canvas.pack() # pack canvas onto window

'''Here, the buttons are stored in dictionaries that contain their name and configurations. Afterwards, they are created by iterating 
through a for loop that, by using the type's respective function, unpacks the configs and creates the button. It also adds the created 
button to a separate dictionary (buttons) to allow for reconfig for the visual-switch.'''

button_configs = {
    "reloadButton": {"text": "↻", "command": reloadConnections, "width": 1, "height": 1, "relief": "flat", "bd": 0, "bg": WINDOWCOLOR, "activebackground": WINDOWCOLOR, "activeforeground": BUTTONCOLOR, "font": ("Times New Roman", 20)},
    "standaloneIMUbutton": {"text": "IMU", "command": standaloneIMU},
    "standaloneMotorButton": {"text": "Motor", "command": standaloneMotor},
    "standalonelcButton": {"text": "Load Cell", "command": standalonelc},
    "fileLocationButton": {"text": "Choose Folder", "command": chooseFolder, "width": 13, "font": ("Courier", 12)},
    "exitButton": {"text": "Exit", "command": exitFunction, "width": 5, "font": ("Courier", 10)},
    "start_static": {"text": "Start Static", "command": startStatic, "width": 14},
    "start_dynamic": {"text": "Start Dynamic", "command": startDynamic, "width": 14},
    "darkButton": {"text": "⏾", "command": darkLight, "width": 3, "font": ("Courier", 16)},
}

static_motor_direction = tk.StringVar(value = "extension") 
dynamic_motor_direction = tk.StringVar(value = "extension")
anticipation = tk.StringVar(value = "anticipated") 
pulltime_val = tk.StringVar() 
time_window_val = tk.StringVar()
log_time_pre_val = tk.StringVar()
log_time_post_val = tk.StringVar()
avg_force = tk.StringVar(value = '-') 
max_force = tk.StringVar(value = '-')

ang_disp_x = tk.StringVar(value = '-')
ang_disp_y = tk.StringVar(value = '-')
ang_disp_z = tk.StringVar(value = '-')
max_vel_x = tk.StringVar(value = '-')
max_vel_y = tk.StringVar(value = '-')
max_vel_z = tk.StringVar(value = '-')
max_accel_x = tk.StringVar(value = '-')
max_accel_y = tk.StringVar(value = '-')
max_accel_z = tk.StringVar(value = '-')

radio_configs = {
    "static_extension": {"text": "Extension", "variable": static_motor_direction, "value": "extension", "width": 8},
    "static_left_lateral": {"text": "Left Lateral", "variable": static_motor_direction, "value": "left_lateral", "width": 11},
    "static_flexion": {"text": "Flexion", "variable": static_motor_direction, "value": "flexion", "width": 8},
    "static_right_lateral": {"text": "Right Lateral", "variable": static_motor_direction, "value": "right_lateral", "width": 12},
    "dynamic_extension": {"text": "Extension", "variable": dynamic_motor_direction, "value": "extension", "width": 8},
    "dynamic_left_lateral": {"text": "Left Lateral", "variable": dynamic_motor_direction, "value": "left_lateral", "width": 11},
    "dynamic_flexion": {"text": "Flexion", "variable": dynamic_motor_direction, "value": "flexion", "width": 8},
    "dynamic_right_lateral": {"text": "Right Lateral", "variable": dynamic_motor_direction, "value": "right_lateral", "width": 12},
    "anticipated": {"text": "Anticipated", "variable": anticipation, "value": "anticipated", "width": 10},
    "unanticipated": {"text": "Unanticipated", "variable": anticipation, "value": "unanticipated", "width": 13},
}

entry_configs = {
    "pulltime_entry": {"textvar": pulltime_val, "width": 4},
    "time_window_entry": {"textvar": time_window_val, "width": 4},
    "log_time_pre_entry": {"textvar": log_time_pre_val, "width": 4},
    "log_time_post_entry": {"textvar": log_time_post_val, "width": 4},
    "pull_accel_entry": {"textvar": pull_accel_val, "width": 4},
    "pull_decel_entry": {"textvar": pull_decel_val, "width": 4},
    "pull_rot_entry": {"textvar": pull_rot_val, "width": 4},
    "pull_speed_entry": {"textvar": pull_speed_val, "width": 4},
}

for name, cfg in entry_configs.items():
    buttons[name] = create_entry(root, **cfg)

for name, cfg in button_configs.items():
    buttons[name] = create_button(root, **cfg)

for name, cfg in radio_configs.items():
    buttons[name] = create_radiobutton(root, **cfg)

def main():
    setupWindow()
    canvasElements()
    placeButtons()
    reloadConnections()
    root.mainloop()

if __name__ == "__main__":
    main()

