import React from "react";
import {NavLink} from "react-router-dom";

export default function Navigation() {
    return (
        <div className="navigation">
            <nav className="navbar navbar-expand navbar-dark bg-dark">
                <div className="container-fluid">
                    <NavLink className="navbar-brand" to="/">
                        My App
                    </NavLink>
                    <div className="collapse navbar-collapse">
                        <div className="navbar-nav">
                            <NavLink className="nav-link" to="/">
                                Home
                            </NavLink>
                            <NavLink className="nav-link" to="/n-gram-metrics">
                                N-Gram Metrics
                            </NavLink>
                            <NavLink className="nav-link" to="/pos-tagger">
                                POS Tagger
                            </NavLink>
                            <NavLink className="nav-link" to="/sentence-trees">
                                Sentence Trees
                            </NavLink>
                            <NavLink className="nav-link" to="/stm">
                                Subtree Metric
                            </NavLink>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
    )
}
