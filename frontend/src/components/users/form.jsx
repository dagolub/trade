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

        return {"btc": btc, "ltc": ltc, "usdt": usdt, "eth": eth}
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
        getCurrencies().then((data) => {
            setCurrencies(data)
        })
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