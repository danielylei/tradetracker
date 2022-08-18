function switchTab(tab){
	var i;
	var x = document.getElementsByClassName("trades_tab");
	alert('test');
	for (i=0; i<x.length;i++){
		x[i].style.display = "none";
	}
	document.getElementById(tab).style.display = "block";
}

$(document).ready(function(){
	$('#allTrades').DataTable({
		"pagingType": "simple"
	});

	alert('test');
});
