import React, { useRef, useEffect } from 'react';
import { createDeposit, updateDeposit } from '../../services/api'; // Correct path to your API service

function Form({
  wallet = "",
  type = "",
  sum = "",
  currency = "",
  status = "",
  callback = "",
  callback_response = "",
  id = ""
}) {
  const refWallet = useRef("");
  const refType = useRef("");
  const refSum = useRef("");
  const refCurrency = useRef("");
  const refStatus = useRef("");
  const refCallback = useRef("");
  const refCallbackResponse = useRef("");

  const setResp = (resp) => {
    if (resp.wallet === refWallet.current.value) {
      window.location.href = "/deposits/list";
    } else {
      alert(resp.response.data.detail);
    }
  };

  const submitHandler = async (e) => {
    e.preventDefault();

    if (id) {
      const r = await updateDeposit(
        id,
        refWallet.current.value,
        refType.current.value,
        refSum.current.value,
        refCurrency.current.value,
        refStatus.current.value,
        refCallback.current.value
      );
      setResp(r);
    } else {
      const r = await createDeposit(
        refWallet.current.value,
        refType.current.value,
        refSum.current.value,
        refCurrency.current.value,
        refStatus.current.value,
        refCallback.current.value
      );
      setResp(r);
    }
  };

  const handleCallback = (e) => {
    e.preventDefault();
    callbackDeposit(id);
  };

  useEffect(() => {
    refWallet.current.value = wallet;
    refType.current.value = type;
    refSum.current.value = sum;
    refCurrency.current.value = currency;
    refStatus.current.value = status;
    refCallback.current.value = callback;
    refCallbackResponse.current.value = callback_response;
  }, [wallet, type, sum, currency, status, callback, callback_response]);

  return (
    <div className="max-w-sm mx-auto w-full px-4 py-8">
      <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Creating Deposit</h1>
      <form onSubmit={submitHandler} method="POST">
        {/* ... Input fields ... */}
        <div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="Currency-text">
              Callback
            </label>
            <input id="Currency-text" className="form-input w-full" type="text" ref={refCallback} />
            <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" onClick={handleCallback}>
              Send Callback
            </button>
          </div>
        </div>
        {/* ... More input fields ... */}
        <div className="m-1.5">
          <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

export default Form;
