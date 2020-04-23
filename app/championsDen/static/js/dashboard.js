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


}




fetch('http://127.0.0.1:8000/check')
    .then(response => {
      return response.json();
    })
    .then(users => {
      console.log(users);
    })
