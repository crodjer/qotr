function InvalidEncryptionError (message) {
  this.name = 'InvalidEncryptionError';
  this.message =  message || 'The text is not encrypted or correctly encrypted';
}
InvalidEncryptionError.prototype = Error.prototype;

export default InvalidEncryptionError;
