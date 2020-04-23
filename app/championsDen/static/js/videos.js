async function getVideo(id){
  index = id
  video_url_object = document.getElementById('section_url'+index);
  video_url = video_url_object.value
  section_description = document.getElementById(index)

  paragaph_to_append = document.getElementById("paragraph_section")
  console.log(section_description);

  video_frame = document.getElementById('video_frame');

  video_frame.src = video_url;
  paragaph_to_append.innerHTML = section_description.value;
}
