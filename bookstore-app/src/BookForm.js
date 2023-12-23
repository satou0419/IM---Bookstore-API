import React, { useState, useEffect } from "react";
import "./BookForm.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBook,
  faCoins,
  faSearch,
  faTag,
  faUser,
} from "@fortawesome/free-solid-svg-icons";
import { CreateCategory } from "./CreateCategory";

const BookForm = () => {
  const [books, setBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [newBook, setNewBook] = useState({
    Title: "",
    Author: "",
    Price: "",
    Category: "",
  });
  const [showCategoryModal, setShowCategoryModal] = useState(false);

  useEffect(() => {
    loadBooks();
    loadCategories();
  }, []);

  useEffect(() => {
    setFilteredBooks(books);
  }, [books]);

  const loadBooks = () => {
    fetch("http://localhost:5000/books") // Update the endpoint to fetch data from the BookView
      .then((response) => response.json())
      .then((data) => {
        console.log("Books data:", data);
        setBooks(data);
      })
      .catch((error) => {
        console.error("Error fetching books:", error);
      });
  };

  const loadCategories = () => {
    fetch("http://localhost:5000/categories")
      .then((response) => response.json())
      .then((data) => {
        console.log("Categories data:", data);
        setCategories(data);
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
      });
  };

  const addBook = () => {
    fetch("http://localhost:5000/books", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newBook),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        loadBooks();
        setNewBook({
          Title: "",
          Author: "",
          Price: "",
          Category: "",
        });
      })
      .catch((error) => {
        console.error("Error adding book:", error);
      });
  };

  const updateBook = () => {
    if (!selectedBook || !selectedBook.BookID) {
      alert("Please select a book to update.");
      return;
    }

    fetch(`http://localhost:5000/books/${selectedBook.BookID}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newBook),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Update Book Response:", data);
        alert(data.message);
        loadBooks();
        setNewBook({
          Title: "",
          Author: "",
          Price: "",
          Category: "",
        });
        setSelectedBook(null);
      })
      .catch((error) => {
        console.error("Error updating book:", error);
      });
  };

  const deleteBook = (book) => {
    if (window.confirm(`Are you sure you want to delete "${book.Title}"?`)) {
      fetch(`http://localhost:5000/books/${book.BookID}`, {
        method: "DELETE",
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          loadBooks();
          setNewBook({
            Title: "",
            Author: "",
            Price: "",
            Category: "",
          });
          setSelectedBook(null);
        })
        .catch((error) => {
          console.error("Error deleting book:", error);
        });
    }
  };

  const handleRowClick = (book) => {
    setSelectedBook(book);
    setNewBook({
      Title: book.Title,
      Author: book.Author,
      Price: book.Price,
      Category: book.Category ? book.Category.CategoryName : "",
    });
  };

  const handleAddCategory = (categoryName) => {
    fetch("http://localhost:5000/categories", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ CategoryName: categoryName }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        loadCategories();
        setShowCategoryModal(false);
      })
      .catch((error) => {
        console.error("Error adding category:", error);
      });
  };

  const handleCategoryChange = (e) => {
    const selectedCategory = e.target.value;
    if (selectedCategory === "New Category") {
      setShowCategoryModal(true);
    } else {
      setNewBook({ ...newBook, Category: selectedCategory });
    }
  };

  const handleSearch = (searchText) => {
    const filtered = books.filter((book) =>
      book.Title.toLowerCase().includes(searchText.toLowerCase())
    );
    setFilteredBooks(filtered);
  };

  return (
    <>
      <section className="book--container">
        <h1>Bookstore</h1>
        <div className="content--container">
          <div className="left--container">
            <div className="icon--field">
              <FontAwesomeIcon icon={faBook} className="icon push--down" />
              <input
                type="text"
                className="input--field push--top"
                placeholder="Title"
                value={newBook.Title}
                onChange={(e) =>
                  setNewBook({ ...newBook, Title: e.target.value })
                }
              />
            </div>

            <div className="icon--field">
              <FontAwesomeIcon icon={faUser} className="icon" />
              <input
                type="text"
                className="input--field"
                placeholder="Author"
                value={newBook.Author}
                onChange={(e) =>
                  setNewBook({ ...newBook, Author: e.target.value })
                }
              />
            </div>

            <div className="icon--field">
              <FontAwesomeIcon icon={faCoins} className="icon" />
              <input
                type="number"
                className="input--field"
                placeholder="Price"
                value={newBook.Price}
                onChange={(e) =>
                  setNewBook({ ...newBook, Price: e.target.value })
                }
              />
            </div>

            <div className="icon--field">
              <FontAwesomeIcon icon={faTag} className="icon" />
              <select
                className="input--field"
                value={newBook.Category}
                onChange={handleCategoryChange}
              >
                <option value="" disabled>
                  Select Category
                </option>
                {categories.map((category, index) => (
                  <option key={index} value={category.CategoryName}>
                    {category.CategoryName}
                  </option>
                ))}
                <option value="New Category">New Category</option>
              </select>
            </div>

            <div className="btn--field">
              <button className="btn btn--add" onClick={addBook}>
                Add Book
              </button>
              <button className="btn btn--update" onClick={updateBook}>
                Update Book
              </button>
            </div>
          </div>
          <div className="right--container">
            <div className="icon--field">
              <FontAwesomeIcon icon={faSearch} className="icon" />
              <input
                type="text"
                placeholder="Search..."
                className="input--field"
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>

            <table className="book-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Author</th>
                  <th>Price</th>
                  <th>Category</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredBooks.map((book, index) => (
                  <tr
                    key={index}
                    className="table-row"
                    onClick={() => handleRowClick(book)} // Bind the function to onClick
                  >
                    <td>{book.Title}</td>
                    <td>{book.Author}</td>
                    <td>{book.Price}</td>
                    <td>{book.Category?.CategoryName || ""}</td>
                    <td
                      className="delete-icon"
                      onClick={() => deleteBook(book)}
                    >
                      🗑️
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {showCategoryModal && (
          <CreateCategory
            onClose={() => setShowCategoryModal(false)}
            onSubmit={handleAddCategory}
          />
        )}
      </section>
    </>
  );
};

export default BookForm;
