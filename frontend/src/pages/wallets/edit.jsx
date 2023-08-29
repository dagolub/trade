import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../../partials/Sidebar';
import Form from '../../components/wallets/form';
import { getWallet } from '../../services/api';

function WalletEdit() {
  const { id } = useParams();
  const [wallet, setWallet] = useState('');
  const [type, setType] = useState('');

  useEffect(() => {
    getWallet(id)
      .then((data) => {
        setWallet(data.wallet); // Use lowercase variable names here
        setType(data.type);     // Use lowercase variable names here
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
            <Form
              wallet={wallet}
              type={type}
              id={id}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default WalletEdit;
