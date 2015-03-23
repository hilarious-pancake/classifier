var fs = require('fs');
var natural = require('natural');
var classifier = new natural.BayesClassifier();

function readData(category) {
  // read file associated with category
  fs.readFile('data/' + category + '-desc.txt', function(err, data) {
    if (err) {
      throw err;
    }

    // split data on new lines
    var items = data.toString().split('\n');

    // add each item with associated category to classifier
    for (var i in items) {
      classifier.addDocument(items[i], category)
    }

    // train classifier
    classifier.train();
    
    // save classifier
    classifier.save('classifier.json', function(err, classifier) {
      if (err) {
        throw err;
      }
    });
  });
}

// call readData() on compost, recycle, and landfill datasets
readData('compost');
readData('recycle');
readData('landfill');
