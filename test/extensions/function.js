$(document).ready(function(){
    $("div").append("hi");
    chrome.serial.connect(5,{bitrate:9600},function(info){
        connectionId = info.connectionId;
        $("div").append(connectionId);
    });
});