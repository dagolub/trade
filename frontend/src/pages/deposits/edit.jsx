import React, { useEffect, useState } from 'react';
import { getDeposit } from '../../services/api';
import Header from '../../partials/Header';
import Sidebar from '../../partials/Sidebar';
import Form from '../../components/deposits/form'; // Make sure to import your Form component

function DepositEdit() {
  const { id } = useParams();

  const [wallet, setWallet] = useState("");
  const [type, setType] = useState("");
  const [sum, setSum] = useState("");
  const [currency, setCurrency] = useState("");
  const [status, setStatus] = useState("");
  const [callback, setCallback] = useState("");
  const [callback_response, setCallbackResponse] = useState("");

  useEffect(() => {
    getDeposit(id).then((data) => {
      setWallet(data.wallet);
      setType(data.type);
      setSum(data.sum);
      setCurrency(data.currency);
      setStatus(data.status);
      setCallback(data.callback);
      setCallbackResponse(data.callback_response);
    });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form
              wallet={wallet}
              type={type}
              sum={sum}
              currency={currency}
              status={status}
              callback={callback}
              callback_response={callback_response}
              id={id}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default DepositEdit;
