import time

import cv2
import os
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from math import pi
from PIL import Image
import rembg
from io import BytesIO

last_picture = "caca"


# Function to remove background using rembg
def remove_background(image_path):
    with open(image_path, "rb") as f:
        input_image = f.read()
    output = rembg.remove(input_image)
    return output


# Function to add a new background
def add_background(image_with_alpha, background_image):
    with Image.open(BytesIO(image_with_alpha)) as img:
        with Image.open(background_image) as bg:
            # Resize background to match the size of the foreground image
            bg = bg.resize(img.size)
            # Composite images
            img = img.convert("RGBA")
            bg = bg.convert("RGBA")
            result = Image.alpha_composite(bg, img)
            return result


def choose_random_path(directory):
    # Get list of files and directories in the given directory
    files = os.listdir(directory)

    # Filter out directories from the list of files
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

    # Choose a random file from the list
    random_file = random.choice(files)

    # Return the full path of the chosen file
    return os.path.join(directory, random_file)


class SM(App):
    def build(self):
        self.screenmanager = ScreenManager()
        self.screen0 = Load(name='gougoucaca')
        self.screen1 = Detection(name='manger caca le caca c\'est délicieux')
        self.screen2 = ResultDisplay(name='echo caca')
        self.screen3 = Memories(name='echo ACAC')
        Window.size = (400, 640)
        self.screenmanager.add_widget(self.screen0)
        Clock.schedule_once(self.start_app, 5)
        return self.screenmanager

    def start_app(self, dt):
        self.screenmanager.remove_widget(self.screen0)
        self.screen1.active = True
        self.screenmanager.add_widget(self.screen1)

    def switch_screen(self, n):
        if n == 2:
            self.screenmanager.remove_widget(self.screen1)
            self.screen1.active = False
            self.screen2.load_image(last_picture)
            self.screenmanager.add_widget(self.screen2)
        elif n == 3:
            self.screenmanager.remove_widget(self.screen1)
            self.screen1.active = False
            self.screen3.imagesPath = []
            for imagePath in os.listdir("undossier/"):
                if (imagePath.endswith(".jpg")):
                    self.screen3.imagesPath.append(imagePath)
            self.screenmanager.add_widget(self.screen3)
        elif n == 4:
            self.screenmanager.remove_widget(self.screen3)
            self.screen1.is_smile_detected = False
            self.screen1.is_detection_started = False
            self.screen1.start = None
            self.screen1.last = time.time()
            self.screen1.start_loop()
            self.screen1.active = True
            self.screenmanager.add_widget(self.screen1)
        else:
            self.screenmanager.remove_widget(self.screen2)
            self.screen1.is_smile_detected = False
            self.screen1.is_detection_started = False
            self.screen1.start = None
            self.screen1.last = time.time()
            self.screen1.start_loop()
            self.screen1.active = True
            self.screenmanager.add_widget(self.screen1)


sm = SM()


class Load(Screen):
    def __init__(self, **kwargs):
        super(Load, self).__init__(**kwargs)
        layout = BoxLayout()
        image = KivyImage(source="smile.png")
        layout.add_widget(image)
        self.add_widget(layout)


