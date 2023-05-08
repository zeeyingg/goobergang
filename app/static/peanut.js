var clicke = function(e) { // changes vis of all paragraphs
    var parags = document.getElementsByTagName('p')[0];
    parags.innerHTML = "hi";
    console.log("clicked")
}

var changevisibility = function(x) {
    if(x.visibility != "hidden") {
        console.log(x.visibility);
    }
}

var clickme = document.getElementById("cickme");
clickme.addEventListener("click", clicke);