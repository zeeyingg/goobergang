```
HELLO
```

var clickme = document.getElementById("cickme");
clickme.addEventListener("click", clcike());

var clicke = function(e) { // changes vis of all paragraphs
    var parags = document.getElementsByTagName('p')[0];
    parags.innerHTML = "hi";
}

var changevisibility = function(x) {
    if(x.visibility != "hidden") {
        console.log(x.visibility);
    }
}