import showWalletCopy from "./showWalletCopy";

const apiKEY = (apikey, id) => {
    const ak = "12345678901234567890" //apikey["apikey"]
    return (
        <div className="apiKEY">
            <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" style={{"margin": "10px"}}
                    type="submit">
                Regenerate KEY
            </button>

            <a href="#">Request details</a>
            <input type="text" value={ak} style={{"width": "95%"}}/>
            {
                showWalletCopy(ak)
            }
            <br/>
            <label>
                Deposit <input type="checkbox"/>
            </label>
            <label>
                Withdraw <input type="checkbox"/>
            </label>
            <label>
                Allowed IP: <input type="text"/>
            </label>
        </div>
    )
}

export default apiKEY;