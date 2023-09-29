import React from 'react';
import Sidebar from '../../partials/Sidebar';
import Header from '../../partials/Header';
import {getCurrencies, getChains} from "../../services/api";
import Select from "react-select";
import {populateSelect} from "../../utils"
function UsersNew() {
    const refSum = React.useRef("")
    const refCurrency = React.useRef("")
    const refChain = React.useRef("")
    const refCallback = React.useRef("")

    const [currencies, setCurrencies] = React.useState([])
    const [chains, setChains] = React.useState([])

    const [currency, setCurrency] = React.useState(false)
    const [chain, setChain] = React.useState(false)
    // const setCurrency = (data) => {
    //     alert(data)
    // }
    // const setChain = (data) => {
    //     alert(data)
    // }
    React.useEffect(()=>{
        getCurrencies().then((data)=>setCurrencies(populateSelect(data, "currency")))
        getChains().then((data)=>setChains(populateSelect(data, "chain")))
    }, [])
    return (
        <div className="flex h-[100vh] overflow-hidden"> {/* Fixed typo in height */}
            <Sidebar/>
            <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                <Header/>
                <main className="grow">
                    <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                        <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">New deposit</h1>
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
                                <label>Currencies</label>
                                <Select options={currencies}

                                        // value={currency.find((d) => d.value === currency)}
                                            onChange={(choice) => setCurrency(choice["value"])}/>
                            </div>
                        </div>
                        <div>
                            <div>
                                <label>Chains</label>
                                <Select options={chains} styles={{"width": "200px"}}
                                        // value={chain.find((d) => d.value === chain)}
                                            onChange={(choice) => setChain(choice["value"])}/>
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
                    </div>
                </main>
            </div>
        </div>
    );
}

export default UsersNew;
