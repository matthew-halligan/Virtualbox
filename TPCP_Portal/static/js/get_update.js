function get_server_data(cFunction, htmlID, apiRoute){
      var server_data=new XMLHttpRequest(cFunction);

      server_data.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            cFunction(this, htmlID);
            }
      };

      server_data.open("GET", apiRoute, true);
      server_data.send(null)
  }


function UpdateCounter(server_data, htmlID){
    document.getElementById(htmlID).innerHTML = server_data.responseText;
}

//  <!--    Every 500 miliseconds, call get_server_data()-->
function setIntervalH(cFunction, htmlID, updateInterval, apiRoute){
    setInterval(function(){get_server_data(cFunction, htmlID, apiRoute); console.log("Calling Anonymous")}, updateInterval)
};
//  setInterval(function(){
//        get_server_data(UpdateCounter)
//  }, 500);