import time
import VL53L0X

tof = VL53L0X.VL53L0X()

tof.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
	timing = 20000

#Change to constant once we get a trash can :P
trash_height = int(input("Enter height of trash can (in mm): "))

#Helps to set threshold of when to alert client
alert_threshold = trash_height / 5

"""
(Assume a 32 gallon can with height 984.25 mm (38.75 in))
TRASH DETECTION LEVELS:
|TOF facing bottom |
+-------LID--------+
|ALERT:   5-199  mm|
+------------------+
|  BAD: 200-399  mm|
+------------------+
|   OK: 400-599  mm|
+------------------+
| GOOD: 600-799  mm|
+------------------+
|GREAT: 800-1000 mm|
+------------------+
"""

while True:
	distance = tof.get_distance()
	
	if distance <= alert_threshold: #ALERT level
		print(f"ALERT: TRASH CAN ALMOST FULL! ({distance} mm from sensor)") 
		#"High" priority alert
	
	elif alert_threshold <= distance < alert_threshold*2: #BAD level
		print(f"Trash at BAD level, consider emptying. ({distance} mm from sensor)")
		#"Low" priority alert
		
	elif alert_threshold*2 <= distance < alert_threshold*3: #OK level
		print(f"Trash at OK level. ({distance} mm from sensor)")
	elif alert_threshold*3 <= distance < alert_threshold*4: #GOOD level
		print(f"Trash at GOOD level. ({distance} mm from sensor)")
	else: #GREAT level
		print(f"Trash at GREAT level, no need to empty :) ({distance} mm from sensor)")
		
	time.sleep(timing/1000000.00)
	
	
tof.stop_ranging()