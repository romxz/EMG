from bottle import route, run
import serial
dic = {}
ser = serial.Serial(port='COM6',baudrate=9600,timeout=None)
@route('/test')

def test():
    c = ser.readline()
    c = (str(c)[2:-5])
    dic["val"] = c
    return(dic)

run(host='localhost', port=8080, debug=True)
