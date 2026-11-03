const messageBox = document.getElementById("message");
const tableBody = document.getElementById("book-table");

function showMessage(text) {
  messageBox.textContent = text;
}

async function loadBooks() {
  const response = await fetch("/books");
  const books = await response.json();
  tableBody.innerHTML = "";

  for (const book of books) {
    const row = document.createElement("tr");
    const status = book.is_borrowed
      ? '<span class="borrowed">Borrowed</span>'
      : '<span class="available">Available</span>';
    const actionButton = book.is_borrowed
      ? `<button class="return-btn" onclick="returnBook(${book.id})">Return</button>`
      : `<button class="borrow-btn" onclick="borrowBook(${book.id})">Borrow</button>`;

    row.innerHTML = `
      <td>${book.id}</td>
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${status}</td>
      <td>
        ${actionButton}
        <button class="delete-btn" onclick="deleteBook(${book.id})">Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  }
}

async function sendRequest(url, method, body) {
  const options = { method: method };
  if (body) {
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json();
    showMessage(error.detail || "Something went wrong");
    return false;
  }
  showMessage("");
  return true;
}

document.getElementById("book-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const book = {
    id: parseInt(document.getElementById("book-id").value),
    title: document.getElementById("book-title").value,
    author: document.getElementById("book-author").value,
    is_borrowed: false
  };
  const ok = await sendRequest("/books", "POST", book);
  if (ok) {
    event.target.reset();
  }
  loadBooks();
});

async function borrowBook(id) {
  await sendRequest(`/books/${id}/borrow`, "POST");
  loadBooks();
}

async function returnBook(id) {
  await sendRequest(`/books/${id}/return`, "POST");
  loadBooks();
}

async function deleteBook(id) {
  await sendRequest(`/books/${id}`, "DELETE");
  loadBooks();
}

loadBooks();