import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import BookingPortal from "./pages/BookingPortal";
import NurseVerification from "./pages/NurseVerification";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Booking</Link> | <Link to="/verify">Verify Nurse</Link> |{" "}
        <Link to="/admin">Admin</Link>
      </nav>
      <Routes>
        <Route path="/" element={<BookingPortal patientId={1} />} />
        <Route path="/verify" element={<NurseVerification />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