class Memories(Screen):
    def __init__(self, **kwargs):
        super(Memories, self).__init__(**kwargs)
        layout = FloatLayout()
        self.imagesPath = []
        for imagePath in os.listdir("undossier/"):
            if (imagePath.endswith(".jpg")):
                self.imagesPath.append(imagePath)
        self.ttl = KivyImage(source="buttonPic/ttl.jpg", pos_hint={'center_x': 0.50, 'center_y': 0.9},
                             size_hint=(0.75, 0.75))
        self.inSublist = False
        self.backButton = Button(background_normal="buttonPic/rounded_button.png", size_hint=(0.20, 0.09),
                                 pos_hint={'center_x': 0.15, 'center_y': 0.08})
        self.magicButton = Button(background_normal="buttonPic/rmBG.png", background_down="buttonPic/rmBG.png",
                                  size_hint=(0.27, 0.15), pos_hint={'center_x': 0.85, 'center_y': 0.08})
        self.left_button = Button(background_normal="buttonPic/arrowL.png", background_down="buttonPic/arrowL.png",
                                  size_hint=(0.2, 0.12), pos_hint={'center_x': 0.1, 'center_y': 0.5})
        self.right_button = Button(background_normal="buttonPic/arrowR.png", background_down="buttonPic/arrowR.png",
                                   size_hint=(0.2, 0.12), pos_hint={'center_x': 0.9, 'center_y': 0.5})
        self.trash_button = Button(background_normal="buttonPic/trash.png", background_down="buttonPic/trash.png",
                                   size_hint=(0.150, 0.092), pos_hint={'center_x': 0.50, 'center_y': 0.20})
        self.left_button.bind(on_press=lambda instance: self.switch_img(-1))
        self.right_button.bind(on_press=lambda instance: self.switch_img(1))
        self.trash_button.bind(on_press=lambda instance: self.switch_img(2))
        self.magicButton.bind(on_press=lambda instance: self.chgBack())

        self.left_button.pos = (100, 100)
        self.right_button.pos = (100, 100)

        self.m = 0

        self.backButton.bind(on_press=lambda instance: sm.switch_screen(4))
        self.currentImage = KivyImage(source="undossier/" + self.imagesPath[self.m])

        layout.add_widget(self.currentImage)
        layout.add_widget(self.left_button)
        layout.add_widget(self.right_button)
        layout.add_widget(self.trash_button)
        layout.add_widget(self.backButton)
        layout.add_widget(self.magicButton)
        layout.add_widget(self.ttl)

        self.add_widget(layout)

    def switch_img(self, n):
        if n == 2:
            os.remove(self.currentImage.source)
            self.imagesPath.pop(self.m)
            n = 1
        for imagePath in os.listdir("undossier/"):
            if (imagePath.endswith(".jpg") and imagePath not in self.imagesPath):
                self.imagesPath.append(imagePath)
        self.m = (self.m + n) % len(self.imagesPath)

        self.currentImage.source = "undossier/" + self.imagesPath[self.m]

    def chgBack(self):
        imgO, imgB = self.imagesPath[self.m], datetime.now().strftime("Back-%Y-%m-%d--%H-%M-%S.jpg")
        input_image_path = "undossier/" + imgO
        output_image_path = "undossier/" + imgB
        self.imagesPath.append(imgB)
        choosenString = choose_random_path("backgrounds/")
        background_image_path = choosenString

        # Remove background
        removed_background_image = remove_background(input_image_path)
        # Add new background
        final_image = add_background(removed_background_image, background_image_path)
        # Save the final image
        final_image = final_image.convert("RGB")

        final_image.save(output_image_path)

        self.currentImage.source = output_image_path


class Detection(Screen):
    def __init__(self, **kwargs):
        super(Detection, self).__init__(**kwargs)

        self.active = False

        # Create a box layout for the camera screen
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.13, 0.13, 0.13, 1)  # Gray color
            rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        # Bind the size and pos properties to update the background rectangle
        self.layout.bind(size=lambda instance, value: setattr(rect, 'size', value))
        self.layout.bind(pos=lambda instance, value: setattr(rect, 'pos', value))

        self.size = (480, 640)
        self.label = Label(text="Smile to take a selfie", font_name='SF-Pro-Display-Medium', font_size='24sp')
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.2}

        # Create a camera widget
        self.feed = KivyImage(source=last_picture)
        self.layout.add_widget(self.feed)
        self.layout.add_widget(self.label)

        self.add_widget(self.layout)

        self.progress_bar = ProgressBar(max=100, size_hint=(0.6, 0.1))
        self.progress_bar.border_width = 2
        self.progress_bar.pos_hint = {'center_x': 0.5, 'center_y': 0.2}

        self.layout.add_widget(self.progress_bar)

        self.is_detection_started = False
        self.is_smile_detected = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

        self.memory_button = Button(background_normal='buttonPic/macron.png', size_hint=(None, None), size=(100, 100),
                                    pos_hint={'center_x': 0.85, 'center_y': 0.9})
        self.layout.add_widget(self.memory_button)
        self.memory_button.bind(on_press=lambda instance: sm.switch_screen(3))

        self.start = None
        self.last = time.time()

        self.video_capture = cv2.VideoCapture(0)
        self.start_loop()

    def start_loop(self):
        Clock.schedule_interval(self.TakePic, 1.0 / 30.0)
        Clock.schedule_interval(self.bar_loop, 1.0 / 60.0)

    def bar_loop(self, dt):
        self.layout.canvas.after.clear()
        if self.is_smile_detected:
            with self.layout.canvas.after:
                self.label.opacity = 0
                self.progress_bar.opacity = 1
                self.progress_bar.value = (time.time() - self.start) * 50
        else:
            self.label.opacity = 1
            self.progress_bar.opacity = 0

    def TakePic(self, dt):
        global last_picture
        ret, frame = self.video_capture.read()
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.feed.texture = texture

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cropped_gray = gray[y:y + h, x:x + w]
            smiles = self.smile_cascade.detectMultiScale(cropped_gray, 1.8, 20)

            if len(smiles) > 0 and self.active:
                if not self.start:
                    self.start = time.time()
                self.is_smile_detected = True
                self.last = time.time()
                if time.time() - self.start > 2:
                    current_datetime = datetime.now().strftime("undossier/Capture-%Y-%m-%d--%H-%M-%S.jpg")
                    last_picture = current_datetime
                    cv2.imwrite(current_datetime, frame)
                    Clock.unschedule(self.TakePic)
                    Clock.unschedule(self.bar_loop)
                    sm.switch_screen(2)
            elif time.time() - self.last > 0.5 or not self.active:
                self.is_smile_detected = False
                self.start = time.time()
        if len(faces) == 0 and time.time() - self.last > 0.5:
            self.is_smile_detected = False
            self.start = time.time()


