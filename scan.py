import tkinter as tk
import cv2 as cv
import pyttsx3
import pytesseract
import pathlib
pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Program Files\Tesseract-OCR\\tesseract.exe'
)
class Scanner():
    def __init__(self, bookname):
        self.bookname = bookname
        self.page_no = 1
    def open_camera(self,speaker):
        speaker.say("Opening camera.")
        speaker.run()
        recognize_flag = False
        cap = cv.VideoCapture(1)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        speaker.say("Camera open sucessful.")
        speaker.run()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                speaker.say("Camera Error. Going back to main menu. Please check your camera's connection.")
                speaker.run()
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Display the resulting frame
            frame = cv.flip(frame, -1)
            
            cv.imshow('Camera', frame)
            if cv.waitKey(1) == ord('c'):
                speaker.say("Taking Photo.")
                speaker.run()
                cv.imshow('img1',frame) #display the captured image
                img_url = rf'img/{self.bookname}{self.page_no}.png'
                #Test
                img_url = rf'img/sample1.png'
                cv.imwrite(img_url,frame)
                speaker.say("Photo saved.")
                speaker.run()
                recognize_flag = True
                break
            elif cv.waitKey(1) == ord('q'):
                speaker.say("Going back to main menu.")
                speaker.run()
                cap.release()
                cv.destroyAllWindows()
                return None
        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()
        #Test
        img_url = rf'img/test1.png'
        frame = cv.imread(img_url)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        crop = gray [0:1080,420:1500]
        cv.imshow("Scanned Image",gray)
        cv.waitKey(1000) 
        cv.destroyAllWindows()
        text = pytesseract.image_to_string(crop, lang='eng', config='--psm 3')
        print(text)
        cv.imshow("Scanned Image",crop)
        speaker.say("Press r to read. Press s to scan the next page. Press q to quit.")
        while(True):    
            speaker.run()
            if cv.waitKey(0) == ord('r'):
                speaker.say(text.replace("\n\n",". ").replace("\n"," "))
                speaker.run()
                speaker.say("Press s to scan the next page. Press q to quit.")
            elif cv.waitKey(0) == ord('s'):
                speaker.say("Saving")
                speaker.run()
                with open(img_url.replace("png","txt"),'w') as f:
                    f.write(text.replace("\n"," "))
                speaker.say("Document saved")
                speaker.run()
                cv.destroyAllWindows()
                self.open_camera(speaker)
                return text
            elif cv.waitKey(0) == ord('q'):
                cv.destroyAllWindows()
                return text