import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import serial
import time
import Image
import ImageDraw
import ImageFont
from firebase import firebase

# 라즈베리파이 포트 번호
port = "/dev/ttyACM0"
seri = serial.Serial(port, 9600, timeout = 2)
seri.flushInput()

def func1():
	str = 'A'
	seri.write(bytes(str.encode()))

def func2():
	str = "B"
	seri.write(bytes(str.encode()))

# 파이어베이스 주소
firebase = firebase.FirebaseApplication("https://rasbebe-1205.firebaseio.com/", None)
resultA = firebase.get('/multitap', 'switch_A')
resultB = firebase.get('/multitap', 'switch_B')

timer10 = firebase.get('/powersaving', 'timer10')

RST = 24
DC = 23
SPI_PORT =0
SPI_DEVICE =0

disp=Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height=disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline = 0, fill=0)

padding = 2
shape_width = 20
top = padding
bottom = height-padding
x = padding


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

font = ImageFont.load_default()

draw.text((x,top), 'MultiTap', font=font, fill = 255)
draw.text((x, top+20), 'RasBebe', font=font, fill=255)
disp.image(image)
disp.display()
	
while True:
	timer10 = firebase.get('/powersaving', 'timer10')
	inputASC1 = 0
	inputASC2 = 0
	if resultA == True:
		print("pin 11, bcm 17 ON")
                GPIO.output(17, False)
		func1()
		inputASC1 = ''
		time.sleep(1.2)
		while seri.inWaiting():
			inputASC1 = seri.readline()
		print(inputASC1)
		firebase.put('/statistic', 'statistic_1',inputASC1)

		if resultB == True:
                	print("pin 12, bcm 18 ON")
                        GPIO.output(18, False)
                        func2()
                        inputASC2 = ''
                        time.sleep(1.2)
                        while seri.inWaiting():
  	                      inputASC2 = seri.readline()
                        print(inputASC2)
                        firebase.put('/statistic', 'statistic_2', inputASC2)
                                    
		elif resultB == False:
			print("pin 12, bcm 18 OFF")
			GPIO.output(18, True)
              
	elif resultA == False :
        	print("pin 11, bcm 17 OFF")
                GPIO.output(17, True)

		if resultB == True:
			print("pin 12, bcm 18 ON")
			GPIO.output(18, False)
			func2()
			inputASC2 = ''
			time.sleep(1.2)
			while seri.inWaiting():
				inputASC2 = seri.readline()
			print(inputASC2)
			firebase.put('/statistic', 'statistic_2', inputASC2)
                                    
		elif resultB == False:
			print("pin 12, bcm 18 OFF")
			GPIO.output(18, True)
	print (timer10)
	if timer10 == True:
		print("timer start!")
		time.sleep(5)
		print("pin11, 12 OFF")
		GPIO.output(17, True)
		firebase.put('/multitap', 'switch_A',False)
		GPIO.output(18, True)
		firebase.put('/multitap', 'switch_B', False)
		firebase.put('/powersaving', 'timer10', False) 
                    
        '''if resultA == True and resultB == True:                     
            #disp.clear()
            #disp.display()
            draw.text((x,top), '1 On', font=font, fill = 255)
            draw.text((x, top+20), '2 On', font=font, fill=255)
            disp.image(image)
            disp.display()
            disp.clear()
            
        elif resultA == True and resultB == False:
            #disp.clear()
            #disp.display()
            draw.text((x,top), '1 On', font=font, fill = 255)
            draw.text((x, top+20), '2 Off', font=font, fill=255)
            disp.image(image)
            disp.display()
            disp.clear()
        
        elif resultA == False and resultB == True :
            #disp.clear()
            #disp.display()
            draw.text((x,top), '1 Off', font=font, fill = 255)
            draw.text((x, top+20), '2 On', font=font, fill=255)
            disp.image(image)
            disp.display()
            disp.clear()

        elif resultA == False and resultB == False:
            #disp.clear()
            #disp.display()
            draw.text((x,top), '1 Off', font=font, fill = 255)
            draw.text((x, top+20), '2 Off', font=font, fill=255)
            disp.image(image)
            disp.display()
            disp.clear()'''
            
            
	print("---------------------------------------------------------")
        time.sleep(1)
        


        resultA = firebase.get('/multitap', 'switch_A')
        resultB = firebase.get('/multitap', 'switch_B')
        

GPIO.cleanup()
print("Shutdown All relays")
