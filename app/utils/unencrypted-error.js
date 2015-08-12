function UnencryptedError (message) {
  this.name = 'UnencryptedError';
  this.message =  message || 'Recieved unencrypted text!';
}
UnencryptedError.prototype = Error.prototype;

export default UnencryptedError;
