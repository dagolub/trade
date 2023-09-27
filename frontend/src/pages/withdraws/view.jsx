import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../../partials/Sidebar';
import {getWithdraw} from '../../services/api';
import dayjs from "dayjs"
function WithdaraView() {
  const { id } = useParams();
  const [sum, setSum] = useState('');
  const [to, setTo] = useState('');
  const [currency, setCurrency] = useState('');
  const [chain, setChain] = useState('');
  const [status, setStatus] = useState('');
  const [created, setCreated] = useState('');

  useEffect(() => {
    getWithdraw(id)
      .then((data) => {
        setSum(data.sum); // Use lowercase variable names here
        setTo(data.to);     // Use lowercase variable names here
        setCurrency(data.currency);     // Use lowercase variable names here
        setChain(data.chain);     // Use lowercase variable names here
        setStatus(data.status);     // Use lowercase variable names here
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
              <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">View Withdraw</h1>
              id: {id}<br />
              Sum: {sum}<br />
              To: {to}<br />
              Currency: {currency}<br />
              Chain: {chain}<br />
              Status: {status}<br />
              Created: {dayjs(created).format("HH:mm:ss DD MMM YY")}
          </div>
        </main>
      </div>
    </div>
  );
}

export default WithdaraView;
