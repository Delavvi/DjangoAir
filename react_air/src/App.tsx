import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Flights from '@/(home)/flights/flights';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Flights />} />
    </Routes>
  </Router>
);

export default App;
