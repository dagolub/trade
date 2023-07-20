import Form from "../../components/transactions/form"
import Sidebar from "../../partials/Sidebar";
import {useParams} from "react-router-dom";
import {getTransaction} from "../../services/api";
import React from "react";
function TransactionEdit() {
    const { id } = useParams();

    const [owner_id, setOwnerId] = React.useState("")
    const [from_wallet, setFromWallet] = React.useState("")
    const [to_wallet, setToWallet] = React.useState("")
    const [tx, setTx] = React.useState("")
    const [amount, setAmount] = React.useState("")
    const [currency, setCurrency] = React.useState("")
    const [type, setType] = React.useState("")
    

    React.useEffect(()=> {
        getTransaction(id).then((data)=> {
            setOwnerId(data.owner_id)
            setFromWallet(data.from_wallet)
            setToWallet(data.to_wallet)
            setTx(data.tx)
            setAmount(data.amount)
            setCurrency(data.currency)
            setType(data.type)
            
        })
    })
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form

                          owner_id={owner_id}
                          from_wallet={from_wallet}
                          to_wallet={to_wallet}
                          tx={tx}
                          amount={amount}
                          currency={currency}
                          type={type}
                          

                          id={id}
                    />
                </div>
            </main>
        </div>
    </div>)
}

export default TransactionEdit