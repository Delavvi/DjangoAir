import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import FlightCard from '@/components/cards/flight_card';
import { FlightDetail } from "@/schemas/schema";
import { FlightSearch } from '@/components/search/FlightSearch';

const Flights = () => {
  const [details, setDetails] = useState<FlightDetail[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasNextPage, setHasNextPage] = useState(true);
  const [searchParams, setSearchParams] = useState<{ origin?: string; destination?: string; date?: string }>({});

  const fetchData = async (page: number, params: any = {}) => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({ ...params, page: page.toString() }).toString();
      const response = await axios.get(`http://localhost:8000/flights?${queryParams}`);

      if (page === 1) {
        setDetails(response.data.results);
      } else {
        setDetails((prevDetails) => {
          const existingIds = new Set(prevDetails.map((detail) => detail.id));
          const uniqueDetails = response.data.results.filter((detail) => !existingIds.has(detail.id));
          return [...prevDetails, ...uniqueDetails];
        });
      }
      setHasNextPage(response.data.next !== null);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  // При изменении searchParams загружаем данные с новыми параметрами
  useEffect(() => {
    fetchData(1, searchParams);
  }, [searchParams]);

  // При изменении страницы загружаем данные
  useEffect(() => {
    if (currentPage > 1) {
      fetchData(currentPage, searchParams);
    }
  }, [currentPage]);

  const loadMore = () => {
    if (!loading && hasNextPage) {
      setCurrentPage((prevPage) => prevPage + 1);
    }
  };

  const handleSearch = (params: { origin?: string; destination?: string; date?: string }) => {
    setSearchParams(params);
    setCurrentPage(1);
  };

  return (
    <div className="container">
      {/* SearchBar в верхней части */}
      <div className="mb-4">
        <FlightSearch
          onSearch={handleSearch} // Передаем обработчик в SearchBar
        />
      </div>

      {/* Список полетов */}
      <div className="row d-flex justify-content-center">
          {details.length === 0 && !loading ? (
            <div className="col-12 text-center">No flights found.</div>
          ) : (
            details.map((detail) => (
              <div key={detail.id} className="col-12 mb-4 d-flex justify-content-center">
                <FlightCard detail={detail} />
              </div>
            ))
          )}
      </div>

      {loading && <div className="text-center">Loading...</div>}
      {!loading && hasNextPage && (
        <div className="text-center mt-4">
          <button className="btn btn-primary" onClick={loadMore} disabled={loading}>
            Load More
          </button>
        </div>
      )}
    </div>
  );
};

export default Flights;

