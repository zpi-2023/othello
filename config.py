import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1 = 13
led2 = 12
led3 = 19
led4 = 26
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

button_red_pin = 5
button_green_pin = 6
encoder_first_pin = 17
encoder_second_pin = 27
GPIO.setup(button_red_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_green_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder_first_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder_second_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buzzerPin = 23
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, 1)

ws2812pin = 8
