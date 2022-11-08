import os #READING / WRITING DIRS
import tkinter as tk
from tkinter import ttk
import tkinterDnD  #DRAG & DROP
from exif import Image #METADATA READER / WRITER
#rom PIL import Image as pillowImage

MAIN_COLOR = "#2D2D2D"
EXTERNAL_PATH = "/updated"
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ttif']

#NOTE: Every file dependency is store on a system root dir

# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()  
root.title("Image COPYRIGHT Editor  __by AylinDesign®") #Trackbar title
root.iconbitmap("C:/favicon.ico") #Trackbar / Taskbar icon NOTE: copy to C root for it to work
root.geometry(f"{750}x{450}") #Frame with static width and height
root.resizable(False, False) #Frame unresizable by both width and height
root.attributes('-topmost', True) #Frame always on top
root.configure(background=MAIN_COLOR, border=2)

#fonts = Font(file="C:/NovaCut.ttf", size=12)
fonts = ('Helvetica', 12, 'bold')

#Style NOTE: REMOVE THIS ONE. LOW PRIORITY, STYLING WITH `DnD` IS MEEH..
tree_style = ttk.Style()
tree_style.configure("BW.TLabel", background="#383838", font=fonts)

button_style = ttk.Style()
button_style.configure("BW.TButton", background="#383838", font=fonts)

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
    images = filter_images(data)
    load_dragged_images(images)
    images_value.set(images)  
    for image in images:
        tree.insert('', tk.END, values=image)

#DEFINING TREE AND ITS CULOMNS TO SHOW TEMPORARILY DRAGGED FILES
columns = ['PATH', 'SIZE']
tree = ttk.Treeview(root, ondrop=drop, columns=columns, show='headings')
tree.heading('PATH', text='Putanja')
tree.column("PATH", minwidth=200, width=250)
tree.heading('SIZE', text="Veličina")
tree.column("SIZE", minwidth=0, width=5)

#NOTE: REMOVE `drag_command`.IS LOW PRIORITY, PROBABLY WONT EVER BE USED IN AN APP LIKE THIS
def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    #return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")
    return ""

#DEFINING WIDGETS USED IN THE FRAME
def widgets(): 
    #MENU
    #menubar = tk.Menu(root)
    #root.config(menu=menubar)

    # add the File menu to the menubar
    #menubar.add_cascade(
    #    label="About",
    #)

    # Without DnD hook you need to register the widget for every purpose,
    # and bind it to the function you want to call

    # With DnD hook you just pass the command to the proper argument,
    # and tkinterDnD will take care of the rest
    # NOTE: You need a ttk widget to use these arguments
    
    #TREE LABEL
    label_tree = ttk.Label(root, text='Prevuci slike u polje ispod',  background=MAIN_COLOR, foreground="white", font=fonts)
    label_tree.pack(fill="both", expand=True, padx=10, pady=1)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    #TAG INPUT
    label_input = ttk.Label(root, text = 'Unesi novi tag', background=MAIN_COLOR, foreground="white", font=fonts)
    label_input.pack(fill="both", expand=True, padx=10, pady=1)
    name_entry = ttk.Entry(root,textvariable = copyright_value, background=MAIN_COLOR, style="BW.TLabel", justify='center', font=fonts)
    name_entry.pack(fill="both", expand=True, padx=10, pady=10)

    #CHECKBOX
    #copyright_check = ttk.Checkbutton(root)
    #copyright_check.pack(fill="both", expand=True, padx=10, pady=1)

    # Button that will call the submit function
    sub_btn=ttk.Button(root, text = 'SPASI', command=submit, style="BW.TButton", default="active")   
    sub_btn.pack(fill="both", expand=True, padx=10, pady=10)

def filter_images(data):
    image_files = []
    for file in data: #C:/Users/Administrator/Desktop/nove_slike/15.jpeg
            for index in range(len(EXTENSIONS) - 1):     
                try:
                    if(file[file.rindex("."):len(file)].__eq__(EXTENSIONS[index])): #.jpeg == jpg, jpeg, png?
                        image_files.append(file)
                except ValueError:
                    print(file + ' ==> is not an image')           
    return image_files

def load_dragged_images(imgs): 
    folder_path = imgs[0]
    pth = folder_path[0: folder_path.rindex("/")]

    global images
    images = imgs
    global path
    path = pth

def convert_to_jpg(path):
    return
    #Open original image (png)
    #image = pillowImage.open(path)
    #Save converted image  
    #image.save(path[ 0 : path.rindex(".") ] + ".jpg")
    #Edit copyright and save to `updated` dir

#SAVE EDITED METADATA FILES TO A NEW DIRECTORY    
def submit():
    #If images list is empty, break
    if not images:
        return

    current_path = path + "/updated" #Define temporary path for newly crated images to be placed into

    if not os.path.isdir(current_path): #If the previous path does not exists, create one, otherwise run the loop
        os.makedirs(current_path)
        submit() #Now that new dir has been created we do recursion 
    else: 
        int_var = tk.IntVar() #Inti progress bar
        pb_instance = ttk.Progressbar(root, maximum=len(images) - 1, length=280)
        pb_instance['variable'] = int_var
        pb_instance.pack(fill="both", expand=True, padx=10, pady=20)
        progress = 0

        for image in images: #Loop throughout `images` list
            current_path = f'{image}'

            with open(current_path, 'rb') as img_file: #Get binary of the current file / image

                img = Image(img_file)
                #TODO: If image doesnt have exif convert it (_has_exif returns false always on both jpg and png)
                if not img._has_exif:
                    print("File has no exif")
                    #convert_image_to_jpg(current_path)

                img.copyright = copyright_value.get() #Set copyright value 
        
            with open(f'{path}/{EXTERNAL_PATH}{image[image.rindex("/") : len(image)]}', 'wb') as new_image_file: #When copyright is set, 
                                                                                                         #we place the current file into newly created dir
                new_image_file.write(img.get_file())

            int_var.set(progress) 
            progress += 1 #Increment progress
            pb_instance.destroy()

    images_value.set('') 
    copyright_value.set('') #Reset copyright input

    tree.delete(*tree.get_children()) #Reset tree data

    show_message_on_finish()

    for img in images: #Populate Treeview `SIZE` row
        tree.set('', 'SIZE', value = copyright_value.get() if copyright_value.get() else "__EMPTY__")

#SHOW MESSAGE ON FINISH
def show_message_on_finish():
    print("Task finished succesfuly!")

#INITIALIZE WIDGETS AND RUN
widgets()
root.mainloop()
