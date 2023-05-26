from smbus import SMBus

addr = 0x8 
bus = SMBus(1)

numb = 1

print("Enter 1 for On or 0 for OFF")
while numb == 1:

	ledstate = input(">>>>	")

	if ledstate == "1":
		bus.write_byte(addr, 0x1) # switch it on
	elif ledstate = "0":
		bus.write_byte(addr,0x0) # switch it off
	else:
		numb = 0

