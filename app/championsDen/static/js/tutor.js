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
