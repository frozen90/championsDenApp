var my_modal = document.getElementById("skill_assesment");

var take_assesment_btn = document.getElementById("openAlgForm");

var get_path_btn = document.getElementById("get_path")

var courses_path = document.getElementById("path_container")

var form_cont = document.getElementById("suggested_path_container")


take_assesment_btn.onclick = function() {

  my_modal.style.display = "block";
  form_cont.style.display = "inline-block";

}



window.onclick = function(event) {
  if (event.target == modal) {
    my_modal.style.display = "none";
  }
}
