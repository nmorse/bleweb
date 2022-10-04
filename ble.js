/*
A minimal Web Bluetooth connection example

created 6 Aug 2018
by Tom Igoe
*/
var myDevice;
/// var myService = 0x6e400001; // 0xfebb;        // fill in a service you're looking for here
var uartService = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
var uartRxCharacteristic;
var uartTxCharacteristic;

function connect(){
  navigator.bluetooth.requestDevice({
    // filters: [myFilters]       // you can't use filters and acceptAllDevices together
    optionalServices: [uartService],
    acceptAllDevices: true
  })
  .then(function(device) {
    // save the device returned so you can disconnect later:
    myDevice = device;
    console.log(device);
    // connect to the device once you find it:
    return device.gatt.connect();
  })
  .then(function(server) {
    // get the primary service:
    return server.getPrimaryService(uartService);
  })
  .then(function(service) {
    // get the  characteristic:
    return service.getCharacteristics();
  })
  .then(function(characteristics) {
    // subscribe to the characteristic if it has notify?
    for (c in characteristics) {
      console.log("characteristics[c]", characteristics[c])
      if (characteristics[c].properties.notify) {
        console.log("got Rx characteristic")
        uartRxCharacteristic = characteristics[c];
        characteristics[c].startNotifications()
        .then(subscribeToChanges);
      }
      if (characteristics[c].properties.write) {
        console.log("got Tx characteristic")
        uartTxCharacteristic = characteristics[c];
      }
    }
  })
  .catch(function(error) {
    // catch any errors:
    console.error('Connection failed!', error);
  });
}

// subscribe to changes from the meter:
function subscribeToChanges(characteristic) {
  characteristic.oncharacteristicvaluechanged = handleData;
}

// handle incoming data:
function handleData(event) {
  // get the data buffer from the meter:
  var buf = new Uint8Array(event.target.value);
  console.log(buf);
}

// disconnect function:
function disconnect() {
  if (myDevice) {
    // disconnect:
    myDevice.gatt.disconnect();
    uartRxCharacteristic = null;
    uartTxCharacteristic = null;
  }
}

async function send_text(data) {
  while(data.length > 0) {
    let chunk = data.slice(0, 18);
    data = data.slice(18);
    if (uartTxCharacteristic) {
      special_continue_char = data.length ? ',' : '' 
      console.log("chunk+special_continue_char", chunk+special_continue_char)
      var sent = await uartTxCharacteristic.writeValueWithResponse(new TextEncoder().encode(chunk+special_continue_char));
      console.log(sent);
    }
    else {
      console.log("no TX characteristic of the service availible");
    }
  }
}