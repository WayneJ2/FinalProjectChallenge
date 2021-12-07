var empty_table = document.getElementById("empty_div");
var results_table = document.getElementById("results_table");

function get_results_data(){
    for (var i=1, row; row=results_table.rows[i]; i++){
        if(row.cells[0].innerHTML === row.cells[1].innerHTML){
            row.style.backgroundColor = "lime";
        }
        else{
            row.style.backgroundColor = "orangered";
        }
    }
    empty_table.innerHTML = "";
    empty_table.appendChild(results_table);
}