import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const API_BASE = "";

const Home = () => {
    const [dealers, setDealers] = useState([]);
    const [states, setStates] = useState([]);
    const [selectedState, setSelectedState] = useState("All");
    const [username, setUsername] = useState(sessionStorage.getItem("username") || "");

    const fetchDealers = async (state = "All") => {
        try {
            const url =
                state === "All"
                    ? `${API_BASE}/djangoapp/dealers`
                    : `${API_BASE}/djangoapp/dealers/state/${state}`;

            const res = await fetch(url);
            const json = await res.json();
            setDealers(json.dealers || []);
        } catch (error) {
            console.error("Error fetching dealers:", error);
        }
    };

    const fetchAllDealersForStates = async () => {
        try {
            const res = await fetch(`${API_BASE}/djangoapp/dealers`);
            const json = await res.json();
            const uniqueStates = [
                ...new Set((json.dealers || []).map((d) => d.state)),
            ];
            setStates(uniqueStates);
        } catch (error) {
            console.error("Error fetching states:", error);
        }
    };

    useEffect(() => {
        fetchDealers();
        fetchAllDealersForStates();
    }, []);

    const handleStateChange = (e) => {
        const state = e.target.value;
        setSelectedState(state);
        fetchDealers(state);
    };

    const handleLogout = async () => {
        await fetch(`${API_BASE}/djangoapp/logout`, { credentials: "include" });
        sessionStorage.removeItem("username");
        setUsername("");
        window.location.reload();
    };

    return (
        <div className="home-container">
            <nav className="home-nav">
                <div className="logo">Dealership Review</div>
                <div className="nav-right">
                    {username ? (
                        <>
                            <span className="username-display">
                                مرحباً، {username}
                            </span>
                            <button onClick={handleLogout} className="nav-btn">
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="nav-btn">
                                Login
                            </Link>
                            <Link to="/register" className="nav-btn">
                                Register
                            </Link>
                        </>
                    )}
                </div>
            </nav>

            <div className="filter-bar">
                <label htmlFor="state-filter">فلترة حسب الولاية:</label>
                <select
                    id="state-filter"
                    value={selectedState}
                    onChange={handleStateChange}
                >
                    <option value="All">All States</option>
                    {states.map((state) => (
                        <option key={state} value={state}>
                            {state}
                        </option>
                    ))}
                </select>
            </div>

            <div className="dealers-grid">
                {dealers.length === 0 && (
                    <p className="no-dealers">لا يوجد معارض لعرضها.</p>
                )}

                {dealers.map((dealer) => (
                    <Link
                        to={`/dealer/${dealer.id}`}
                        key={dealer.id}
                        className="dealer-card"
                    >
                        <h3>{dealer.name}</h3>
                        <p>{dealer.city}, {dealer.state}</p>
                        <p className="zip">Zip: {dealer.zip_code}</p>
                        {username && (
                            <span className="review-link">Review Dealer</span>
                        )}
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default Home;

