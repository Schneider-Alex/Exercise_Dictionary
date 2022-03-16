
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
        // this how we set up a post request and send the form data.
        fetch(`http://127.0.0.1:5000/createcomment`, { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => {
                console.log(data)
                console.log(data.content)
                var comments = document.getElementById('comments');
                let row = document.createElement('li');
                let content = document.createElement('p');
                content.innerHTML = form.get('content');
                content.innerHTML = data['content'] +' - '+ data['written_by'];
                row.appendChild(content);
                comments.appendChild(row);
                document.getElementById('commentContent').value=""
            } )
        
                
    }


