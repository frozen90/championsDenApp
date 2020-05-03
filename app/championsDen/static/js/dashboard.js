

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




var messages_modal = document.getElementById("messages_modal");
var my_modal_gameplay = document.getElementById("upload_gameplaymodal");
var upload_btn = document.getElementById("openUploadGameplayForm");
var messages_btn_dash = document.getElementById("messages_btn_dash")
var span_btn = document.getElementById("close_modal")
var span_btn_msg_close = document.getElementById("close_msg_modal")

upload_btn.onclick = function() {
  console.log(modal)
  my_modal_gameplay.style.display = "block";
}
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


async function closeModal(){
  messages_modal.style.display = "none";
}


async function submitFeedbackForm(){

  var video_url = document.getElementById('video_url').value
  var course_id = document.getElementById('course_name').value
  var position_played = document.getElementById('position_played').value
  fetch('http://127.0.0.1:8000/feedback?video_url='+ video_url + '&course_id=' + course_id + '&position_played=' + position_played)
  .then(response => {
    return response.json();
  })
  .then(message =>{
    cont = document.getElementById('message_container')
    cont.innerHTML = message.message
    document.getElementById('video_url').value = ''
    document.getElementById('course_name').value = ''
    document.getElementById('position_played').value = ''
  })
}



fetch('http://127.0.0.1:8000/lpprogress?get_lp=get')
  .then(response => {
    return response.json();
  })
  .then(data => {
    console.log(data.x_set)
    console.log(data.y_set)
    var y_set_to_plot = []
    var x_set_to_plot = []
    for (var i = 0; i < data.counter; i++) {
      y_set_to_plot.push(data.y_set[i])
      x_set_to_plot.push(data.x_set[i])
    }
    console.log(y_set_to_plot)
    console.log(x_set_to_plot)
      var trace1 = {
        x: x_set_to_plot,
        y: y_set_to_plot,
        mode: 'lines',
        type: 'scatter',
        name: '2020',

      };


    var data = [trace1];
    var layout = {

    title: 'LP Progress Season 10',
    titlefont: {
      family: 'Arial, sans-serif',
      size: 18,
      color: 'lightgrey'
    },
    showlegend: false,
    plot_bgcolor: "#272932",
    paper_bgcolor: "#272932",
    xaxis: {
      title: 'Date',
      type:'date',
      titlefont: {
        family: 'Arial, sans-serif',
        size: 18,
        color: 'lightgrey'
      },
      showticklabels: true,
      tickangle: 'auto',
      tickfont: {
        family: 'Old Standard TT, serif',
        size: 14,
        color: 'black'
      },
      exponentformat: 'e',
      showexponent: 'all'
    },
    yaxis: {
      title: 'LP Points',
      titlefont: {
        family: 'Arial, sans-serif',
        size: 18,
        color: 'lightgrey'
      },
      showticklabels: true,
      tickangle: 45,
      tickfont: {
        family: 'Old Standard TT, serif',
        size: 14,
        color: 'black'
      },
      exponentformat: 'e',
      showexponent: 'all'
    }


    };

    TESTER = document.getElementById('tester');
    Plotly.newPlot(TESTER,data,layout,{staticPlot:true});
  })






// fetch('http://127.0.0.1:8000/check')
//     .then(response => {
//       return response.json();
//     })
//     .then(users => {
//       console.log(users);
//     })
