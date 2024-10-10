import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def get_color(hue_value):
    color = "undefined"
    if hue_val < 7:
        color = "red"
    elif hue_val < 19:
        color = "orange"
    elif hue_val < 32:
        color = "yellow"
    elif hue_val < 100:
        color = "green"
    elif hue_val < 125:
        color = "blue"
    elif hue_val < 136:
        color = "violet"
    elif hue_val < 162:
        color = "pink"
    elif hue_val >= 162:
        color = "red"
    return color.upper()


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    height, width = frame.shape[:2]
    cx = int(width / 2)
    cy = int(height / 2)
    bgr_pixel_center = frame[cy, cx]
    bgr_pixel_center = tuple(map(int, bgr_pixel_center))
    hsv_pixel_center = hsv_frame[cy, cx]
    hue_val = hsv_pixel_center[0]

    msg = get_color(hue_val) + f" - hue: {str(hue_val)}"

    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)
    cv2.rectangle(frame, (50, 100), (300, 300), bgr_pixel_center, -1)
    text_size, _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    text_w, text_h = text_size
    cv2.rectangle(frame, (50, 60), (50 + text_w, 60 + text_h), (0, 0, 0), -1)
    cv2.putText(frame, msg, (50, 90), 0, 1, (255, 255, 255), 2)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
