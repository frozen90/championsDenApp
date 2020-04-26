// async function matchReload(){
  // role = document.getElementById('Role').value
  // type = document.getElementById('Game-Type').value
  // fetch('http://127.0.0.1:8000/check?role='+ role + '&type=' + type)
  //     .then(response => {
  //       return response.json();
  //     })
  //     .then(users => {
  //       console.log(users);
  //       guzik = document.getElementById('reloadButton');
  //       guzik.value = users.change;
  //     })
  // console.log(role, type)

var my_modal = document.getElementById("upload_gameplaymodal");
var upload_btn = document.getElementById("openUploadGameplayForm");
var span_btn = document.getElementById("close_modal")

upload_btn.onclick = function() {
  console.log(modal)
  my_modal.style.display = "block";
}

span_btn.onclick = function() {
  my_modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    my_modal.style.display = "none";
  }
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
