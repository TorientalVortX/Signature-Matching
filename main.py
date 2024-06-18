import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from signature import match

# Match Threshold percentage
THRESHOLD = 85

def browsefunc(ent):
    """Opens a file dialog to select an image file and inserts the selected file path into the given entry widget."""
    filename = askopenfilename(filetypes=[
        ("JPEG files", "*.jpeg"),
        ("PNG files", "*.png"),
        ("JPG files", "*.jpg"),
    ])
    ent.delete(0, tk.END)  # Clear the current content of the entry widget
    ent.insert(tk.END, filename)  # Insert the selected file path into the entry widget

def capture_image_from_cam_into_temp(sign=1):
    """
    Captures an image from the default camera and saves it to a temporary directory.
    The image is saved as 'test_img1.png' or 'test_img2.png' depending on the sign parameter.
    """
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:  # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # Create temp directory if it doesn't exist
            img_name = f"./temp/test_img{sign}.png"
            cv2.imwrite(filename=img_name, img=frame)  # Save the captured frame
            print(f"{img_name} written!")

    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    """
    Prompts the user to capture an image using the webcam.
    If the user agrees, captures the image and updates the entry widget with the image path.
    """
    filename = os.path.join(os.getcwd(), 'temp', f'test_img{sign}.png')
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit'
    )
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)  # Clear the entry widget
        ent.insert(tk.END, filename)  # Insert the image path into the entry widget
    return True

def checkSimilarity(window, path1, path2):
    """
    Compares two images using the match function.
    Displays a message box indicating whether the signatures match based on the THRESHOLD.
    """
    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match", f"Signatures are {result}% similar!")
    else:
        messagebox.showinfo("Success: Signatures Match", f"Signatures are {result}% similar!")
    return True

# Initialize the main application window
root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")

# UI elements for the first signature
uname_label = tk.Label(root, text="Compare Two Signatures:", font=10)
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Signature 1", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry, sign=1)
)
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry)
)
img1_browse_button.place(x=400, y=140)

# UI elements for the second signature
img2_message = tk.Label(root, text="Signature 2", font=10)
img2_message.place(x=10, y=250)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=150, y=240)

img2_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image2_path_entry, sign=2)
)
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry)
)
img2_browse_button.place(x=400, y=260)

# Button to compare the signatures
compare_button = tk.Button(
    root, text="Compare", font=10, command=lambda: checkSimilarity(
        window=root, path1=image1_path_entry.get(), path2=image2_path_entry.get()
    )
)
compare_button.place(x=200, y=320)

# Start the Tkinter event loop
root.mainloop()
