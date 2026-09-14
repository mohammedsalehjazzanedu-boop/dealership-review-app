import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import "./DealerDetails.css";

const API_BASE = "http://localhost:1258";

const DealerDetails = () => {
    const { id } = useParams();
    const [dealer, setDealer] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [username] = useState(sessionStorage.getItem("username") || "");

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

        const fetchReviews = async () => {
            try {
                const res = await fetch(`${API_BASE}/djangoapp/reviews/dealer/${id}`);
                const json = await res.json();
                setReviews(json.reviews || []);
            } catch (error) {
                console.error("Error fetching reviews:", error);
            }
        };

        fetchDealer();
        fetchReviews();
    }, [id]);

    if (!dealer) {
        return <p className="loading-text">جارٍ التحميل...</p>;
    }

    return (
        <div className="dealer-details-container">
            <nav className="details-nav">
                <Link to="/" className="back-link">&larr; رجوع للرئيسية</Link>
                <div className="logo">Dealership Review</div>
            </nav>

            <div className="dealer-header">
                <h1>{dealer.name}</h1>
                <p>{dealer.address}, {dealer.city}, {dealer.state} {dealer.zip_code}</p>

                {username && (
                    <Link to={`/postreview/${dealer.id}`} className="add-review-btn">
                        Post Review
                    </Link>
                )}
            </div>

            <div className="reviews-section">
                <h2>التقييمات ({reviews.length})</h2>

                {reviews.length === 0 && (
                    <p className="no-reviews">لا يوجد تقييمات بعد لهذا المعرض.</p>
                )}

                <div className="reviews-list">
                    {reviews.map((review) => (
                        <div className="review-card" key={review.id}>
                            <div className="review-header">
                                <strong>{review.name}</strong>
                                {review.sentiment && (
                                    <span className={`sentiment-badge ${review.sentiment}`}>
                                        {review.sentiment}
                                    </span>
                                )}
                            </div>
                            <p className="review-text">{review.review}</p>
                            {review.car_make && (
                                <p className="car-info">
                                    🚗 {review.car_make} {review.car_model} {review.car_year}
                                </p>
                            )}
                            <p className="review-date">{review.purchase_date}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default DealerDetails;
