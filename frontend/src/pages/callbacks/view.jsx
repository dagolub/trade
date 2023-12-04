import React from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../../partials/Sidebar';
import { getCallback } from '../../services/api';
import dayjs from "dayjs"
function WalletView() {
  const { id } = useParams();
  const [callback, setCallback] = React.useState('');
  const [callback_response, setCallbackResponse] = React.useState('');
  const [deposit, setDeposit] = React.useState('');
  const [withdraw, setWithdraw] = React.useState('');

  const [created, setCreated] = React.useState('');

  React.useEffect(() => {
    getCallback(id)
      .then((data) => {
        setCallback(data.callback)
        setCallbackResponse(data.callback_response)
        setDeposit(data.deposit_id)
        setWithdraw(data.withdraw_id)
        setCreated(data.created)
      })
      .catch((error) => {
        console.error('Error fetching wallet:', error);
      });
  }, [id])

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
              <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">View Wallet</h1>
              id: {id}<br />
              Callback: {callback}<br />
              Callback Response: {callback_response}<br />
              Deposit: <a href={"/deposits/view/" + deposit} style={{"textDecoration": "underline"}}>{deposit}</a><br />
              Withdraw: <a href={"/withdraws/view/" + withdraw} style={{"textDecoration": "underline"}}>{withdraw}</a><br />
              Created: {dayjs(created).format("HH:mm:ss DD MMM YY")}
          </div>
        </main>
      </div>
    </div>
  );
}

export default WalletView;
