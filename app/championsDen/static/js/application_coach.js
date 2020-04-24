var modal = document.getElementById("modal");
var btn = document.getElementById("openApplicationForm");
var span = document.getElementsByClassName("close")[0];
var continue_button = document.getElementById("contBtn");
var first_right_column = document.getElementById("right_column_first");
var second_right_column = document.getElementById("right_column_second");
var final_right_column = document.getElementById("right_column_final");
var personal_info_check = document.getElementById("personal_info_check");
var coach_info_check = document.getElementById("coach_info_check");
var submit_application_check = document.getElementById("submit_application_check");
var personal_info_text = document.getElementById("personal_info_text");
var coach_info_text = document.getElementById("coach_info_text");
var submit_app_text = document.getElementById("submit_app_text");

click_ctr = 0


btn.onclick = function() {
  modal.style.display = "flex";
}


window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

continue_button.onclick = function(){
  console.log("im here");
  if (click_ctr == 0) {
    first_right_column.style.display = "none";
    second_right_column.style.display = "block";
    personal_info_check.style = "background-color: grey;";
    personal_info_text.style = "color: grey;";
    coach_info_check.style = "background-color: white;";
    coach_info_text.style = "color: white;";


    click_ctr = click_ctr + 1;
    console.log(click_ctr);
  }else if (click_ctr == 1) {
    second_right_column.style.display = "none";
    final_right_column.style.display = "block";
    coach_info_check.style = "background-color: grey;";
    coach_info_text.style = "color: grey;";
    submit_application_check.style = "background-color: white;";
    submit_application_text.style - "color: white;";

  }
}
