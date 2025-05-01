from ultralytics import YOLO
import os
import shutil
import platform

# Load trained model
model = YOLO('./runs/detect/train6/weights/best.pt')

# Output folder for detected images
output_folder = './images/detected_deathstars'
os.makedirs(output_folder, exist_ok=True)

# Confidence threshold
CONF_THRESHOLD = 0.25

# Get mounted USB directories
def find_usb_mounts():
    system = platform.system()
    usb_mounts = []

    if system == 'Linux':
        base_path = '/media'
        if os.path.exists(base_path):
            for user_folder in os.listdir(base_path):
                user_path = os.path.join(base_path, user_folder)
                if os.path.isdir(user_path):
                    for mount in os.listdir(user_path):
                        mount_path = os.path.join(user_path, mount)
                        if os.path.isdir(mount_path):
                            usb_mounts.append(mount_path)

    elif system == 'Darwin':  # macOS
        base_path = '/Volumes'
        for volume in os.listdir(base_path):
            mount_path = os.path.join(base_path, volume)
            if os.path.isdir(mount_path):
                usb_mounts.append(mount_path)

    else:
        print("[!] USB detection not supported on this OS.")
    
    return usb_mounts

# Recursively find image files in a directory
def find_images_in_dir(root_dir):
    image_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(os.path.join(dirpath, file))
    return image_files

# Main detection logic
usb_dirs = find_usb_mounts()
if not usb_dirs:
    print("[!] No USB drives found.")
else:
    for usb_dir in usb_dirs:
        image_files = find_images_in_dir(usb_dir)
        if not image_files:
            print(f"[-] No images found in {usb_dir}")
            continue

        for img_path in image_files:
            results = model(img_path)
            detections = results[0].boxes

            if detections is not None and any(conf.item() > CONF_THRESHOLD for conf in detections.conf):
                print(f"[+] Death Star detected in: {img_path}")

                folder_tag = os.path.basename(os.path.dirname(img_path)).replace(" ", "_")
                filename = os.path.basename(img_path)
                output_path = os.path.join(output_folder, f"{folder_tag}_{filename}")
                shutil.copy(img_path, output_path)
            else:
                print(f"[-] No Death Star in: {img_path}")