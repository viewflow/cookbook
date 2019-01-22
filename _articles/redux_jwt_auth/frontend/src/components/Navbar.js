import React from 'react'
import { NavLink } from 'react-router-dom'

const Navbar = () => (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <NavLink
            to="/"
            className="navbar-brand"
            activeClassName="active">
            Home
        </NavLink>
        <div className="collapse navbar-collapse">
            <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                    <NavLink
                        to="/companies"
                        className="nav-link"
                        activeClassName="active">
                        Companies
                    </NavLink>
                </li>
                <li>
                    <NavLink
                        to="/about"
                        className="nav-link"
                        activeClassName="active">
                        About
                    </NavLink>
                </li>
            </ul>
        </div>
    </nav>
)


export default Navbar