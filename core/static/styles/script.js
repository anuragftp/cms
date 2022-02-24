
var elems = document.getElementsByClassName('confirmation');
var confirmIt = function (e) {
    if (!confirm('Are you sure to delete ?')) e.preventDefault();
};
for (var i = 0, l = elems.length; i < l; i++) {
  elems[i].addEventListener('click', confirmIt, false);
}




    // window.onbeforeunload = function() {
  //                  var Ans = confirm("Are you sure you want change page!");
  //                  if(Ans==true)
  //                      return true;
  //                  else
  //                      return false;
  //              };