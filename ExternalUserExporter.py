import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
import re
from shutil import copyfile
from docx import Document
from docx.shared import Pt

global targDir
global targFile


def loadLogFile(event):
    # Select and Load file
    filepath = askopenfilename(
        filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    # Change the title of the window to reflect the file
    root.title(f"Export Info Tool - {filepath}")

    # Open the file and extract the appropriate data using regex
    with open(filepath, "r") as input_file:
        text = input_file.read()

        regex_1 = re.compile(r'Date and Time\s*=\s*(.+)')
        regex_2 = re.compile(r'Filename Prefix\s*=\s*(.+)')
        regex_3 = re.compile(r'Source Voltage\s*\(kV\)\s*=\s*(.+)')
        regex_4 = re.compile(r'Source Current\s*\(uA\)\s*=\s*(.+)')
        regex_5 = re.compile(r'Image Pixel Size\s*\(um\)\s*=\s*(.+)')
        regex_6 = re.compile(r'Filter\s*=\s*(.+)')
        regex_7 = re.compile(r'Exposure\s*\(ms\)\s*=\s*(.+)')
        regex_8 = re.compile(r'Rotation Step\s*\(deg\)=(.+)')
        regex_9 = re.compile(r'Frame Averaging\s*=\s*(.+)')
        regex_10 = re.compile(r'Random Movement\s*=\s*(.+)')
        regex_11 = re.compile(r'Use 360 Rotation\s*=\s*(.+)')

        result_1 = regex_1.search(text)
        result_2 = regex_2.search(text)
        result_3 = regex_3.search(text)
        result_4 = regex_4.search(text)
        result_5 = regex_5.search(text)
        result_6 = regex_6.search(text)
        result_7 = regex_7.search(text)
        result_8 = regex_8.search(text)
        result_9 = regex_9.search(text)
        result_10 = regex_10.search(text)
        result_11 = regex_11.search(text)

        # if DateTime:
        DateTime = result_1.group(1)
        Filename = result_2.groups(1)
        Voltage = result_3.groups(1)
        Current = result_4.groups(1)
        PixelSize = result_5.groups(1)
        Filter = result_6.group(1)
        Exposure = result_7.group(1)
        RotStep = result_8.group(1)
        FrameAvg = result_9.group(1)
        RandMov = result_10.group(1)
        Rot360 = result_11.group(1)

        # Clear all input fields for filling
        exp_date.delete(0, tk.END)
        exp_filename.delete(0, tk.END)
        exp_scannedby.delete(0, tk.END)
        exp_machine.delete(0, tk.END)
        exp_voltage.delete(0, tk.END)
        exp_current.delete(0, tk.END)
        exp_pixelsize.delete(0, tk.END)
        exp_filter.delete(0, tk.END)
        exp_exposure.delete(0, tk.END)
        exp_rotationstep.delete(0, tk.END)
        exp_frameaverage.delete(0, tk.END)
        exp_randmovement.delete(0, tk.END)
        exp_360moveY.deselect()
        exp_360moveN.deselect()
        exp_addcomment.delete("1.0", tk.END)

        # Insert appropriate data in input fields
        exp_date.insert(0, DateTime)
        exp_filename.insert(0, Filename)
        exp_scannedby.insert(0, "Kelsi Hurdle")
        exp_machine.insert(0, "Bruker Skyscan 1173")
        exp_voltage.insert(0, Voltage)
        exp_current.insert(0, Current)
        exp_pixelsize.insert(0, PixelSize)
        exp_filter.insert(0, Filter)
        exp_exposure.insert(0, Exposure)
        exp_rotationstep.insert(0, RotStep)
        exp_frameaverage.insert(0, FrameAvg)
        exp_randmovement.insert(0, RandMov)
        if Rot360.upper() == "YES":
            exp_360moveY.select()
        else:
            exp_360moveN.select()

    return


def selectDestination(event):
    global targDir
    targetDir = askdirectory()
    targDir = targetDir

    return


def loadTemplateFile(event):
    # Make a copy of reference doc
    global targDir
    global targFile
    filepath = askopenfilename(
        filetypes=[("Word Doc Files", "*.docx"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    outFile = (targDir + "/External_User_Info.docx")
    copyfile(filepath, outFile)
    targFile = outFile

    return


def publishLogFile(event):
    # Publish field information to new doc copy
    global targDir
    global targFile

    NewDate = exp_date.get()
    NewFile = exp_filename.get()
    NewScanned = exp_scannedby.get()
    NewMachine = exp_machine.get()
    NewVoltage = exp_voltage.get()
    NewCurrent = exp_current.get()
    NewPixel = exp_pixelsize.get()
    NewFilter = exp_filter.get()
    NewExposure = exp_exposure.get()
    NewRotation = exp_rotationstep.get()
    NewFrame = exp_frameaverage.get()
    NewRandMov = exp_randmovement.get()
    NewRot360 = rbVar.get()
    NewAddComment = exp_addcomment.get("1.0", tk.END)

    doc = Document(targFile)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    for run in doc.paragraphs:
        if "Date: " in run.text:
            run.text = run.text.replace("Date: ", "Date: " + NewDate)
            run.style = doc.styles['Normal']
        elif "File Name(s): " in run.text:
            run.text = run.text.replace("File Name(s): ", "File Name(s): " + NewFile)
            run.style = doc.styles['Normal']
        elif "Scanned by: " in run.text:
            run.text = run.text.replace("Scanned by: ", "Scanned by: " + NewScanned)
            run.style = doc.styles['Normal']
        elif "Machine: " in run.text:
            run.text = run.text.replace("Machine: ", "Machine: " + NewMachine)
            run.style = doc.styles['Normal']
        elif "Voltage (kV): " in run.text:
            run.text = run.text.replace("Voltage (kV): ", "Voltage (kV): " + NewVoltage)
            run.style = doc.styles['Normal']
        elif "Current (uA): " in run.text:
            run.text = run.text.replace("Current (uA): ", "Current (uA): " + NewCurrent)
            run.style = doc.styles['Normal']
        elif "Pixel Size (??m): " in run.text:
            run.text = run.text.replace("Pixel Size (??m): ", "Pixel Size (??m): " + NewPixel)
            run.style = doc.styles['Normal']
        elif "Filter: " in run.text:
            run.text = run.text.replace("Filter: ", "Filter: " + NewFilter)
            run.style = doc.styles['Normal']
        elif "Exposure (ms): " in run.text:
            run.text = run.text.replace("Exposure (ms): ", "Exposure (ms): " + NewExposure)
            run.style = doc.styles['Normal']
        elif "Rotation Step (deg): " in run.text:
            run.text = run.text.replace("Rotation Step (deg): ", "Rotation Step (deg): " + NewRotation)
            run.style = doc.styles['Normal']
        elif "Frame Averaging: " in run.text:
            run.text = run.text.replace("Frame Averaging: ", "Frame Averaging: " + NewFrame)
            run.style = doc.styles['Normal']
        elif "Random Movement: " in run.text:
            run.text = run.text.replace("Random Movement: ", "Random Movement: " + NewRandMov)
            run.style = doc.styles['Normal']
        elif "360?? Rotation?: " in run.text:
            run.text = run.text.replace("360?? Rotation?: ", "360?? Rotation?: " + NewRot360)
            run.style = doc.styles['Normal']
        elif "Additional Comments: " in run.text:
            run.text = run.text.replace("Additional Comments: ", "Additional Comments: " + NewAddComment)
            run.style = doc.styles['Normal']

    doc.save(targFile)


def resetFields(event):
    exp_date.delete(0, tk.END)
    exp_filename.delete(0, tk.END)
    exp_scannedby.delete(0, tk.END)
    exp_machine.delete(0, tk.END)
    exp_voltage.delete(0, tk.END)
    exp_current.delete(0, tk.END)
    exp_pixelsize.delete(0, tk.END)
    exp_filter.delete(0, tk.END)
    exp_exposure.delete(0, tk.END)
    exp_rotationstep.delete(0, tk.END)
    exp_frameaverage.delete(0, tk.END)
    exp_randmovement.delete(0, tk.END)
    exp_360moveY.select()
    exp_addcomment.delete("1.0", tk.END)


# Initialize the GUI Window
root = tk.Tk()
root.title("Export Info Tool")

# Add the Title of the Tool to the top of the window
frame_1 = tk.Frame(master=root, relief=tk.RIDGE, borderwidth=1)
exp_title = tk.Label(master=frame_1, text='External User Log Tool', relief=tk.SUNKEN, font="Helvetica 18 bold")
frame_1.grid(column=0, row=0, columnspan=6)
exp_title.grid(column=0, row=0, sticky='EW')

# Initialize the Load Button for loading log files for extraction
exp_loadbutton = tk.Button(text='Load Log File')
exp_loadbutton.grid(column=4, row=1)
exp_loadbutton.bind("<Button-1>", loadLogFile)

exp_templbutton = tk.Button(text='Select Template File')
exp_templbutton.grid(column=4, row=7, columnspan=2, sticky='N', pady=15)
exp_templbutton.bind("<Button-1>", loadTemplateFile)

# Initialize entry box for Date of Scan
exp_date_Label = tk.Label(text='Date: ')
exp_date_Label.grid(column=0, row=1, sticky='e')
exp_date = tk.Entry()
exp_date.grid(column=1, row=1, sticky='w')

# Initialize entry box for File Name of loaded file
exp_filename_Label = tk.Label(text='File Name(s): ')
exp_filename_Label.grid(column=2, row=1, sticky='e')
exp_filename = tk.Entry()
exp_filename.grid(column=3, row=1, columnspan=2, sticky='w')

# Initialize entry box for name of individual that did the scanning
exp_scannedby_Label = tk.Label(text='Scanned By: ')
exp_scannedby_Label.grid(column=0, row=2, sticky='e')
exp_scannedby = tk.Entry()
exp_scannedby.grid(column=1, row=2, sticky='w')

# Initialize entry box for name of machine used for scanning
exp_machine_Label = tk.Label(text='Machine: ')
exp_machine_Label.grid(column=2, row=2, sticky='e')
exp_machine = tk.Entry()
exp_machine.grid(column=3, row=2, sticky='w')

# Initialize entry box for voltage used on scan in kilovolts
exp_voltage_Label = tk.Label(text='Voltage (kV): ')
exp_voltage_Label.grid(column=0, row=3, sticky='e')
exp_voltage = tk.Entry()
exp_voltage.grid(column=1, row=3, sticky='w')

# Initialize entry box for current used on scan in microampere
exp_current_Label = tk.Label(text='Current (uA): ')
exp_current_Label.grid(column=2, row=3, sticky='e')
exp_current = tk.Entry()
exp_current.grid(column=3, row=3, sticky='w')

# Initialize entry box for pixel size of scan in micrometers
exp_pixelsize_Label = tk.Label(text='Pixel Size (\u03BCm')
exp_pixelsize_Label.grid(column=4, row=3, sticky='e')
exp_pixelsize = tk.Entry()
exp_pixelsize.grid(column=5, row=3, sticky='w')

# Initialize entry box for filter used on scan
exp_filter_Label = tk.Label(text='Filter: ')
exp_filter_Label.grid(column=0, row=4, sticky='e')
exp_filter = tk.Entry()
exp_filter.grid(column=1, row=4, sticky='w')

# Initialize entry box for exposure of scan in milliseconds
exp_exposure_Label = tk.Label(text='Exposure (ms): ')
exp_exposure_Label.grid(column=2, row=4, sticky='e')
exp_exposure = tk.Entry()
exp_exposure.grid(column=3, row=4, sticky='w')

# Initialize entry box for rotation step in degrees of scan
exp_rotationstep_Label = tk.Label(text='Rotation Step (deg): ')
exp_rotationstep_Label.grid(column=4, row=4, sticky='e')
exp_rotationstep = tk.Entry()
exp_rotationstep.grid(column=5, row=4, sticky='w')

# Initialize entry box for frame averaging used on scan
exp_frameaverage_Label = tk.Label(text='Frame Averaging: ')
exp_frameaverage_Label.grid(column=0, row=5, sticky='e')
exp_frameaverage = tk.Entry()
exp_frameaverage.grid(column=1, row=5, sticky='w')

# Initialize entry box for random movement in scan
exp_randmovement_Label = tk.Label(text='Random Movement: ')
exp_randmovement_Label.grid(column=2, row=5, sticky='e')
exp_randmovement = tk.Entry()
exp_randmovement.grid(column=3, row=5, sticky='w')

# Initialize radio buttons for indicating if there was or was not 360 degree rotation
exp_360move_Label = tk.Label(text='360\u00B0 Rotation?: ')
exp_360move_Label.grid(column=4, row=5, columnspan=2)
rbVar = tk.StringVar()
exp_360moveY = tk.Radiobutton(root, text='Yes', variable=rbVar, value='Yes')
exp_360moveY.grid(column=4, row=6, sticky='e')
exp_360moveN = tk.Radiobutton(root, text='No', variable=rbVar, value='No')
exp_360moveN.grid(column=5, row=6, sticky='w')
exp_360moveY.select()
exp_360moveN.deselect()

# Initialize text box for adding additional comments
exp_addcomment_Label = tk.Label(text='Additional Comments: ')
exp_addcomment_Label.grid(column=0, row=6, columnspan=2, sticky='w', padx=10)
exp_addcomment = tk.Text(height=10)
exp_addcomment.grid(column=0, row=7, columnspan=4, rowspan=2, padx=10, pady=(0, 10))

exp_frame2 = tk.Frame(master=root)

exp_targetbutton = tk.Button(master=root, text='Select Target Directory')
exp_targetbutton.grid(column=5, row=1, padx=10)
exp_targetbutton.bind("<Button-1>", selectDestination)

# Initialize Publish button for publishing final results to word doc
exp_pubbutton = tk.Button(master=exp_frame2, text='Publish')
exp_pubbutton.grid(column=0, row=0, pady=10)
exp_pubbutton.bind("<Button-1>", publishLogFile)

# Initialize Reset button for resetting all fields for future use
exp_resetbutton = tk.Button(master=exp_frame2, text='Reset')
exp_resetbutton.grid(column=0, row=1, pady=10)
exp_resetbutton.bind("<Button-1>", resetFields)

exp_frame2.grid(column=4, row=7, columnspan=2, rowspan=2)
root.resizable(width=False, height=False)

root.mainloop()
