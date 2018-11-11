import cv2


class Element:
    def __init__(self, color, id, content):
        self.color = color
        self.id = id
        self.content = content

    def show_element(self):
        cv2.imshow(str(self.id), self.content)
