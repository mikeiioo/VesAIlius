import React, { useState } from "react";
import "./Navbar.css"; // Import your CSS file for styling

const Navbar = () => {
  const [isSidebarVisible, setSidebarVisible] = useState(false);

  const showSidebar = () => {
    setSidebarVisible(true);
  };

  const hideSidebar = () => {
    setSidebarVisible(false);
  };

  return (
    <nav>
      <ul className={`LGNavBar ${isSidebarVisible ? "visible" : ""}`}>
        <li id="closer" onClick={hideSidebar}>
          <a href="#">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="29px"
              viewBox="0 -960 960 960"
              width="29px"
              fill="#000000"
            >
              <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z" />
            </svg>
          </a>
        </li>
        <li>
          <a href="#">Home</a>
        </li>
        <li>
          <a href="#">Previous Outages</a>
        </li>
        <li>
          <a href="#">Login</a>
        </li>
      </ul>

      <button id="menu-toggle" className="menu-button" onClick={showSidebar}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="45px"
          viewBox="0 -960 960 960"
          width="45px"
          fill="#000000"
        >
          <path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z" />
        </svg>
      </button>
    </nav>
  );
};

export default Navbar;
