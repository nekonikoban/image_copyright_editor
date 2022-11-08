# image_copyright_editor
This app is made to change metadata (specifically copyright info) on a bulk of images.

1. Drag and drop bulk images from a directory to a frame
2. Enter the new copyright tag in the input below
3. Click `Save`

The output will be saved in a newly created directory called `updated` with exact same copy of the images dragged to a program with new `copyright` tag.

Packages used
- `os` for directory reading & writing
- `tkinter` for easy GUI setup
- `tkinterDnD` for drag & drop functionality
- `exif` for image metadata reading & writing

TODO:
- Convert png to jpg if any while running the task since `copyright` is not existent in this image extension ( Pillow open / save )


NOTE: 
If you encounter problems with `pyinstaller` while building `tkinter`, try providing library path manually like so

`pyinstaller --onefile --noconfirm --onefile --windowed --add-data "C:/<paython_path>/tkinterDnD;tkinterDnD/" "<script.py>"`

depending on which lib you use it could be either `tkinterDnD` or `tkinterdnd2` which in this case is the former. 
