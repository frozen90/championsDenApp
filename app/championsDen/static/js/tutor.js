
var messages_modal = document.getElementById("messages_modal");
var my_modal_gameplay = document.getElementById("upload_gameplaymodal");
var upload_btn = document.getElementById("openUploadGameplayForm");
var messages_btn_dash = document.getElementById("messages_btn_dash")
var span_btn = document.getElementById("close_modal")
var span_btn_msg_close = document.getElementById("close_msg_modal")

messages_btn_dash.onclick = function(){
  messages_modal.style.display = "block";
}
span_btn.onclick = function() {
  my_modal_gameplay.style.display = "none";

}
span_btn_msg_close.onclick = function(){
    messages_modal.style.display = "none";

}

window.onclick = function(event) {
  if (event.target == modal) {
    my_modal_gameplay.style.display = "none";
    messages_modal.style.display = "none";
  }
}

current_displayed_element = 0
function displayMessage(id){
  if (current_displayed_element != 0) {
      var get_current_displayed_element = document.getElementById("right_column_" + current_displayed_element.toString())
      get_current_displayed_element.style.display = "none";
  }


  var first_column = document.getElementById('right_column_msg_first')
  first_column.style.display = "none";
  var element_to_be_displayed = document.getElementById("right_column_"+id)
  element_to_be_displayed.style.display = "block";
  current_displayed_element = id
  console.log(current_displayed_element)


}



async function messageRead(id){
  fetch('http://127.0.0.1:8000/message?id=' + id)
  .then(response => {
    return response.json();
  })
  .then(data =>{

    div_to_style = document.getElementById('message_read_' + data.message_readed.toString())
    div_to_style.style.color = "black";

  })}





function playFeedback (id){
  index = id.toString();
  video_url = document.getElementById('video_url_' + id).value;
  playback_field = document.getElementById('video_playback_field');
  feedback_id = document.getElementById('feedback_id');
  console.log(feedback_id)
  feedback_id.value = id;
  playback_field.src = video_url;


};

async function sendFeedback(){
  var feedback_id = document.getElementById('feedback_id').value
  var feedback_text = document.getElementById('feedback_text').value
  var feedback_grade = document.getElementById('Grade').value

  if (feedback_text == "") {
    alert("Feedback field cannot be empty");

  }else{
  fetch('http://127.0.0.1:8000/feedback?feedback_id='+ feedback_id + '&feedback_text=' + feedback_text + '&grade=' + feedback_grade)
  .then(response => {
    return response.json();
  })
  .then(data =>{

    alert(data.message)
    div_to_delete = document.getElementById('div_' + data.feedback_id )
    div_to_delete.style.display = "none";

  })}

}