class ResultDisplay(Screen):
    def __init__(self, **kwargs):
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.13, 0.13, 0.13, 1)  # Gray color
            rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        # Bind the size and pos properties to update the background rectangle
        self.layout.bind(size=lambda instance, value: setattr(rect, 'size', value))
        self.layout.bind(pos=lambda instance, value: setattr(rect, 'pos', value))
        super(ResultDisplay, self).__init__(**kwargs)

        self.size = (480, 640)

        self.label = Label(text='Capture saved', font_name='SF-Pro-Display-Medium', size_hint=(1, 0.5),
                           font_size='24sp', bold=True)
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.4}

        img = KivyImage(source='buttonPic/rounded_button.png', size_hint=(3, 3))
        img.size[0] *= 2
        img.size[1] *= 2
        img.pos = (10 + 240 - img.size[1] / 2, 50)
        self.image = KivyImage(source=last_picture, size_hint=(1, 1.53))

        # Create a Button and set its background to the Image
        self.button = Button(background_normal='', background_down='', background_color=(0, 0, 0, 0))
        self.button.pos = (100, 100)
        self.button.add_widget(img)

        self.button.bind(on_press=lambda instance: sm.switch_screen(1))
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def load_image(self, last_picture):
        image = cv2.imread(last_picture)

        image = cv2.flip(image, 0)

        # Convert the image to texture
        texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        texture.blit_buffer(image.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

        self.image.texture = texture


class SmileDetector(App):
    is_detection_started = False
    is_smile_detected = False
    scdToWait = 2
    last = time.time()
    start = time.time()

    def build(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.feed = KivyImage(size=(400, 300))
        layout.add_widget(self.feed)

        self.label = Label(text='Smile Detection', size_hint=(1, 0.2), font_size='24sp', bold=True)
        layout.add_widget(self.label)

        self.label2 = Label(text='Timer value: 0 second', size_hint=(1, 0.2), font_size='18sp')
        layout.add_widget(self.label2)

        self.button = Button(text='Start Detection', size_hint=(1, 0.1), font_size='18sp')
        self.button.bind(on_press=self.start_detection)
        layout.add_widget(self.button)

        self.image_widget = KivyImage(size=(400, 300))
        layout.add_widget(self.image_widget)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def start_detection(self, instance):
        if (self.is_detection_started):
            self.is_detection_started = False
            self.button.text = 'Start Detection'
        else:
            self.is_detection_started = True
            self.button.text = 'Stop Detection'
            # self.start = time.time()
            self.video_capture = cv2.VideoCapture(0)  # Initialize video capture here

    def update(self, dt):
        if self.is_detection_started:
            ret, frame = self.video_capture.read()

            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.feed.texture = texture

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            self.label2.text = f'Timer value: {int(time.time() - self.start)} second'

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

                if len(smiles) > 0:
                    self.is_smile_detected = True
                    self.last = time.time()
                    if time.time() - self.start > self.scdToWait:
                        current_datetime = datetime.now().strftime("Capture-%Y-%m-%d--%H-%M-%S.jpg")
                        cv2.imwrite(current_datetime, frame)
                        self.start = time.time()

                        buf = cv2.flip(frame, 0).tobytes()
                        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                        self.image_widget.texture = texture
                elif time.time() - self.last > 0.5:
                    self.is_smile_detected = False
                    self.start = time.time()

            if self.is_smile_detected:
                self.label.text = "Smile Detected!"

            else:
                self.label.text = "No Smile Detected"
                self.start = time.time()

    def on_stop(self):
        self.video_capture.release()


if __name__ == '__main__':
    # SmileDetector().run()
    sm.run()
