import "../../services/api"
import 'react'
import callbackDeposit}
import React
import updateDeposit
import {createDeposit

function Form({wallet = "",type = "",sum = "",currency = "", status="", callback="", callback_response="", id=""}) {
    const refWallet = React.useRef("")
    const refType = React.useRef("")
    const refSum = React.useRef("")
    const refCurrency = React.useRef("")
    const refStatus = React.useRef("")
    const refCallback = React.useRef("")
    const refCallbackResponse = React.useRef("")

    const setResp = (resp) => {
        if( resp.wallet ===  refWallet.current.value ) {
            window.location.href = "/deposits/list"
        } else {
            alert(resp.response.data.detail)
        }
    }
    const submitHandler = async (e) => {
        e.preventDefault()

        if (id) {
            const r = await updateDeposit(id, refWallet.current.value, refType.current.value, refSum.current.value,
                refCurrency.current.value, refStatus.current.value, refCallback.current.value )
            setResp(r)
        } else {
            const r = await createDeposit(refWallet.current.value, refType.current.value, refSum.current.value,
                refCurrency.current.value, refStatus.current.value, refCallback.current.value)
            setResp(r)
        }
    }
    const handleCallback = (e) => {
        e.preventDefault()
        callbackDeposit(id)
    }
    React.useEffect(()=> {
        if (wallet||type||sum||currency||status||callback|callback_response||true) {
            refWallet.current.value = wallet
            refType.current.value = type
            refSum.current.value = sum
            refCurrency.current.value = currency
            refStatus.current.value = status
            refCallback.current.value = callback
            refCallbackResponse.current.value = callback_response

        }

    })
    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Ceating Deposit</h1>
            <form onSubmit={submitHandler} method="POST">

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Wallet-text">
                            Wallet
                        </label>
                        <input id="Wallet-text" className="form-input w-full" type="text" ref={refWallet}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Type-text">
                            Type
                        </label>
                        <input id="Type-text" className="form-input w-full" type="text" ref={refType}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Sum-text">
                            Sum
                        </label>
                        <input id="Sum-text" className="form-input w-full" type="text" ref={refSum}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Currency-text">
                            Currency
                        </label>
                        <input id="Currency-text" className="form-input w-full" type="text" ref={refCurrency}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Currency-text">
                            Status
                        </label>
                        <input id="Currency-text" className="form-input w-full" type="text" ref={refStatus}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Currency-text">
                            Callback
                        </label>
                        <input id="Currency-text" className="form-input w-full" type="text" ref={refCallback}/>
                        <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" onClick={handleCallback}>Send Callback</button>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Currency-text">
                            Callback Response
                        </label>
                        <textarea rows="5" id="Currency-text" className="form-input w-full" ref={refCallbackResponse}>
                        </textarea>
                    </div>
                </div>
                <div className="m-1.5">
                      <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Form;