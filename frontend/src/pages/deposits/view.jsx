import React, { useEffect, useState } from 'react';
import { getDeposit } from '../../services/api';
import Header from '../../partials/Header';
import Sidebar from '../../partials/Sidebar';// Make sure to import your Form component
import { useParams } from 'react-router-dom';
import dayjs from "dayjs";
function DepositView() {
  const { id } = useParams();

  const [wallet, setWallet] = useState("");
  const [type, setType] = useState("");
  const [sum, setSum] = useState("");
  const [currency, setCurrency] = useState("");

  const [callback, setCallback] = useState("");
  const [callback_response, setCallbackResponse] = useState("");
  const [created, setCreated] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    getDeposit(id).then((data) => {
      setWallet(data.wallet);
      setType(data.type);
      setSum(data.sum);
      setCurrency(data.currency);
      setCallback(data.callback);
      setCallbackResponse(data.callback_response);
      setStatus(data.status);
      setCreated(data.created)
    });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">View Deposit</h1>
            id: {id}
            Wallet: {wallet}<br />
            Type: {type}<br />
            Sum: {sum}<br />
            Currency: {currency}<br />
            Callback: {callback}<br />
            Callback Response: {callback_response}
            Status: {status}<br />
            Created: {dayjs(created).format("HH:mm:ss DD MMM YY")}
          </div>
        </main>
      </div>
    </div>
  );
}

export default DepositView;
