var fs = require('fs');
var natural = require('natural');
var classifier = new natural.BayesClassifier();

natural.BayesClassifier.load('../classifier.json', null, function(err, classifier) {
  if (err) {
    throw err;
  }

  fs.readFile('results.txt', function(err, data) {
    if (err) {
      throw err;
    }

    var results = data.toString().split('\n');

    for (var i in results) {
      console.log(results[i], ': ', classifier.classify(results[i]))
    }
  });
});