import React, { useState, useEffect } from 'react';
import { getTransaction } from '../../services/api'; // Corrected import
import Sidebar from '../../partials/Sidebar'; // Corrected import
import { useParams } from 'react-router-dom'; // Corrected import
import Form from '../../components/transactions/form'; // Corrected import

function TransactionEdit() {
  const { id } = useParams();

  const [from_wallet, setFromWallet] = useState('');
  const [to_wallet, setToWallet] = useState('');
  const [tx, setTx] = useState('');
  const [amount, setAmount] = useState('');
  const [currency, setCurrency] = useState('');
  const [type, setType] = useState('');

  useEffect(() => {
    getTransaction(id).then((data) => {
      setFromWallet(data.from_wallet);
      setToWallet(data.to_wallet);
      setTx(data.tx);
      setAmount(data.amount);
      setCurrency(data.currency);
      setType(data.type);
    });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form
              from_wallet={from_wallet}
              to_wallet={to_wallet}
              tx={tx}
              amount={amount}
              currency={currency}
              type={type}
              id={id}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default TransactionEdit;
