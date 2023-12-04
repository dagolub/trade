import React, { useState, useEffect } from 'react';
import { getTransaction } from '../../services/api'; // Corrected import
import Sidebar from '../../partials/Sidebar'; // Corrected import
import { useParams } from 'react-router-dom'; // Corrected import
import dayjs from "dayjs"

function TransactionEdit() {
  const { id } = useParams();

  const [from_wallet, setFromWallet] = useState('');
  const [to_wallet, setToWallet] = useState('');
  const [tx, setTx] = useState('');
  const [amount, setAmount] = useState('');
  const [currency, setCurrency] = useState('');
  const [type, setType] = useState('');
  const [created, setCreated] = useState('');
  const [deposit, setDeposit] = useState('');
  const [withdraw, setWithdraw] = useState('');

  useEffect(() => {
    getTransaction(id).then((data) => {
      setFromWallet(data.from_wallet)
      setToWallet(data.to_wallet)
      setTx(data.tx)
      setAmount(data.amount)
      setCurrency(data.currency)
      setType(data.type)
      setCreated(data.created)
      setDeposit(data.deposit_id)
      setWithdraw(data.withdraw_id)
    });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">View Transaction</h1>
            id: {id}<br />
            From wallet: {from_wallet}<br />
            To wallet: {to_wallet}<br />
            TX: {tx}<br />
            Amount: {amount}<br />
            Currency: {currency}<br />
            Type: {type}<br />
            Deposit: <a href={"/deposits/view/" + deposit} style={{"textDecoration": "underline"}}>{deposit}</a><br />
            Withdraw: <a href={"/withdraws/view/" + withdraw} style={{"textDecoration": "underline"}}>{withdraw}</a><br />
            Created: {dayjs(created).format("HH:mm:ss DD MMM YY")}
          </div>
        </main>
      </div>
    </div>
  );
}

export default TransactionEdit;
