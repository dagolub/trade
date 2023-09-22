import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../../partials/Sidebar';
import { getWallet } from '../../services/api';
import dayjs from "dayjs"
function WalletView() {
  const { id } = useParams();
  const [wallet, setWallet] = useState('');
  const [type, setType] = useState('');
  const [created, setCreated] = useState('');

  useEffect(() => {
    getWallet(id)
      .then((data) => {
          console.log(data)
        setWallet(data.wallet); // Use lowercase variable names here
        setType(data.type);     // Use lowercase variable names here
        setCreated(data.created);     // Use lowercase variable names here
      })
      .catch((error) => {
        console.error('Error fetching wallet:', error);
      });
  }, [id]); // Make sure to include 'id' in the dependency array

  return (
    <div className="flex h-[100vh] overflow-hidden"> {/* Fixed typo in height */}
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
              <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">View Wallet</h1>
              id: {id}<br />
              Wallet: {wallet}<br />
              Type: {type}<br />
              Created: {dayjs(created).format("HH:mm:ss DD MMM YY")}
          </div>
        </main>
      </div>
    </div>
  );
}

export default WalletView;
