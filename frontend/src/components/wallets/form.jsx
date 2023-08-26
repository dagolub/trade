import "../../services/api"
import 'react'
import React
import updateWallet}
import {createWallet

function Form({wallet = "",type = "",id=""}) {
    const refWallet = React.useRef("")
    const refType = React.useRef("")
    
    const setResp = (resp) => {
        if( resp.wallet ==  refWallet.current.value ) {
            window.location.href = "/wallets/list"
        } else {
            alert(resp.response.data.detail)
        }
    }
    const submitHandler = async (e) => {
        e.preventDefault()

        if (id) {
            const r = await updateWallet(id, refWallet.current.value, refType.current.value, )
            setResp(r)
        } else {
            const r = await createWallet(refWallet.current.value, refType.current.value, )
            setResp(r)
        }
    }
    React.useEffect(()=> {
        if (wallet||type||true) {
            refWallet.current.value = wallet
            refType.current.value = type
            
        }

    })
    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Ceating Wallet</h1>
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

                
                <div className="m-1.5">
                      <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Form;