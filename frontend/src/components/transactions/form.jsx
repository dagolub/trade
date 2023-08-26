import "../../services/api"
import 'react'
import React
import updateTransaction}
import {createTransaction

function Form({from_wallet = "",to_wallet = "",tx = "",amount = "",currency = "",type = "",id=""}) {
    const refFromWallet = React.useRef("")
    const refToWallet = React.useRef("")
    const refTx = React.useRef("")
    const refAmount = React.useRef("")
    const refCurrency = React.useRef("")
    const refType = React.useRef("")
    
    const setResp = (resp) => {
        if( resp.tx ==  refTx.current.value ) {
            window.location.href = "/transactions/list"
        } else {
            alert(resp.response.data.detail)
        }
    }
    const submitHandler = async (e) => {
        e.preventDefault()

        if (id) {
            const r = await updateTransaction(id, refFromWallet.current.value, refToWallet.current.value,refTx.current.value,
                refAmount.current.value, refCurrency.current.value, refType.current.value, )
            setResp(r)
        } else {
            const r = await createTransaction(refFromWallet.current.value, refToWallet.current.value, refTx.current.value,
                refAmount.current.value, refCurrency.current.value, refType.current.value, )
            setResp(r)
        }
    }
    React.useEffect(()=> {
        if (from_wallet||to_wallet||tx||amount||currency||type||true) {
            refFromWallet.current.value = from_wallet
            refToWallet.current.value = to_wallet
            refTx.current.value = tx
            refAmount.current.value = amount
            refCurrency.current.value = currency
            refType.current.value = type
            
        }

    })
    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Ceating Transaction</h1>
            <form onSubmit={submitHandler} method="POST">
                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Tx-text">
                            From Wallet
                        </label>
                        <input id="Tx-text" className="form-input w-full" type="text" ref={refFromWallet}/>
                    </div>
                </div>                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Tx-text">
                            To Wallet
                        </label>
                        <input id="Tx-text" className="form-input w-full" type="text" ref={refToWallet}/>
                    </div>
                </div>
                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Tx-text">
                            Tx
                        </label>
                        <input id="Tx-text" className="form-input w-full" type="text" ref={refTx}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="Amount-text">
                            Amount
                        </label>
                        <input id="Amount-text" className="form-input w-full" type="text" ref={refAmount}/>
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
                        <label className="block text-sm font-medium mb-1" htmlFor="Type-text">
                            Type
                        </label>
                        <input id="Type-text" className="form-input w-full" type="text" ref={refType}/>
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