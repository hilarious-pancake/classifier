var fs = require('fs');
var natural = require('natural');
var classifier = new natural.BayesClassifier();

function readData(category) {
  fs.readFile('data/' + category + '-desc.txt', function(err, data) {
    if (err) {
      throw err;
    }

    var items = data.toString().split('\n');

    for (var i in items) {
      classifier.addDocument(items[i], category)
    }

    classifier.train();
    
    // save classifier
    classifier.save('classifier.json', function(err, classifier) {
      if (err) {
        throw err;
      }
    });
  });
}

readData('compost');
readData('recycle');
readData('landfill');
