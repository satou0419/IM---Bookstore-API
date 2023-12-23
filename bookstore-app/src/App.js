import "./App.css";
import AuditTrail from "./AuditTrail";
import BookForm from "./BookForm";
import { CreateCategory } from "./CreateCategory";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Outlet,
} from "react-router-dom";

import Navigation from "./Navigation";
import CategoryList from "./CategoryList";

function App() {
  return (
    // <CreateCategory />
    <Router>
      <Routes>
        <Route path="/" element={<Navigation />}>
          {/* Use the Outlet to render nested routes */}
          <Route path="/" element={<BookForm />} />

          <Route path="/book" element={<BookForm />} />
          <Route path="/audit-trail" element={<AuditTrail />} />
          <Route path="/category-list" element={<CategoryList />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
