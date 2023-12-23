import React, { useState, useEffect } from "react";
import "./AuditTrail.css";

// ... (other imports and code)

export default function AuditTrail() {
  const [originalEntries, setOriginalEntries] = useState([]);
  const [filteredEntries, setFilteredEntries] = useState([]);

  const loadAuditTrail = () => {
    fetch("http://localhost:5000/audit-logs")
      .then((response) => response.json())
      .then((data) => {
        console.log("Audit Trail data:", data);
        setOriginalEntries(data);
        setFilteredEntries(data);
      })
      .catch((error) => {
        console.error("Error fetching audit trail:", error);
      });
  };

  // Use loadAuditTrail in useEffect
  useEffect(() => {
    loadAuditTrail();
  }, []);

  const handleSearch = (searchText) => {
    const filtered = originalEntries.filter((entry) =>
      entry.Message.toLowerCase().includes(searchText.toLowerCase())
    );
    setFilteredEntries(filtered);
  };

  return (
    <section className="book--container">
      <h1>Audit</h1>

      <div className="audit--container">
        <div className="right--container">
          <div className="icon--field">
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
                <th>ID</th>
                <th>Message</th>
                <th>Object Type</th>
                <th>Object ID</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map((entry, index) => (
                <tr key={index}>
                  <td>{entry.ID}</td>
                  <td>{entry.Message}</td>
                  <td>{entry["Object Type"]}</td>
                  <td>{entry["Object ID"]}</td>
                  <td>{entry.Date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
