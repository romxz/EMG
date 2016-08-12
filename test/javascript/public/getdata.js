var num = require("./randomdata.js");

function myFunc() {
    document.getElementById("p1").innerHTML = num.random(); 
    //consolelog(num.random)
    //setInterval(function(){
    //    document.getElementById("p1").innerHTML = num.random; 
    //}, 10);
}