import React, { useState } from 'react';
import { CityAutocomplete } from './CityAutocomplete';
import { City } from "@/schemas/schema";

interface FlightSearchProps {
  onSearch: (params: { origin?: string; destination?: string; date?: string }) => void;
}

export const FlightSearch: React.FC<FlightSearchProps> = ({ onSearch }) => {
  const [originCity, setOriginCity] = useState<City | null>(null);
  const [destinationCity, setDestinationCity] = useState<City | null>(null);
  const [date, setDate] = useState('');

  const handleOriginSelect = (city: City) => {
    setOriginCity(city);
  };

  const handleDestinationSelect = (city: City) => {
    setDestinationCity(city);
  };

  const handleSearch = () => {
    if (!originCity || !destinationCity || !date) {
      alert('Please select origin, destination, and date.');
      return;
    }

    onSearch({
      origin: originCity.name,
      destination: destinationCity.name,
      date,
    });
  };

  return (
    <div className="container my-4">
      <div className="d-flex flex-wrap justify-content-between align-items-center bg-primary text-white p-3 rounded">
        {/* Origin City */}
        <div className="p-2">
          <CityAutocomplete
            label="Origin City"
            initialPlaceholder="Enter origin"
            onSelectCity={handleOriginSelect}
          />
        </div>

        {/* Destination City */}
        <div className="p-2">
          <CityAutocomplete
            label="Destination City"
            initialPlaceholder="Enter destination"
            onSelectCity={handleDestinationSelect}
          />
        </div>

        {/* Date Picker */}
        <div className="p-2">
          <div className="form-group">
            <label>Date of Flight</label>
            <input
              type="date"
              className="form-control"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
            />
          </div>
        </div>

        {/* Search Button */}
        <div className="p-2">
          <button className="btn btn-light w-100" onClick={handleSearch}>
            Search Flights
          </button>
        </div>
      </div>
    </div>
  );
};



