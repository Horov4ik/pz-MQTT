const mqtt = require('mqtt')

const client  = mqtt.connect('mqtt://localhost:1883')

const topic = 'test/topic'

client.on('connect', function () {
  console.log('Publisher connected')
  const payload = JSON.stringify({ time: new Date().toISOString(), msg: 'hello from publisher' })
  client.publish(topic, payload, { qos: 1 }, function (err) {
    if (err) console.error('Publish error', err)
    else console.log('Published:', payload)
    client.end()
  })
})
