
function getArduinoVals(){
    $.getJSON("http://localhost:8080/test.json", function(data){
        $('#images').html(data.val);
    });
    t = setTimeout("getArduinoVals()",50);
    $.getJSON("http://api.flickr.com/services/feeds/photos_public.gne?tags=cat&tagmode=any&format=json&jsoncallback=?",
        function(data){
            alert("HI");
          $.each(data.items, function(i,item){
            $("<img/>").attr("src", item.media.m).appendTo("#images");
            if ( i == 3 ) return false;
          });
        });
}
	
$(document).ready(function(){
    getArduinoVals();
});
