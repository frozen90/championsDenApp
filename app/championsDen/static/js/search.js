var my_modal = document.getElementById("skill_assesment");
console.log(my_modal)
var take_assesment_btn = document.getElementById("openAlgForm");
console.log(take_assesment_btn)
var get_path_btn = document.getElementById("get_path")
console.log(get_path_btn)
var courses_path = document.getElementById("path_container")
console.log(courses_path)
var form_cont = document.getElementById("suggested_path_container")
console.log(form_cont)

take_assesment_btn.onclick = function() {
  console.log(my_modal)
  my_modal.style.display = "block";
  form_cont.style.display = "inline-block";

}



window.onclick = function(event) {
  if (event.target == modal) {
    my_modal.style.display = "none";
  }
}
