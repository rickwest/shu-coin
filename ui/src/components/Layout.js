import React from "react";
import logo from "../assets/logo.png";
import { Link } from "react-router-dom";

function Layout({ children }) {
  return (
    <div className="container p-3 text-center text-break">
      <div className="row justify-content-center">
        <div className="col-md-auto">
          <img className="img-fluid" src={logo} alt="SHUcoin logo" />
          <div className="mt-4 mb-4">
            <ul className="nav justify-content-center border-bottom mb-4">
                <li className="nav-item">
                <Link className="nav-link" to="/">
                  Home
                </Link>
              </li>
                <li className="nav-item">
                <Link className="nav-link" to="/blockchain">
                  Blockchain Explorer
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/transaction/new">
                  New Transaction
                </Link>
              </li>
            </ul>

            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Layout;
