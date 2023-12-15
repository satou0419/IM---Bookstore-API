import React, { useState } from "react";
import "./CreateCategory.css";

export function CreateCategory({ onClose, onSubmit }) {
  const [newCategory, setNewCategory] = useState("");

  const handleInputChange = (e) => {
    setNewCategory(e.target.value);
  };

  const handleAddCategory = () => {
    onSubmit(newCategory);
    setNewCategory("");
    onClose();
  };

  return (
    <section className="wrapper">
      <section className="category--container">
        <h1>Create Category</h1>
        <div className="category--form">
          <input
            type="text"
            className="input--category"
            placeholder="Category Name"
            value={newCategory}
            onChange={handleInputChange}
          />
          <button className="btn--add" onClick={handleAddCategory}>
            Add
          </button>
        </div>
      </section>
    </section>
  );
}
