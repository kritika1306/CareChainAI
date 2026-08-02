# CareChain — Blockchain-Powered Healthcare Staffing Platform

Full-stack platform connecting elderly patients with verified nurses.
Features a real-time booking portal, integrated payments, availability
tracking, and Ethereum smart contracts for tamper-proof nurse license
verification.

## Tech Stack
- **Backend:** Python (FastAPI), SQL (SQLite/PostgreSQL)
- **Blockchain:** Solidity, Hardhat, Ethereum (local/testnet)
- **Frontend:** React
- **Data Pipeline:** AWS Glue-style ETL with data quality checks

## Architecture
1. **Smart Contract Layer** — `NurseLicenseRegistry.sol` issues, verifies,
   and revokes nurse licenses on-chain, so credential status can't be
   silently altered by any single party.
2. **Backend API** — FastAPI service manages patients, caregivers, admins,
   bookings, and payments; calls the smart contract via web3.py before
   confirming any nurse booking.
3. **Frontend** — React app with role-based views for patients, caregivers,
   and admins.
4. **Data Pipeline** — Simulated AWS Glue job with data quality checks for
   ingesting patient/caregiver records at scale.

## Getting Started

### Smart Contracts
```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
npx hardhat node        # in one terminal
npx hardhat run scripts/deploy.js --network localhost   # in another
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## User Roles
- **Patient** — books nurses, views availability, makes payments
- **Caregiver (Nurse)** — manages availability, license verified on-chain
- **Admin** — issues/revokes licenses, oversees platform activity
