import showWalletCopy from "./showWalletCopy";
import React from "react"
import {putApikeys, getApikey} from "../services/api";
const ApiKEY = ({apikey, id}) => {
    const ak = apikey.apikey
    const [deposit, setDeposit] = React.useState(false)
    const [withdraw, setWithdraw] = React.useState(false)
    const [ips, setIPS] = React.useState([])
    const regenerate = () => {
        const data = {"id": id, "deposit": deposit, "withdraw": withdraw, "ips": ips}
        putApikeys(data).then((data)=>console.log(data))
    }
    const getChecked = (value, name) => {
        if (name === "deposit") {
            setDeposit(value)
        }
        if (name === "withdraw") {
            setWithdraw(value)
        }
    }
    const getIPS = (value) => {
        setIPS(value)
    }
    React.useEffect(()=>{
        getApikey(id).then((data)=>{
            setDeposit(data["deposit"])
            setWithdraw(data["withdraw"])
            setIPS(data["ips"])
        })
    },[])
    return (
        <div className="apiKEY">
            <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" style={{"margin": "10px"}}
                    type="submit" onClick={regenerate}>
                Regenerate KEY
            </button>

            <a href="#">Request details</a>
            <input type="text" className="apikey" value={ak} style={{"width": "95%"}}/>
            {
                showWalletCopy(ak)
            }
            <br/>
            <label>
                Deposit <input type="checkbox" checked={deposit} onChange={e=> getChecked(e.currentTarget.checked, "deposit")}/>
            </label>
            <label>
                Withdraw <input type="checkbox" checked={withdraw} onChange={e=> getChecked(e.currentTarget.checked, "withdraw")}/>
            </label>
            <label>
                Allowed IP: <input type="text" value={ips} onChange={e=>getIPS(e.target.value)}/>
            </label>
        </div>
    )
}

export default ApiKEY;