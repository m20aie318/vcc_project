fetchNotes();

async function addNote() {
    const title = document.getElementById("recipient-name").value;
    const content = document.getElementById("message-text").value;

    const response = await fetch("http://localhost:5001/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, content }),
    });

    const result = await response.json();
    console.log(result)
    alert(result.message);
    fetchNotes();
}

async function fetchNotes() {
    const response = await fetch("http://localhost:5001/notes");
    const data = await response.json();
    var size = 0;
    let html = "";

    data.notes.forEach(note => {
        var modelid = "note" + size;
        html += ` <div class="noteCard my-2 mx-2 card" style="width: 18rem">
        <div class="card-body">
          <h5 class="card-title">Note ${note.title}</h5>
          <p class="card-text"> ${note.title}</p>
          <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#${modelid}">Details</button>
        </div>
      </div>`;
      size = size + 1
    });

    let notesEle = document.getElementById("notes");
    if (size != 0) {
        notesEle.innerHTML = html;
    }
    else {
        notesEle.innerHTML = `Nothing to show! Use "Add a Note" section to add note`
    }
}


async function searchNotes() {
  const response = await fetch("http://localhost:5001/notes");
  const data = await response.json();
  var size = 0;
  let html = "";

  data.notes.forEach(note => {
      var modelid = "note" + size;
      html += ` <div class="noteCard my-2 mx-2 card" style="width: 18rem">
      <div class="card-body">
        <h5 class="card-title">Note ${note.title}</h5>
        <p class="card-text"> ${note.title}</p>
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#${modelid}">Details</button>
      </div>
    </div>`;
    size = size + 1
  });

  let notesEle = document.getElementById("searched_notes");
  if (size != 0) {
      notesEle.innerHTML = html;
  }
  else {
      notesEle.innerHTML = `Nothing to show! Use "Add a Note" section to add note`
  }
}