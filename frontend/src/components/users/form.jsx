import React from 'react';
import {updateUser, createUser, getCurrencies} from '../../services/api'; // Make sure to provide the correct path to your API methods
import showError from "../showError";

function Form({
                  name = '',
                  email = '',
                  is_active = false,
                  is_superuser = false,
                  id = '',
                  auto = false,
                  commissions = []
              }) {

    const refBTCinPercent = React.useRef('');
    const refBTCinFixed = React.useRef('');
    const refBTCoutPercent = React.useRef('');
    const refBTCoutFixed = React.useRef('');

    const refLTCinPercent = React.useRef('');
    const refLTCinFixed = React.useRef('');
    const refLTCoutPercent = React.useRef('');
    const refLTCoutFixed = React.useRef('');

    const refUSDTinPercent = React.useRef('');
    const refUSDTinFixed = React.useRef('');
    const refUSDToutPercent = React.useRef('');
    const refUSDToutFixed = React.useRef('');
    
    const refETHinPercent = React.useRef('');
    const refETHinFixed = React.useRef('');
    const refETHoutPercent = React.useRef('');
    const refETHoutFixed = React.useRef('');
    
    const refUSDCinPercent = React.useRef('');
    const refUSDCinFixed = React.useRef('');
    const refUSDCoutPercent = React.useRef('');
    const refUSDCoutFixed = React.useRef('');
    
    const refXRPinPercent = React.useRef('');
    const refXRPinFixed = React.useRef('');
    const refXRPoutPercent = React.useRef('');
    const refXRPoutFixed = React.useRef('');
        
    const refMATICinPercent = React.useRef('');
    const refMATICinFixed = React.useRef('');
    const refMATICoutPercent = React.useRef('');
    const refMATICoutFixed = React.useRef('');
    
    const refSOLinPercent = React.useRef('');
    const refSOLinFixed = React.useRef('');
    const refSOLoutPercent = React.useRef('');
    const refSOLoutFixed = React.useRef('');
    
    const refTRXinPercent = React.useRef('');
    const refTRXinFixed = React.useRef('');
    const refTRXoutPercent = React.useRef('');
    const refTRXoutFixed = React.useRef('');
    
    const refTONinPercent = React.useRef('');
    const refTONinFixed = React.useRef('');
    const refTONoutPercent = React.useRef('');
    const refTONoutFixed = React.useRef('');
    
    const refName = React.useRef('');
    const refEmail = React.useRef('');
    const refPassword = React.useRef('');
    const refActive = React.useRef(false);
    const refSuperuser = React.useRef(false);
    const [autotransfer, setAutoTransfer] = React.useState(false);
    const [loading, setLoading] = React.useState(false);
    const [currencies, setCurrencies] = React.useState([]);

    const setResp = (resp) => {
        if (resp.email === refEmail.current.value) {
            window.location.href = '/users/list';
        } else {
            showError(resp);
            setLoading(false)
        }
    };
    const getCommission = () => {
        let btc = {
            "in": {"percent": refBTCinPercent.current.value, "fixed": refBTCinFixed.current.value},
            "out": {"percent": refBTCoutPercent.current.value, "fixed": refBTCoutFixed.current.value}
        }
        let ltc = {
            "in": {"percent": refLTCinPercent.current.value, "fixed": refLTCinFixed.current.value},
            "out": {"percent": refLTCoutPercent.current.value, "fixed": refLTCoutFixed.current.value}
        }

        let usdt = {
            "in": {"percent": refUSDTinPercent.current.value, "fixed": refUSDTinFixed.current.value},
            "out": {"percent": refUSDToutPercent.current.value, "fixed": refUSDToutFixed.current.value}
        }
        let eth = {
            "in": {"percent": refETHinPercent.current.value, "fixed": refETHinFixed.current.value},
            "out": {"percent": refETHoutPercent.current.value, "fixed": refETHoutFixed.current.value}
        }
        let usdc = {
            "in": {"percent": refUSDCinPercent.current.value, "fixed": refUSDCinFixed.current.value},
            "out": {"percent": refUSDCoutPercent.current.value, "fixed": refUSDCoutFixed.current.value}
        }
        let xrp = {
            "in": {"percent": refXRPinPercent.current.value, "fixed": refXRPinFixed.current.value},
            "out": {"percent": refXRPoutPercent.current.value, "fixed": refXRPoutFixed.current.value}
        }
        let matic = {
            "in": {"percent": refMATICinPercent.current.value, "fixed": refMATICinFixed.current.value},
            "out": {"percent": refMATICoutPercent.current.value, "fixed": refMATICoutFixed.current.value}
        }
        let sol = {
            "in": {"percent": refSOLinPercent.current.value, "fixed": refSOLinFixed.current.value},
            "out": {"percent": refSOLoutPercent.current.value, "fixed": refSOLoutFixed.current.value}
        }
        let trx = {
            "in": {"percent": refTRXinPercent.current.value, "fixed": refTRXinFixed.current.value},
            "out": {"percent": refTRXoutPercent.current.value, "fixed": refTRXoutFixed.current.value}
        }
        let ton = {
            "in": {"percent": refTONinPercent.current.value, "fixed": refTONinFixed.current.value},
            "out": {"percent": refTONoutPercent.current.value, "fixed": refTONoutFixed.current.value}
        }
        return {"btc": btc, "ltc": ltc, "usdt": usdt, "eth": eth, "usdc": usdc, "xrp": xrp, "matic": matic, "sol": sol, "trx": trx, "ton": ton}
    }
    const submitHandler = async (e) => {
        e.preventDefault();
        const commission = getCommission()
        if (!loading) {
            if (id) {
                const r = await updateUser(
                    id,
                    refName.current.value,
                    refEmail.current.value,
                    refPassword.current.value,
                    refActive.current.checked,
                    refSuperuser.current.checked,
                    autotransfer,
                    commission
                );
                setResp(r);
            } else {
                const r = await createUser(
                    refName.current.value,
                    refEmail.current.value,
                    refPassword.current.value,
                    refActive.current.checked,
                    refSuperuser.current.checked,
                    autotransfer,
                    commission
                );
                setResp(r);
            }
            setLoading(true)
        }
    };
    React.useEffect(() => {
        // getCurrencies().then((data) => {
        //     setCurrencies(data)
        // })
        if (name || email || is_active || is_superuser || auto || commissions) {
            refName.current.value = name;
            refEmail.current.value = email;
            refActive.current.checked = is_active;
            refSuperuser.current.checked = is_superuser;
            setAutoTransfer(auto);
            if (commissions) {

                if (commissions.hasOwnProperty("btc") && commissions.btc.hasOwnProperty("in")) {
                    refBTCinPercent.current.value = commissions["btc"]["in"]["percent"]
                    refBTCinFixed.current.value = commissions["btc"]["in"]["fixed"]
                    refBTCoutPercent.current.value = commissions["btc"]["out"]["percent"]
                    refBTCoutFixed.current.value = commissions["btc"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("ltc") && commissions.ltc.hasOwnProperty("in")) {
                    refLTCinPercent.current.value = commissions["ltc"]["in"]["percent"]
                    refLTCinFixed.current.value = commissions["ltc"]["in"]["fixed"]
                    refLTCoutPercent.current.value = commissions["ltc"]["out"]["percent"]
                    refLTCoutFixed.current.value = commissions["ltc"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("usdt") && commissions.usdt.hasOwnProperty("in")) {
                    refUSDTinPercent.current.value = commissions["usdt"]["in"]["percent"]
                    refUSDTinFixed.current.value = commissions["usdt"]["in"]["fixed"]
                    refUSDToutPercent.current.value = commissions["usdt"]["out"]["percent"]
                    refUSDToutFixed.current.value = commissions["usdt"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("eth") && commissions.eth.hasOwnProperty("in")) {
                    refETHinPercent.current.value = commissions["eth"]["in"]["percent"]
                    refETHinFixed.current.value = commissions["eth"]["in"]["fixed"]
                    refETHoutPercent.current.value = commissions["eth"]["out"]["percent"]
                    refETHoutFixed.current.value = commissions["eth"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("usdc") && commissions.usdc.hasOwnProperty("in")) {
                    refUSDCinPercent.current.value = commissions["usdc"]["in"]["percent"]
                    refUSDCinFixed.current.value = commissions["usdc"]["in"]["fixed"]
                    refUSDCoutPercent.current.value = commissions["usdc"]["out"]["percent"]
                    refUSDCoutFixed.current.value = commissions["usdc"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("xrp") && commissions.xrp.hasOwnProperty("in")) {
                    refXRPinPercent.current.value = commissions["xrp"]["in"]["percent"]
                    refXRPinFixed.current.value = commissions["xrp"]["in"]["fixed"]
                    refXRPoutPercent.current.value = commissions["xrp"]["out"]["percent"]
                    refXRPoutFixed.current.value = commissions["xrp"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("matic") && commissions.matic.hasOwnProperty("in")) {
                    refMATICinPercent.current.value = commissions["matic"]["in"]["percent"]
                    refMATICinFixed.current.value = commissions["matic"]["in"]["fixed"]
                    refMATICoutPercent.current.value = commissions["matic"]["out"]["percent"]
                    refMATICoutFixed.current.value = commissions["matic"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("sol") && commissions.sol.hasOwnProperty("in")) {
                    refSOLinPercent.current.value = commissions["sol"]["in"]["percent"]
                    refSOLinFixed.current.value = commissions["sol"]["in"]["fixed"]
                    refSOLoutPercent.current.value = commissions["sol"]["out"]["percent"]
                    refSOLoutFixed.current.value = commissions["sol"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("trx") && commissions.trx.hasOwnProperty("in")) {
                    refTRXinPercent.current.value = commissions["trx"]["in"]["percent"]
                    refTRXinFixed.current.value = commissions["trx"]["in"]["fixed"]
                    refTRXoutPercent.current.value = commissions["trx"]["out"]["percent"]
                    refTRXoutFixed.current.value = commissions["trx"]["out"]["fixed"]
                }
                if (commissions.hasOwnProperty("ton") && commissions.ton.hasOwnProperty("in")) {
                    refTONinPercent.current.value = commissions["ton"]["in"]["percent"]
                    refTONinFixed.current.value = commissions["ton"]["in"]["fixed"]
                    refTONoutPercent.current.value = commissions["ton"]["out"]["percent"]
                    refTONoutFixed.current.value = commissions["ton"]["out"]["fixed"]
                }
            }
        }
    }, [name, email, is_active, is_superuser, auto]);

    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">User</h1>
            <form onSubmit={submitHandler} method="POST">

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Name
                        </label>
                        <input id="supporting-text" className="form-input w-full" type="text" ref={refName}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            E-Mail
                        </label>
                        <input id="email" className="form-input w-full" type="email" ref={refEmail}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Password
                        </label>
                        <input id="supporting-text" className="form-input w-full" type="password" ref={refPassword}/>
                    </div>
                </div>

                <div className="m-3">
                    <label className="flex items-center">
                        <input type="checkbox" className="form-checkbox" name="is_active" ref={refActive}/>
                        <span className="text-sm ml-2">Is Active</span>
                    </label>
                </div>

                <div className="m-3">
                    <label className="flex items-center">
                        <input type="checkbox" className="form-checkbox" name="is_superuser" ref={refSuperuser}/>
                        <span className="text-sm ml-2">Is Superuser</span>
                    </label>
                </div>

                <div className="m-3 w-24">
                    <div>
                        <div className="text-slate-800 dark:text-slate-100 font-semibold"
                             style={{"width": "200px"}}>Auto Transfer
                        </div>

                    </div>
                    <div className="flex items-center">
                        <div className="form-switch">
                            <input type="checkbox" id="switch-1" className="sr-only" checked={autotransfer}
                                   onChange={() => setAutoTransfer(!autotransfer)}/>
                            <label className="bg-slate-400 dark:bg-slate-700" htmlFor="switch-1">
                                <span className="bg-white shadow-sm" aria-hidden="true"></span>
                                <span className="sr-only">Switch label</span>
                            </label>
                        </div>
                        <div
                            className="text-sm text-slate-400 dark:text-slate-500 italic ml-2">{autotransfer ? 'On' : 'Off'}</div>
                    </div>
                </div>
                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Commissions
                        </label>
                        <table cellPadding={3}>
                            <thead>
                            <tr>
                                <th rowSpan={2}>Currency</th>
                                <th colSpan={2}>Income</th>
                                <th colSpan={2}>Outcome</th>
                            </tr>
                            <tr>
                                <th>Percent</th>
                                <th>Fixed</th>
                                <th>Percent</th>
                                <th>Fixed</th>
                            </tr>
                            </thead>
                            <tbody>
                            {/*{currencies.map(currency => {*/}
                            {/*        return (<tr key={currency}>*/}
                            {/*            <th>{currency}</th>*/}
                            {/*            <td><input type="text" ref={getRef(currency, suf)} style={{"width": "60px"}}/></td>*/}
                            {/*            <td><input type="text" ref={getRef(currency)} style={{"width": "60px"}}/></td>*/}
                            {/*            <td><input type="text" ref={getRef(currency)} style={{"width": "60px"}}/></td>*/}
                            {/*            <td><input type="text" ref={getRef(currency)}  style={{"width": "60px"}}/></td>*/}
                            {/*        </tr>)*/}
                            {/*    }*/}
                            {/*)}*/}
                            <tr>
                                <th>BTC</th>
                                <td><input type="text" ref={refBTCinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refBTCinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refBTCoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refBTCoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>LTC</th>
                                <td><input type="text" ref={refLTCinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refLTCinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refLTCoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refLTCoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>USDT</th>
                                <td><input type="text" ref={refUSDTinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refUSDTinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refUSDToutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refUSDToutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>ETH</th>
                                <td><input type="text" ref={refETHinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refETHinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refETHoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refETHoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>USDC</th>
                                <td><input type="text" ref={refUSDCinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refUSDCinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refUSDCoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refUSDCoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>XRP</th>
                                <td><input type="text" ref={refXRPinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refXRPinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refXRPoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refXRPoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>MATIC</th>
                                <td><input type="text" ref={refMATICinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refMATICinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refMATICoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refMATICoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>SOL</th>
                                <td><input type="text" ref={refSOLinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refSOLinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refSOLoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refSOLoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>TRX</th>
                                <td><input type="text" ref={refTRXinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refTRXinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refTRXoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refTRXoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            <tr>
                                <th>TON</th>
                                <td><input type="text" ref={refTONinPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refTONinFixed} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refTONoutPercent} style={{"width": "80px"}}/></td>
                                <td><input type="text" ref={refTONoutFixed} style={{"width": "80px"}}/></td>
                            </tr>
                            </tbody>
                        </table>
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