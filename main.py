import time

import cv2
import numpy as np
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from datetime import datetime
class SmileDetector(App):
    is_detection_started = False  # Define the attribute here
    scdToWait = 2
    start = time.time()
    def build(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

        # OpenCV VideoCapture
        self.video_capture = cv2.VideoCapture(0)
        self.is_smile_detected = False

        # Kivy UI
        layout = BoxLayout(orientation='vertical')

        self.feed = KivyImage(size=(400, 300))  # Set size of the box
        layout.add_widget(self.feed)

        self.label = Label(text='Smile Detection', size_hint=(1, 0.5))
        layout.add_widget(self.label)

        self.label2 = Label(text=f'Timer value : 0 second', size_hint=(1, 0.5))
        layout.add_widget(self.label2)

        self.button = Button(text='Start Detection', size_hint=(1, 0.1))
        self.button.bind(on_press=self.start_detection)
        layout.add_widget(self.button)

        self.image_widget = KivyImage(size=(400, 300))  # Set size of the box
        layout.add_widget(self.image_widget)

        # Create a camera object
        #self.camera = Camera(play=True)

        # Add the camera widget and image widget to the layout
        #layout.add_widget(self.camera)

        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update every 1/30th of a second
        return layout

    def start_detection(self, instance):
        self.is_detection_started = True

    def update(self, dt):
        if self.is_detection_started:
            # Capture video frame by frame
            ret, frame = self.video_capture.read()

            # Convert the frame to a format suitable for Kivy
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # Update the image widget with the new frame
            self.feed.texture = texture

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            self.label2.text = f'Timer value : {int(time.time() - self.start)} second'


            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

                if len(smiles) > 0:
                    self.is_smile_detected = True
                    if time.time() - self.start > self.scdToWait:
                        print("timer finished")
                        current_datetime = datetime.now().strftime("Capture-%Y-%m-%d--%H-%M-%S.jpg")
                        cv2.imwrite(current_datetime, frame)
                        self.start = time.time()

                        # Convert the frame to a format suitable for Kivy
                        buf = cv2.flip(frame, 0).tostring()
                        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                        # Update the image widget with the new frame
                        self.image_widget.texture = texture
                else:
                    self.is_smile_detected = False
                    self.start = time.time()

            if self.is_smile_detected:
                self.label.text = "Smile Detected!"
            else:
                self.label.text = "No Smile Detected"
                self.start = time.time()


    def on_stop(self):
        # Release the capture once the app is closed
        self.video_capture.release()


if __name__ == '__main__':
    SmileDetector().run()
