import React, { useState, useEffect, useCallback, ChangeEvent } from 'react';
import { City } from "@/schemas/schema";

interface CityAutocompleteProps {
  label: string;
  initialPlaceholder?: string;
  onSelectCity: (city: City) => void;
}

const debounce = (fn: (...args: any[]) => void, delay: number) => {
  let timeoutId: number;
  return (...args: any[]) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = window.setTimeout(() => fn(...args), delay);
  };
};

export const CityAutocomplete: React.FC<CityAutocompleteProps> = ({
  label,
  initialPlaceholder,
  onSelectCity,
}) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<City[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [placeholder, setPlaceholder] = useState(initialPlaceholder || '');

  const fetchCities = useCallback(
    debounce(async (val: string) => {
      if (!val) {
        setSuggestions([]);
        return;
      }
      try {
        const response = await fetch(`http://localhost:8000/cities?name=${encodeURIComponent(val)}`);
        if (response.ok) {
          const data: City[] = await response.json();
          setSuggestions(data);
          setShowSuggestions(true);
        } else {
          console.error('Failed to fetch cities');
        }
      } catch (error) {
        console.error(error);
      }
    }, 300),
    []
  );

  useEffect(() => {
    fetchCities(query);
  }, [query, fetchCities]);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  const handleFocus = () => {
    setPlaceholder('Start typing to search...');
    if (query) setShowSuggestions(true);
  };

  const handleBlur = () => {
    setTimeout(() => setShowSuggestions(false), 200);
    setPlaceholder(initialPlaceholder || '');
  };

  const handleSelect = (city: City) => {
    console.log('handleSelect called with:', city);
    setQuery(city.name);
    setSuggestions([]);
    setShowSuggestions(false);
    onSelectCity(city);
  };

  return (
    <div className="form-group position-relative" style={{ marginBottom: '1rem' }}>
      <label>{label}</label>
      <input
        type="text"
        className="form-control"
        placeholder={placeholder}
        value={query}
        onChange={handleChange}
        onFocus={handleFocus}
        onBlur={handleBlur}
      />
      {showSuggestions && suggestions.length > 0 && (
        <ul
          className="list-group position-absolute w-100"
          style={{
            zIndex: 1000,
            top: '100%',
            left: 0,
            maxHeight: '200px',
            overflowY: 'auto',
          }}
        >
          {suggestions.map((city) => (
            <li
              key={city.id}
              className="list-group-item list-group-item-action"
              style={{ cursor: 'pointer' }}
              onMouseDown={() => handleSelect(city)}
            >
              {city.name} ({city.country.name})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

