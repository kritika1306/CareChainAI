import { useEffect, useState } from "react";
import api from "../api";

export default function AdminDashboard() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    // Example: replace with a real admin-scoped endpoint as the API grows
    api.get("/bookings/patient/1").then((res) => setBookings(res.data));
  }, []);

  return (
    <div>
      <h2>Admin Dashboard</h2>
      <table>
        <thead>
          <tr>
            <th>Booking ID</th>
            <th>Patient</th>
            <th>Caregiver</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {bookings.map((b) => (
            <tr key={b.id}>
              <td>{b.id}</td>
              <td>{b.patient_id}</td>
              <td>{b.caregiver_id}</td>
              <td>{b.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
