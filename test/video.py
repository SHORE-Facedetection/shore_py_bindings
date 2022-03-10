import numpy as np
import cv2
import shore


def getShoreContent():

    # Open default webcam (/dev/video0)
    cap = cv2.VideoCapture(0)
    framerate = cap.get(cv2.CAP_PROP_FPS)

    if framerate == 0:
        framerate = 30
    print(framerate)
    # Refer to SHORE documentation for parameter description
    eng = shore.CreateFaceEngine(timeBase=1/float(framerate), modelType="Face.Front",
                                 searchParts="On",analyzeExpression="Dnn", 
                                 analyzeDemography="Dnn",pointLocator="Face68")
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if(not ret):
            print ("cannot get frame")
            cap.open(0)
            break
        shape = np.shape(frame)
        content = eng.Process(frame, "BGR")
        if(content):
            cv2.putText(frame, "FPS: " + str(content.getInfoOf('FrameRate')),
                        (5, shape[0] - 20 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0,255,0), 1, cv2.LINE_AA)
            # Iterate over all detected objects
            for j in range(0,content.getObjectCount()):
                obj = content.getObject(j)
                gender = obj.getAttributeOf('Gender')
                age = obj.getRatingOf('Age')
                happy = obj.getRatingOf('Happy')
                id = obj.getAttributeOf('Id')
                rect = obj.getRegion()
                if (rect != None):
                    cv2.rectangle(frame,
                                  (int(rect.getLeft()), int(rect.getTop())),
                                  (int(rect.getRight()), int(rect.getBottom())),
                                  (255,0,0))
                    cv2.putText(frame, "Id: " + str(id),
                                (int(rect.getLeft()), int(rect.getBottom()) + 15 ),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                    cv2.putText(frame, "Gender: " + str(gender),
                                (int(rect.getLeft()), int(rect.getBottom()) + 30 ),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                    cv2.putText(frame, "Age: " + str(age),
                                (int(rect.getLeft()), int(rect.getBottom()) + 45 ),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                    cv2.putText(frame, "Happy: " + str(happy),
                                (int(rect.getLeft()), int(rect.getBottom()) + 60 ),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
         

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    shore.DeleteEngine(eng)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    getShoreContent()