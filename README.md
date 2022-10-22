# image_copyright_editor
This app is made specificaly to change metadata (copyright info) on a bulk of images.

1. Drag and drop bulk images from a directory to a frame
2. Enter the new copyright tag in the input below
3. Click `Save`

The output will be save in a newly created directory called `updated` with exact same copy of the images dragged to a program.

Packages used
- `os` for directory reading & writing
- `tkinter` for easy GUI setup
- `tkinterDnD` for drag & drop functionality
- `exif` for image metadata reading & writing

TODO:
1. Restrict files to images only
2. Show updated images on the frame
3. Reduce unnecessary imports
