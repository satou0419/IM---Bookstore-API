import React, { useState, useEffect } from "react";
import "./CategoryList.css";

export default function CategoryList() {
  const [categoryStats, setCategoryStats] = useState([]);
  const [searchText, setSearchText] = useState("");

  useEffect(() => {
    // Fetch category statistics when the component mounts
    fetch("http://localhost:5000/category-stats")
      .then((response) => response.json())
      .then((data) => {
        console.log("Category Stats:", data);
        setCategoryStats(data);
      })
      .catch((error) => {
        console.error("Error fetching category statistics:", error);
      });
  }, []); // The empty dependency array ensures that the effect runs only once

  const handleSearch = (e) => {
    setSearchText(e.target.value);
  };

  const filteredCategories = categoryStats.filter((category) =>
    category.CategoryName.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <section className="book--container">
      <h1>Category List</h1>

      <div className="categorylist--container">
        <div className="right--container">
          <div className="icon--field">
            <input
              type="text"
              placeholder="Search..."
              className="input--field"
              value={searchText}
              onChange={handleSearch}
            />
          </div>

          <table className="book-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Total Books</th>
                <th>Date Created</th>
              </tr>
            </thead>
            <tbody>
              {filteredCategories.map((category, index) => (
                <tr key={index}>
                  <td>{category.CategoryName}</td>
                  <td>{category.TotalBooks}</td>
                  <td>{category.CreationDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
