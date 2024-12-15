import React, { useState } from "react";
import axios from 'axios';
import { FlightDetail } from "@/schemas/schema";

const FlightCard = ({ detail }: { detail: FlightDetail }) => {
  const modalId = `flightDetailModal${detail.id}`;

  // State to store additional flight details
  const [flightDetails, setFlightDetails] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  // Function to fetch additional details from the API
  const fetchAdditionalDetails = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/flights/${detail.id}`);
      const data = await response.data;
      setFlightDetails(data);
    } catch (error) {
      console.error("Error fetching flight details:", error);
    } finally {
      setLoading(false);
    }
  };

      const renderService = (service) => {
          const { name, meal, baggage } = service.service;
          console.log(name);
          return (
            <li key={service.service.id}>
              <strong>{name}</strong>
              <div>
                <span>Meal: {meal.name}</span>
              </div>
              <div>
                <span>Baggage: </span>
                <span>Weight - {baggage.max_weight}</span>,
                <span> Width - {baggage.width}</span>,
                <span> Height - {baggage.height}</span>
              </div>
            </li>
          );
        };

  return (
    <div className="card" style={{ width: "100%", height: "200px" }}>
      <div className="card-body d-flex flex-column justify-content-center">
        <p className="card-text">
          {detail.origin.name} - {detail.destination.name}
        </p>
        <p className="card-text">
          {detail.origin_airport.name} - {detail.destination_airport.name}
        </p>
        <p className="card-text">
          {new Date(detail.date_of_flight).toLocaleString()} -{" "}
          {new Date(detail.arriving_date).toLocaleString()}
        </p>
        {/* Button to open the modal */}
        <button
          className="btn btn-primary mt-3"
          data-bs-toggle="modal"
          data-bs-target={`#${modalId}`}
          onClick={fetchAdditionalDetails} // Fetch details on open
        >
          More Details
        </button>
      </div>

      {/* Unique Modal */}
      <div
        className="modal fade"
        id={modalId}
        tabIndex={-1}
        aria-labelledby={`${modalId}Label`}
        aria-hidden="true"
      >
        <div className="modal-dialog modal-lg">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id={`${modalId}Label`}>
                Flight Details
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">
              {/* Display loading state or fetched data */}
              {loading ? (
                <p>Loading...</p>
              ) : flightDetails ? (
                <div>
                  <p>
                    <strong>Additional Information:</strong> {flightDetails.origin.name} - {flightDetails.destination.name}
                    <strong>Additional Information:</strong> {flightDetails.origin_airport.name} - {flightDetails.destination.name}
                  </p>
                  <p>
                    <strong>Economy price:</strong> ${flightDetails.base_seat_price}
                    <strong>First class price:</strong> ${flightDetails.first_class_seat_price}
                    <strong>Business price:</strong> ${flightDetails.business_seat_price}
                  </p>
                  <p>
                    <strong>Duration:</strong> {flightDetails.date_of_flight} - {flightDetails.arriving_date}
                  </p>
                  <div>
                    <strong>Available Services:</strong>
                    {flightDetails.available_services?.length > 0 && (
                        <ul>
                          {flightDetails && flightDetails.available_services && flightDetails.available_services.map(service => renderService(service))}
                        </ul>
                    )}
                  </div>
                </div>
              ) : (
                <p>Failed to load flight details.</p>
              )}
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FlightCard;

