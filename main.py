import numpy as np
from kivy.app import App
from kivy.lang import Builder  # Import Builder class
from kivy.uix.boxlayout import BoxLayout
import time

#Builder.load_file('camera.kv')  # Load the external kv file
Builder.load_string(''' <CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture() ''')
class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        texture = camera.texture
        region = texture.get_region(0, 0, self.width, self.height)
        pixels = np.frombuffer(region.pixels, dtype=np.uint8)
        print("Captured")

class TestCamera(App):
    def build(self):
        return CameraClick()

if __name__ == '__main__':
    TestCamera().run()
