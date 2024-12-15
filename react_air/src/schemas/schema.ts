export type Country = {
        id: string;
        name: string;
    }

export type FlightSchema = {
  id: number;
  origin_airport: string;
  destination_airport: string;
  origin: string;
  destination: string;
  date_of_flight: string;
  arriving_date: string;
};

export type City {
  id: string;
  name: string;
  country: Country
}