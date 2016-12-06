var filter_table;
filter_table = function(){
    var input, filter, table, tr, td, i;
  input = document.getElementById("sites-filter");
  filter = input.value.toLowerCase();
  table = document.getElementById("sites-table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toLowerCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

$(document).ready(function(){
    $("#sites-filter").bind("keyup", filter_table);
});