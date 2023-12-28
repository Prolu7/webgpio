const remoteSocket = new WebSocket("ws://192.168.1.205:8765", [
		"protocolOne",
		"protocolTwo"
]);

function stop(){
		remoteSocket.send("kys");
}

//structure of JSON data to receive
var receivedJsonData = {
	"gpio":[
		{"type":"PWMOutputDevice","data":"0.5"},
		{"type":"DigitalOutputDevice","data":false},
		{"type":"DigitalInputDevice","data":false}
	]
};
//structure of JSON data to send
var sentJsonData = {
	"data":[
		0.5,
		true,
		false
	]
};

//websocket client receives message
remoteSocket.onmessage = (event) => {
		var JsonData = JSON.parse(event.data);
		console.log(`Received from websocket`);
		for (let index = 0; index < JsonData.gpio.length; index++) {
			const newData = JsonData.gpio[index];
			display(newData, index)
		}
};

//display input data
function display(data, index) {
	console.log(`Display change`);
	var statusElement = document.getElementsByClassName('status')[index];
	var valueElement = document.getElementsByClassName('value')[index];
	if(data.type == "PWMOutputDevice"){
		statusElement.innerText = `PWM duty cycle at ${Math.round(parseFloat(data.data)*100)}%`;
		valueElement.value = Math.round(parseFloat(data.data)*100);
	}
	else{
		statusElement.innerText = `DigitalOutputDevice set to: ${data.data}`;
		valueElement.checked = data.data;
	}
}


function sendUpdateToWebsocket() {
	var values = [];
	for (let index = 0; index < document.getElementsByClassName('value').length; index++) {
		const element = document.getElementsByClassName('value')[index];
		if(Array.from(document.querySelectorAll('input[type="range"]')).includes(element)){
			values.push(element.value);
		}
		else{
			values.push(element.checked);
		}
	}
	val = {
		"data":values
	};
	console.log(`Sent to Websocket`);
	remoteSocket.send(JSON.stringify(val)); //JSON.stringify()
}
