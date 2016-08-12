$(document).ready(function(){
    
    $("h2").click(function(){
        
        $.getJSON("http://localhost:8080/test.json", function(data){
        alert(""Data: " + data");
        });
    });
});