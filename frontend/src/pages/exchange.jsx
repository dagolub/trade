import React from 'react';
import Sidebar from '../partials/Sidebar';
import Header from '../partials/Header';
import {getChains, getCurrencies} from "../services/api";
import {populateSelect} from "../utils";
import {useSearchParams} from "react-router-dom";
import load from '../images/load.svg'
import showError from "../components/showError";


function Exchange() {
    let [searchParams, setSearchParams] = useSearchParams();
    const [fromSum, setFromSUM] = React.useState(0)
    const [toSum, setToSUM] = React.useState(0)


    const [selectedFromCurrency, setSelectedFromCurrency] = React.useState([])
    const [selectedToCurrency, setSelectedToCurrency] = React.useState([])



    const [fromCurrencies, setFromCurrencies] = React.useState([])
    const [fromChains, setFromChains] = React.useState([])
    const [toCurrencies, setToCurrencies] = React.useState([])
    const [toChains, setToChains] = React.useState([])

    const [loading, setLoading] = React.useState(false)
    const submitHandler = (e) => {
        e.preventDefault()


    }

    React.useEffect(() => {

        const sum = searchParams.get("sum")
        if (sum > 0) {
            setFromSUM(parseFloat(sum))
        }
        const currency = searchParams.get("currency")
        if (currency) {
            setSelectedFromCurrency([currency])
            setSelectedToCurrency(["USDT"])
        }
        getCurrencies().then((data) => {
            setFromCurrencies(populateSelect(data, "fromCurrency"))
            setToCurrencies(populateSelect(data, "toCurrency"))
        })
    }, [])
    return (
        <div className="flex h-[100vh] overflow-hidden"> {/* Fixed typo in height */}
            <Sidebar/>
            <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                <Header/>
                <main className="grow">
                    <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto"><h1
                        className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Exchange</h1>

                        <form method="POST" onSubmit={submitHandler}>
                            <div className="grid grid-cols-12 gap-6">
                                <div className="flex-col col-span-full sm:col-span-6">

                                    <div>
                                        <div>
                                            <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                                                Sum
                                            </label>
                                            <input id="supporting-text" className="form-input w-full" type="text"
                                                   style={{"width": "100px"}} value={fromSum}/>
                                        </div>
                                    </div>
                                    <div>
                                        <div>
                                            <label>Currencies</label><br/>
                                            <select id="fromCurrency" name="fromCurrency" className="form-select w-full"
                                                    style={{"width": "100px"}} value={selectedFromCurrency}>
                                                {
                                                    fromCurrencies.map(entity => {
                                                        return (
                                                            <option key={entity.value}

                                                                    value={entity.value}>{entity.label}</option>)
                                                    })
                                                }
                                            </select>

                                        </div>
                                    </div>


                                </div>
                                <div className="flex-col col-span-full sm:col-span-6">

                                    <div>
                                        <div>
                                            <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                                                Sum
                                            </label>
                                            <input id="supporting-text" className="form-input w-full" type="text"

                                                   style={{"width": "100px"}}/>
                                        </div>
                                    </div>
                                    <div>
                                        <div>
                                            <label>Currencies</label><br/>
                                            <select id="toCurrency" name="toCurrency" className="form-select w-full"
                                                    style={{"width": "100px"}}  value={selectedToCurrency}>
                                                {
                                                    toCurrencies.map(entity => {
                                                        return (
                                                            <option key={entity.value}

                                                                    value={entity.value}>{entity.label}</option>)
                                                    })
                                                }
                                            </select>

                                        </div>
                                    </div>


                                </div>
                            </div>
                            <div className="m-1.5" style={{
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "marginTop": "30px"
                            }}>
                                <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white"
                                        type="submit">
                                    {loading ? <img src={load} width="24" height="24"/> : ''}
                                    Exchange
                                </button>
                            </div>
                        </form>
                    </div>
                </main>
            </div>
        </div>
    );
}

export default Exchange;
