import "../../components/deposits/form"
import "../../partials/Header"
import "../../partials/Sidebar"
import "../../services/api"
import "react"
import "react-router-dom"
import Form
import Header
import React
import Sidebar
import {getDeposit}
import {useParams}

function DepositEdit() {
    const { id } = useParams();

    const [wallet, setWallet] = React.useState("")
    const [type, setType] = React.useState("")
    const [sum, setSum] = React.useState("")
    const [currency, setCurrency] = React.useState("")
    const [status, setStatus] = React.useState("")
    const [callback, setCallback] = React.useState("")
    const [callback_response, setCallbackResponse] = React.useState("")


    React.useEffect(()=> {
        getDeposit(id).then((data)=> {
            setWallet(data.wallet)
            setType(data.type)
            setSum(data.sum)
            setCurrency(data.currency)
            setStatus(data.status)
            setCallback(data.callback)
            setCallbackResponse(data.callback_response)
        })
    })
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <Header />
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form
                          wallet={wallet}
                          type={type}
                          sum={sum}
                          currency={currency}
                          status={status}
                          callback={callback}
                          callback_response={callback_response}

                          id={id}
                    />
                </div>
            </main>
        </div>
    </div>)
}

export default DepositEdit