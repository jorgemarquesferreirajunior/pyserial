import numpy as np
import cv2


def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lower_limit = (hsvC[0][0][0] - 10, 100, 100)
    upper_limit = (hsvC[0][0][0] + 10, 255, 255)

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


def get_limits2(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lower_limit = (hsvC[0][0][0] - 172, 100, 100)
    upper_limit = (hsvC[0][0][0] + 178, 255, 255)

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)

    return lower_limit, upper_limit


def get_limits_red():
    # Limites para a cor vermelha
    lower_limit1 = np.array([0, 100, 100], dtype=np.uint8)  # Intervalo inferior
    upper_limit1 = np.array([10, 255, 255], dtype=np.uint8)  # Intervalo superior

    lower_limit2 = np.array([170, 100, 100], dtype=np.uint8)  # Intervalo inferior
    upper_limit2 = np.array([180, 255, 255], dtype=np.uint8)  # Intervalo superior

    return (lower_limit1, upper_limit1), (lower_limit2, upper_limit2)
