import cv2
import imutils
import pytesseract
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cam = cv2.VideoCapture(0)   # 0 -> index of camera

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()


# read the image
image = cv2.imread('opencv_frame_0.png')

# resize image
image = imutils.resize(image, width=500)

cv2.imshow("Original Image", image)
cv2.waitKey(0)

# Convert to grey Scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grey scale image ", gray)
cv2.waitKey(0)

# reduce noise in image
gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("Grey scale image Reduce Noise ", gray)
cv2.waitKey(0)

# edges of image
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("Edges of image ", edged)
cv2.waitKey(0)

# contours
cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Draw all the contours
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
cv2.imshow("New Image after contouring ", image1)
cv2.waitKey(0)

# sorted to top 30
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:70]
numberPlateCount = None

# New Image Copy with top 30 cont
image2 = image.copy()
cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
cv2.imshow("New Image Top 30 contouring ", image2)
cv2.waitKey(0)

# Find the best contours using loop
count = 0
name = 1

for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
    # print(len(approx))
    if len(approx) == 4:
        numberPlateCount = approx
        x, y, w, h = cv2.boundingRect(i)
        crop_img = image[y:y + h, x:x + w]

        cv2.imwrite(str(name) + '.png', crop_img)
        name += 1

        break

# identified number plate in Main Image
cv2.drawContours(image, [numberPlateCount], -1, (0, 255, 0), 3)
cv2.imshow("Final Image", image)
cv2.waitKey(0)


# crop the number plate only
crop_img_loc = '1.png'
cv2.imshow("Cropped Image ", cv2.imread(crop_img_loc))


# Convert Image to text
text = pytesseract.image_to_string(crop_img_loc,lang='eng')
if text:
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    print(date_time, ' : ', text)
else:
    print("No text found")
cv2.waitKey(0)



