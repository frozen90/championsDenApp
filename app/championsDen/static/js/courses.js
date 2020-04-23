
counter = 1
async function updateSection(){

video_url = document.getElementById('video_url').value;
section_title = document.getElementById('section_title').value;
section_description = document.getElementById('section_description').value;


document.getElementById("sections").innerHTML += "<div class='div-block-34' style='border-bottom: 5px solid #101d42' ><div><div class='text-block-12'>Section " + counter + " : " + section_title + '</div></div></div>';
document.getElementById("wf-form-Course-Form").innerHTML += '<input name="' + "section" + counter.toString() + '_section_title" type="hidden" value="' + section_title + '">' + "<input name=" + "section" + counter.toString() + '_section_description'+' type="hidden" value="' + section_description + '">' + "<input name=" + "section" + counter.toString() + '_video_url type="hidden"' + "value="  + video_url + ">";
document.getElementById("counter").value = counter;
counter ++;


}
