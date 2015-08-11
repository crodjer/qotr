/* global re_weburl */

function toTag (url) {
  return '<a target="_blank" href="' + url + '">' + url + '</a>';
}

var punctuation = "[\.,]",
    splitRe = new RegExp([
      punctuation + "$",
      punctuation + "\\s+",
      "\\s+",
    ].join('|'));

export default function tagUrls(message) {
  var urlMap = {};

  message.split(splitRe).forEach(function (slice) {
    if (slice.match(re_weburl)) {
      urlMap[slice] = toTag(slice);
    }
  });

  Object.keys(urlMap).forEach(function (url) {
    var source = url,
        tag = urlMap[url];

    message = message.replace(source, tag);
  });

  return message;
}
