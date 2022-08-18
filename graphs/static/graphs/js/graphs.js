function switchTab(tab){
	var i;
	var x = document.getElementsByClassName("trades_tab");
	for (i=0; i<x.length;i++){
		x[i].style.display = "none";
	}
	document.getElementById(tab).style.display = "block";
}


