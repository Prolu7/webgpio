#!/usr/bin/env python

from gpiozero import PWMOutputDevice
from gpiozero import DigitalInputDevice
from gpiozero import DigitalOutputDevice

import asyncio
from websockets.server import serve
from websockets import broadcast

import json

#structure of JSON data to send
#JsonDataToReceive = {
#	"data":[
#		0.5,
#		True,
#		False
#	]
#};
##structure of JSON data to receive
#JsonDataToSend = {
#	"gpio":[
#		{"type":"PWMOutputDevice","data":"0.5"},
#		{"type":"DigitalOutputDevice","data":False},
#		{"type":"DigitalInputDevice","data":False}
#	]
#};

websocketsList = []

UsableGpio = [2,3,4,5,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] #24 usable gpio pins

ActiveGpio = []
GpioType = []
GpioData = []

realDevices = []

async def webconnection(websocket):
	await websocket.send(json.dumps(updateGpioData()))
	websocketsList.append(websocket)
	async for message in websocket:
		if(message == "kys"):
			print("death")
			stop()
			return
		
		if("set" in message):
			print("set in message")
			return
		print(f"message = {message}")
		setNewGpioData(message)
		await websocket.send(json.dumps(updateGpioData()))
		broadcast(websocketsList,json.dumps(updateGpioData()))

async def main():
	ActiveGpio.append(4)
	ActiveGpio.append(17)
	ActiveGpio.append(27)
	GpioType.append("PWMOutputDevice")
	GpioType.append("DigitalOutputDevice")
	GpioType.append("DigitalOutputDevice")
	GpioData.append(0)
	GpioData.append(0)
	GpioData.append(0)
	updateUsedGpio()
	#example
	async with serve(webconnection, "192.168.1.205", 8765):
		await asyncio.Future()  # run forever

def stop():
	#terminate the loop
	asyncio.get_event_loop().stop()

def updateUsedGpio():
	for i in range(len(realDevices)):
		realDevices[i].close()
	realDevices.clear()
	for i in range(len(ActiveGpio)):
		GpioNum = ActiveGpio[i]
		if(GpioType[i] == "PWMOutputDevice"):
			realDevices.append(PWMOutputDevice(GpioNum))
			pass
		if(GpioType[i] == "DigitalOutputDevice"):
			realDevices.append(DigitalOutputDevice(GpioNum))
			pass
		if(GpioType[i] == "DigitalInputDevice"):
			realDevices.append(DigitalInputDevice(GpioNum))
			pass

def setNewGpioData(jsonString):
	jsonObject = json.loads(jsonString)
	for i in range(min(len(realDevices), len(jsonObject["data"]))):
		realDevices[i].value = float(jsonObject["data"][i])*.01

def updateGpioData():
	jsonObject = []
	for i in range(len(realDevices)):
		gpioDictionary = {}
		if(GpioType[i] == "PWMOutputDevice"):
			GpioData[i] = realDevices[i].value
			pass
		if(GpioType[i] == "DigitalOutputDevice"):
			GpioData[i] = realDevices[i].value == 1
			pass
		gpioDictionary = {"type":GpioType[i], "data":GpioData[i]}
		jsonObject.append(gpioDictionary)
	jsonDictionary = {"gpio":jsonObject}
	return jsonDictionary

asyncio.run(main())
