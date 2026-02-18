const mqtt = require('mqtt')

const client  = mqtt.connect('mqtt://localhost:1883')

const topic = 'test/topic'

client.on('connect', function () {
  console.log('Subscriber connected')
  client.subscribe(topic, { qos: 1 }, function (err) {
    if (err) console.error('Subscribe error', err)
    else console.log('Subscribed to', topic)
  })
})

client.on('message', function (t, message) {
  console.log(`Message received on ${t}: ${message.toString()}`)
})
