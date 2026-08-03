import { useState } from "react";
import { verifyNurse } from "../api";

export default function NurseVerification() {
  const [nurseId, setNurseId] = useState("");
  const [result, setResult] = useState(null);

  const handleCheck = async () => {
    const res = await verifyNurse(nurseId);
    setResult(res.data);
  };

  return (
    <div>
      <h2>Verify Nurse License</h2>
      <input
        value={nurseId}
        onChange={(e) => setNurseId(e.target.value)}
        placeholder="Nurse ID"
      />
      <button onClick={handleCheck}>Verify</button>
      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}
