/* utils.js
 * 
 * This file contains helper utility functions/objects for use by the
 * main experiment code.
 */


// Object to hold the state of the experiment. 
var State = function () {

    // 0 (false) or 1 (true)
    this.instructions = 1;
    // Trial index
    this.index = 0;
    // One of the phases defined in TRIAL
    this.trial_phase;

    // Update the instructions flag. Defaults to 1.
    this.set_instructions = function (instructions) {
        if (instructions != undefined) {
            this.instructions = instructions;
        } else {
            this.instructions = 1;
        }
    };

    // Update the trial index. Defaults to 0.
    this.set_index = function (index) {
        if (index != undefined) {
            this.index = index;
        } else {
            this.index = 0;
        }
    };

    // Return a list of the state's properties in human-readable form,
    // to be recorded as data in the database
    this.as_data = function () {
        var instructions = Boolean(this.instructions);
        var index = this.index;
        
        return {
            'instructions': instructions,
            'index': index, 
        };
    };
};

// Object to properly format rows of data
var DataRecord = function () {
    this.update = function (other) {
        _.extend(this, other);
    };
};

// Log a message to the console, if debug mode is turned on.
function debug(msg) {
    if ($c.debug) {
        console.log(msg);
    }
}

// Throw an assertion error if a statement is not true.
function AssertException(message) { this.message = message; }
AssertException.prototype.toString = function () {
    return 'AssertException: ' + this.message;
};
function assert(exp, message) {
    if (!exp) {
        throw new AssertException(message);
    }
}

// Open a new window and display the consent form
function open_window(hitid, assignmentid, workerid) {
    popup = window.open(
        '/consent?' + 
            'hitId=' + hitid + 
            '&assignmentId=' + assignmentid + 
            '&workerId=' + workerid,
        'Popup',
        'toolbar=no,' +
            'location=no,' +
            'status=no,' +
            'menubar=no,' + 
            'scrollbars=yes,' + 
            'resizable=no,' + 
            'width=' + screen.availWidth + ',' +
            'height=' + screen.availHeight + '');
    popup.onunload = function() { 
        location.reload(true) 
    };
}

// Update the progress bar based on the current trial and total number
// of trials.
function update_progress(num, num_trials) {
    debug("update progress");
    var width = 2 + 98 * (num / (num_trials - 1.0));
    $("#indicator-stage").css({"width": width + "%"});
    $("#progress-text").html("Progress " + (num + 1) + "/" + num_trials);
}

function update_progress1(num, num_trials) {
    debug("update progress1");
    var x = 2 + 98 * (num / (num_trials - 1.0));
    $("#indicator-stage1").css({"width": x + "%"});
    $("#progress-text1").html("Progress " + (num + 1) + "/" + num_trials);
}

//Shuffle an array 

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex ;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}
