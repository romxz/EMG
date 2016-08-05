//var SerialPort = require("serialport").SerialPort;
//var http = require('http');
var numberarray = [];
var SerialPort = require("serialport").SerialPort;
var serialport = new SerialPort("COM6", {baudrate:9600});
serialport.on('open', function(){
    console.log("opena");
    serialport.on("data", function(data){
                for (var i = 0; i<data.length; i++){
                    numberarray.push(String.fromCharCode(data[i]));
                }
                numberarray = numberarray.slice(0, -2);
                console.log(numberarray);
                });
});
/*
var SerialPort = require("serialport");   
var http = require('http');

var numberarray = [];

var serialport = new SerialPort("COM6", {baudRate:9600});
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    serialport.on('open', function(){
        res.write("hi");
        res.write('Serial Port Opened');
        serialport.on('data', function(data){
            for (var i = 0; i<data.length; i++){
                numberarray.push(String.fromCharCode(data[i]));
            }
            numberarray = numberarray.slice(0, -2);
            res.write(numberarray);
        });
  
        
    });
    res.end('Hello World\n');    
}).listen(8080);

console.log('Server running on port 8080.');
*/