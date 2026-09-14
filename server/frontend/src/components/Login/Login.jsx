import React, { useState } from "react";
import "./Login.css";

const API_BASE = "http://localhost:1258";

const Login = () => {
    const [formData, setFormData] = useState({ username: "", password: "" });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch(`${API_BASE}/djangoapp/login`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    userName: formData.username,
                    password: formData.password,
                }),
            });

            const json = await res.json();

            if (json.status === "Authenticated") {
                sessionStorage.setItem("username", json.userName);
                window.location.href = "/";
            } else {
                alert("اسم المستخدم أو كلمة المرور غير صحيحة.");
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("تعذر الاتصال بالسيرفر.");
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>تسجيل الدخول</h2>

                <label htmlFor="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />

                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;

