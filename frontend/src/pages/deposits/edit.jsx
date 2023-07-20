import Form from "../../components/deposits/form"
import Sidebar from "../../partials/Sidebar";
import {useParams} from "react-router-dom";
import {getDeposit} from "../../services/api";
import React from "react";
function DepositEdit() {
    const { id } = useParams();

    const [owner_id, setOwnerId] = React.useState("")
    const [wallet, setWallet] = React.useState("")
    const [type, setType] = React.useState("")
    const [sum, setSum] = React.useState("")
    const [currency, setCurrency] = React.useState("")
    

    React.useEffect(()=> {
        getDeposit(id).then((data)=> {
            setOwnerId(data.owner_id)
            setWallet(data.wallet)
            setType(data.type)
            setSum(data.sum)
            setCurrency(data.currency)
            
        })
    })
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form

                          owner_id={owner_id}
                          wallet={wallet}
                          type={type}
                          sum={sum}
                          currency={currency}
                          

                          id={id}
                    />
                </div>
            </main>
        </div>
    </div>)
}

export default DepositEdit