import threading
import time
from datetime import datetime
import os
import ffmpeg
import shutil

class ScreenshotThread(threading.Thread):
    def __init__(self, driver, video_folder):
        threading.Thread.__init__(self)
        self.driver = driver
        self.stop_event = threading.Event()
        self.video_folder = video_folder

    def run(self):
        while not self.stop_event.is_set():
            timestamp = str(datetime.now()).replace(" ", "_").replace(":", "_")
            self.driver.save_screenshot(f"{self.video_folder}/{timestamp}.png")
            time.sleep(0.05)

    def stop(self):
        self.stop_event.set()



    # def create_video_from_pngs(self, png_folder, output_file):
    #     # Get a list of PNG files in the folder
    #     png_files = [file for file in os.listdir(png_folder) if file.endswith('.png')]
        
    #     # Sort the files in ascending order based on their names
    #     png_files.sort()
        
    #     # Set up the FFmpeg input
    #     input_args = []
    #     for png_file in png_files:
    #         input_args.extend(['-i', os.path.join(png_folder, png_file)])
        
    #     # Set the output file path
    #     # output_path = os.path.join(png_folder, output_file)
        
    #     # Define the FFmpeg command
    #     ffmpeg.input(*input_args).output(output_file).run()

    def create_video_from_pngs(self, png_folder, output_file):
        # Get a list of PNG files in the folder
        png_files = [file for file in os.listdir(png_folder) if file.endswith('.png')]

        # Sort the files in ascending order based on their names
        png_files.sort()

        # Set up the FFmpeg input file list
        input_file_list = os.path.join(png_folder, 'input.txt')
        with open(input_file_list, 'w') as f:
            for i, png_file in enumerate(png_files):
                file_path = os.path.join(png_folder, png_file)
                f.write(f"file '{file_path}'\nduration 0.1\n")
        
        # Set the output file path
        # output_path = os.path.join(png_folder, output_file)
        
        # Define the FFmpeg command
        print(input_file_list)
        ffmpeg.input(input_file_list, format='concat', safe=0).output(
            output_file,
            pix_fmt='yuv420p',  # Set pixel format to yuv420p
            r=10,  # Set framerate to 10 frames per second (adjust as needed)
            start_number=0  # Set the start number of the input files
        ).run()
        
        # Remove the input file list
        os.remove(input_file_list)

        shutil.rmtree(png_folder)

# # Usage example
# create_video_from_pngs('/path/to/png/folder', 'output.mp4')
