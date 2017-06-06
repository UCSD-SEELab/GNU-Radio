from ardupilot import ArduPilot

AP = ArduPilot('udp:localhost:14550', 15200, True)

print ("Finished instantiating AP")
print AP.getMode();
print "Finished getting mode"
AP.arm()
AP.setDataStreams()

while True:
	while True:
	    try: 
	        print AP.getAltitude()
	        print "getting altitude ",
	        break
	    except Exception:
	        print "",
	        #print "exception 1"
	
	while True:
	    try:
	        print "getting heading ",
	        print AP.getHeading()
	        break
	    except Exception:
	        print "",
	        #print "exception 2"
	
	while True:
	    try:
	        print "getting speed ",
	        print AP.getSpeed()
	        break
	    except Exception:
	        print "",
	        #print "exception 3"
	
	
	while True:
	    try:
	        print "getting GPS location ",
	        print AP.getLocation()
	        break
	    except Exception:
	        print "",
	        #print "exception 3"
	
	
	while True:
	    try:
	        print "getting attitude",
	        print AP.getAttitude()
	        break
	    except Exception:
	        print "",
	        #print "exception 3"
