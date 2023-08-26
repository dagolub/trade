import "../../components/transactions/form"
import "../../partials/Sidebar"
import "../../services/api"
import "react"
import "react-router-dom"
import Form
import React
import Sidebar
import {getTransaction}
import {useParams}

function TransactionEdit() {
    const { id } = useParams();

    const [Tx, setTx] = React.useState("")
    const [Amount, setAmount] = React.useState("")
    const [Currency, setCurrency] = React.useState("")
    const [Type, setType] = React.useState("")
    

    React.useEffect(()=> {
        getTransaction(id).then((data)=> {
            setTx(data.Tx)
            setAmount(data.Amount)
            setCurrency(data.Currency)
            setType(data.Type)
            
        })
    })
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form

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