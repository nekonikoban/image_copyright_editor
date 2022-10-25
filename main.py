import os #READING / WRITING DIRS
import tkinter as tk
from tkinter import ttk #GUI
import tkinterDnD  #DRAG & DROP
from exif import Image #METADATA READER / WRITER

# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()  
root.title("Image EXIF (COPYRIGHT) Editor  __by AylinDesign®") #Trackbar title
root.iconbitmap("C:/favicon.ico") #Trackbar / Taskbar icon NOTE: copy to C root for it to work
root.geometry(f"{750}x{450}") #Frame with static width and height
root.resizable(False, False) #Frame unresizable by both width and height
root.attributes('-topmost', True) #Frame always on top

#Style NOTE: REMOVE THIS ONE. LOW PRIORITY, STYLING WITH `DnD` IS MEH
style = ttk.Style()
style.configure("BW.TLabel", foreground="white", background="transparent")

images_value = tk.StringVar()
images_value.set('Drag & Drop')

copyright_value = tk.StringVar() #HOLDER OF THE CURRENT COPYRIGHT TAG
copyright_value.set('')

#GLOBAL VARIABLES
images = [] #HOLDS DROPPED FILES PATHS
path = "" #ABSOLUTE COMMON PATH FOR DROPPED FILES

#DRAG & DROP EVENT, LIST ALL FILES PATHS ON THE TREEVIEW WHEN DRAGGED OVER
def drop(event):
    data = event.data.split(" ")
    images_value.set(data)  
    load_dragged_images(data)
    for image in data:
        tree.insert('', tk.END, values=image)

#DEFINING TREE AND ITS CULOMNS TO SHOW TEMPORARILY DRAGGED FILES
columns = ['PATH', 'NEW_TAG']
tree = ttk.Treeview(root, ondrop=drop, columns=columns, show='headings')
tree.heading('PATH', text='Image Path')
tree.heading('NEW_TAG', text="New Tag")

#NOTE: REMOVE `drag_command`.IS LOW PRIORITY, PROBABLY WONT EVER BE USED IN AN APP LIKE THIS
def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    #return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")
    return ""

#DEFINING WIDGETS USED IN THE FRAME
def widgets(): 
    # Without DnD hook you need to register the widget for every purpose,
    # and bind it to the function you want to call

    # With DnD hook you just pass the command to the proper argument,
    # and tkinterDnD will take care of the rest
    # NOTE: You need a ttk widget to use these arguments

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    #TAG INPUT
    name_label = ttk.Label(root, text = 'Tag Name', font=('calibre', 10, 'bold'))
    name_label.pack(fill="both", expand=True, padx=10, pady=1)
    name_entry = ttk.Entry(root,textvariable = copyright_value, font=('calibre', 15, 'normal'))
    name_entry.pack(fill="both", expand=True, padx=10, pady=10)

    #CHECKBOX
    #copyright_check = ttk.Checkbutton(root)
    #copyright_check.pack(fill="both", expand=True, padx=10, pady=1)

    # Button that will call the submit function
    sub_btn=ttk.Button(root,text = 'Save', command=submit)   
    sub_btn.pack(fill="both", expand=True, padx=10, pady=10)

def load_dragged_images(imgs): 
    folder_path = imgs[0]
    pth = folder_path[0: folder_path.rindex("/")]
    img_filename = imgs[0]
    #img_path = f'{folder_path}/{img_filename}'

    #for x in imgs:
        #print(x)

    global images
    images = imgs
    global path
    path = pth

#SAVE EDITED METADATA FILES TO A NEW DIRECTORY    
def submit():
    #If images list is empty, break
    if not images:
        return

    tmp_path = path + "/updated" #Define temporary path for newly crated images to be placed into

    if not os.path.isdir(tmp_path): #If the previous path does not exists, create one, otherwise run the loop
        os.makedirs(tmp_path)
        submit() #Now that new dir has been created we do recursion 
    else: 
        int_var = tk.IntVar() #Inti progress bar
        pb_instance = ttk.Progressbar(root, maximum=len(images) - 1, length=280)
        pb_instance['variable'] = int_var
        pb_instance.pack(fill="both", expand=True, padx=10, pady=20)
        progress = 0

        for image in images: #Loop throughout `images` list
            tmp_path = f'{image}'

            with open(tmp_path, 'rb') as img_file: #Get binary of the current file / image
                img = Image(img_file)
                img.copyright = copyright_value.get() #Set copyright value with `exif` class
        
            with open(f'{path}/updated{image[image.rindex("/") : len(image)]}', 'wb') as new_image_file: #When copyright is set, 
                                                                                                         #we place the current file into newly created dir
                new_image_file.write(img.get_file())

            int_var.set(progress) 
            progress += 1 #Increment progress

    images_value.set('')  
    copyright_value.set('') #Reset copyright input

    for img in images: #Populate Treeview `NEW_TAG` row
        tree.set('', 'NEW_TAG', value = copyright_value.get() if copyright_value.get() else "__EMPTY__")

#INITIALIZE WIDGETS
widgets()
#RUN `Tk`` LOOP
root.mainloop()

#NOTE: THE APP STOPS RESPONDING WHILE RUN ON AN DIFFERENT WINDOWS MACHINE
#POSSIBLE SOLUTION: 
# - Installing / Updating C++ Redistributable