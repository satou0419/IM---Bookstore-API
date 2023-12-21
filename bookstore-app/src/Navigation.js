import { Link, Outlet } from "react-router-dom";
import "./Navigation.css";

export default function Navigation() {
  return (
    <section>
      <nav>
        <ul>
          <Link to="/book">
            <li>Books</li>
          </Link>
          <Link to="/category-list">
            <li>Categories</li>
          </Link>
          <Link to="/audit-trail">
            <li>Audit Trail</li>
          </Link>
        </ul>
      </nav>

      <section className="content">
        <Outlet />
      </section>
    </section>
  );
}
