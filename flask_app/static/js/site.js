
function getExerciseComments(excerciseid){
    fetch('http://127.0.0.1:5000/exercise/<exerciseid>')
        .then(res =>  res.json())
        .then(data => {
            var comments = document.getElementById('comments');
            comments.innerHTML=' '
            console.log(comments)
            for( let i = 0; i < data.length; i++){
                let row = document.createElement('tr');

                let content = document.createElement('td');
                content.innerHTML = data[i].content;
                row.appendChild(content);
                
                let written_by = document.createElement('td');
                written_by.innerHTML = data[i].written_by;
                row.appendChild(written_by);
                comments.appendChild(row);
                console.log(comments)
            }
        })
}





var myForm = document.getElementById('commentSubmit');
    myForm.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(myForm);
        console.log(form.get('content'))
        // this how we set up a post request and send the form data.
        fetch("http://127.0.0.1:5000/createcomment/", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => console.log(data) )
        var users = document.getElementById('users');
        let row = document.createElement('tr');
                let name = document.createElement('td');
                name.innerHTML = form.get('user_name');
                row.appendChild(name);
                
                let email = document.createElement('td');
                email.innerHTML = form.get('email');
                row.appendChild(email);
                users.appendChild(row);
                console.log(users)


    }


