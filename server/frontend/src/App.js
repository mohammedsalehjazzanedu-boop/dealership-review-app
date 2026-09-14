import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home/Home";
import Login from "./components/Login/Login";
import Register from "./components/Register/Register";
import DealerDetails from "./components/DealerDetails/DealerDetails";
import PostReview from "./components/PostReview/PostReview";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dealer/:id" element={<DealerDetails />} />
                <Route path="/postreview/:id" element={<PostReview />} />
            </Routes>
        </Router>
    );
}

export default App;