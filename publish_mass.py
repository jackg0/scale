import mass_finder as mf
import paho.mqtt.client as mqtt

broker = "172.29.103.87"
start = "OFF"

def on_message(client, userdata, msg):
    if msg.topic == "game/start2":
        global start
        start = str(msg.payload)

client = mqtt.Client("scale")
client.connect(broker, 1883, 60)
client.subscribe("game/start2")
client.on_message = on_message
client.loop_start()
mf.setup()


while 1:
    if start == "ON":
        mf.startGame()
        while 1:
            status = mf.getGameStatus()
            client.publish("game/scale_game", payload=status[0])
            if (status[1]):
                client.publish("game/stop2", payload="OFF")
                start = "OFF"
                break
#client.publish("game/stop2", payload="OFF")


