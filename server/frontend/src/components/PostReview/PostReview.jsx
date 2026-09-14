import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./PostReview.css";

const API_BASE = "http://localhost:1258";

const PostReview = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [dealer, setDealer] = useState(null);
    const [carModels, setCarModels] = useState([]);
    const [formData, setFormData] = useState({
        review: "",
        purchase: false,
        purchase_date: "",
        car_make: "",
        car_model: "",
        car_year: "",
    });

    useEffect(() => {
        const fetchDealer = async () => {
            try {
                const res = await fetch(`${API_BASE}/djangoapp/dealer/${id}`);
                const json = await res.json();
                setDealer(json.dealer);
            } catch (error) {
                console.error("Error fetching dealer:", error);
            }
        };

        const fetchCarModels = async () => {
            try {
                const res = await fetch(`${API_BASE}/djangoapp/carmakes`);
                const json = await res.json();
                const flatModels = [];
                (json.CarModels || []).forEach((make) => {
                    (make.models || []).forEach((model) => {
                        flatModels.push({
                            makeName: make.name,
                            modelName: model.name,
                            year: model.year,
                        });
                    });
                });
                setCarModels(flatModels);
            } catch (error) {
                console.error("Error fetching car models:", error);
            }
        };

        fetchDealer();
        fetchCarModels();
    }, [id]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === "checkbox" ? checked : value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch(`${API_BASE}/djangoapp/review/add`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    dealer_id: id,
                    review: formData.review,
                    purchase: formData.purchase,
                    car_make: formData.car_make,
                    car_model: formData.car_model,
                    car_year: formData.car_year ? parseInt(formData.car_year) : null,
                }),
            });

            const json = await res.json();

            if (json.status === 200) {
                navigate(`/dealer/${id}`);
            } else {
                alert("لم يتم حفظ التقييم. تأكد أنك مسجّل دخول.");
            }
        } catch (error) {
            console.error("Error submitting review:", error);
            alert("تعذر الاتصال بالسيرفر.");
        }
    };

    if (!dealer) {
        return <p className="loading-text">جارٍ التحميل...</p>;
    }

    return (
        <div className="post-review-container">
            <nav className="post-review-nav">
                <div className="logo">Dealership Review</div>
            </nav>

            <div className="post-review-card">
                <h2>إضافة تقييم لـ {dealer.name}</h2>

                <form onSubmit={handleSubmit}>
                    <label htmlFor="review">التقييم</label>
                    <textarea
                        id="review"
                        name="review"
                        rows="4"
                        value={formData.review}
                        onChange={handleChange}
                        required
                    />

                    <div className="checkbox-row">
                        <input
                            type="checkbox"
                            id="purchase"
                            name="purchase"
                            checked={formData.purchase}
                            onChange={handleChange}
                        />
                        <label htmlFor="purchase">قمت بشراء سيارة من هذا المعرض</label>
                    </div>

                    <label htmlFor="car_make">ماركة السيارة</label>
                    <select
                        id="car_make"
                        name="car_make"
                        value={formData.car_make}
                        onChange={handleChange}
                    >
                        <option value="">-- اختر --</option>
                        {[...new Set(carModels.map((m) => m.makeName))].map((make) => (
                            <option key={make} value={make}>
                                {make}
                            </option>
                        ))}
                    </select>

                    <label htmlFor="car_model">موديل السيارة</label>
                    <input
                        type="text"
                        id="car_model"
                        name="car_model"
                        value={formData.car_model}
                        onChange={handleChange}
                    />

                    <label htmlFor="car_year">سنة الصنع</label>
                    <input
                        type="number"
                        id="car_year"
                        name="car_year"
                        value={formData.car_year}
                        onChange={handleChange}
                    />

                    <button type="submit">Post Review</button>
                </form>
            </div>
        </div>
    );
};

export default PostReview;
