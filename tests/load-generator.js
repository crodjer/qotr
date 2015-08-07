/* globals exports */

/**
 * Generate a join message that we will be sent to a connected client.
 *
 * @async
 * @param {Number} size The specified in bytes for the message. This is ignored.
 * @param {Function} fn The callback function for the data.
 * @public
 */
function joinGenerator (_, fn) {
  // Send a ping to the server. Also, try to join the channel 1 in 1000
  // times. In case the client is already joined we'd get an error, which is
  // fine. This activity ensures that heroku doesn't kill clients abruptly.
  var message = Math.random() <= 0.001 ? {
    "kind": "join",
    "body": (Math.floor(Math.random() * 1000000)).toString()
  } : {
    "kind": "ping",
    "body": null
  };

  return fn(undefined, JSON.stringify(message));
}

exports.utf8 = joinGenerator;
exports.binary = joinGenerator;
