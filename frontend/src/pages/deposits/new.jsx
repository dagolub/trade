import React from 'react';
import Sidebar from '../../partials/Sidebar';
import Header from '../../partials/Header';
import {getCurrencies, getChains, createDeposit} from "../../services/api";
import {populateSelect} from "../../utils"
import load from '../../images/load.svg'
import showError from '../../components/showError'
function DepositNew() {
    const refSum = React.useRef("")
    const refCurrency = React.useRef("")
    const refChain = React.useRef("")
    const refCallback = React.useRef("")

    const [currencies, setCurrencies] = React.useState([])
    const [chains, setChains] = React.useState([])
    const [loading, setLoading] = React.useState(false)

    const setCurrencyRate = (data) => {
        if (data === "USDT") {
            refChain.current.value = "TRC20"
        } else {
            refChain.current.value = data
        }

    }

    const submitHandler = (e) => {
        e.preventDefault()
        const sum = refSum.current.value
        const currency = refCurrency.current.value
        const chain = refChain.current.value
        const callback = refCallback.current.value

        if (loading === false) {
            setLoading(true)
            createDeposit(sum, currency, chain, callback).then((data) => {
                if (data.id) {
                    window.location.href = "/deposits/view/" + data.id
                } else {
                    showError(data)
                    setLoading(false)
                }
            })
        }
    }

    React.useEffect(() => {
        getCurrencies().then((data) => setCurrencies(populateSelect(data, "currency")))
        getChains().then((data) => setChains(populateSelect(data, "chain")))
    }, [])
    return (
        <div className="flex h-[100vh] overflow-hidden"> {/* Fixed typo in height */}
            <Sidebar/>
            <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                <Header/>
                <main className="grow">
                    <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                        <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">New deposit</h1>
                        <form method="POST" onSubmit={submitHandler}>
                            <div>
                                <div>
                                    <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                                        Sum
                                    </label>
                                    <input id="supporting-text" className="form-input w-full" type="text" ref={refSum}
                                           style={{"width": "100px"}}/>
                                </div>
                            </div>
                            <div>
                                <div>
                                    <label>Currencies</label><br/>
                                    <select id="currency" name="currency" className="form-select w-full"
                                            style={{"width": "100px"}} ref={refCurrency}>
                                        {
                                            currencies.map(entity => {
                                                return (
                                                    <option key={entity.value}
                                                            onClick={() => setCurrencyRate(entity.value)}
                                                            value={entity.value}>{entity.label}</option>)
                                            })
                                        }
                                    </select>

                                </div>
                            </div>
                            <div>
                                <div>
                                    <label>Chains</label><br/>
                                    <select id="chains" name="chains" className="form-select w-full"
                                            style={{"width": "100px"}} ref={refChain}>
                                        {
                                            chains.map(entity => {
                                                return (
                                                    <option key={entity.value}
                                                            value={entity.value}>{entity.label}</option>)
                                            })
                                        }
                                    </select>
                                </div>
                            </div>
                            <div>
                                <div>
                                    <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                                        Callback
                                    </label>
                                    <input id="supporting-text" className="form-input w-full" type="text"
                                           ref={refCallback}/>
                                </div>
                            </div>
                            <div className="m-1.5">
                                <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white"
                                        type="submit">
                                    {loading ? <img src={load} width="24" height="24"/> : ''}
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </main>
            </div>
        </div>
    );
}

export default DepositNew;
