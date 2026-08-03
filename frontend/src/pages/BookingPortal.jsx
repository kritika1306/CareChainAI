import { useEffect, useState } from "react";
import { getOpenAvailability, createBooking, verifyNurse } from "../api";

export default function BookingPortal({ patientId }) {
  const [slots, setSlots] = useState([]);
  const [verifiedStatus, setVerifiedStatus] = useState({});
  const [message, setMessage] = useState("");

  useEffect(() => {
    getOpenAvailability().then((res) => setSlots(res.data));
  }, []);

  const checkVerification = async (caregiverId) => {
    const res = await verifyNurse(caregiverId);
    setVerifiedStatus((prev) => ({ ...prev, [caregiverId]: res.data.license_valid }));
  };

  const bookSlot = async (slot) => {
    try {
      await createBooking({
        patient_id: patientId,
        caregiver_id: slot.caregiver_id,
        availability_id: slot.id,
      });
      setMessage(`Booking confirmed for slot ${slot.id}`);
      setSlots((prev) => prev.filter((s) => s.id !== slot.id));
    } catch (err) {
      setMessage(err.response?.data?.detail || "Booking failed");
    }
  };

  return (
    <div>
      <h2>Available Caregivers</h2>
      {message && <p>{message}</p>}
      <ul>
        {slots.map((slot) => (
          <li key={slot.id}>
            Caregiver #{slot.caregiver_id} — {slot.start_time} to {slot.end_time}
            <button onClick={() => checkVerification(slot.caregiver_id)}>
              Check License
            </button>
            {verifiedStatus[slot.caregiver_id] !== undefined && (
              <span>
                {verifiedStatus[slot.caregiver_id] ? " ✅ Verified" : " ❌ Not Verified"}
              </span>
            )}
            <button onClick={() => bookSlot(slot)}>Book</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
