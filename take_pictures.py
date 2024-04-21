import cv2
import uuid
import os
import time

def countdown_timer(duration, label):
    start_time = time.time()
    while time.time() - start_time < duration:
        remain = duration - (time.time() - start_time)
        ret, frame = cap.read()
        cv2.putText(frame, f'{label} photos. Be ready in {int(remain)+1} seconds...', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Image Collection", frame)
        cv2.waitKey(100)

IMG_PATH = os.path.join('data', 'images')
labels = ['awake', 'sleepy']
num_imgs = 20

cap = cv2.VideoCapture(0)

for label in labels:
    print('Collecting images for {}'.format(label))
    
    countdown_timer(5, label)
    
    for img_num in range(num_imgs):
        print('Collecting images for {}. Image number - {}'.format(label, img_num))

        ret, frame = cap.read()

        img_name = os.path.join(IMG_PATH, label + '.' + str(uuid.uuid1()) + '.jpg')

        cv2.imwrite(img_name, frame)

        cv2.putText(frame, f'Image number: {img_num+1}/{num_imgs}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Image Collection", frame)

        time.sleep(2)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
print("Excellent! All photos collected.")