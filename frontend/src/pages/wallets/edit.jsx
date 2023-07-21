import Form from "../../components/wallets/form"
import Sidebar from "../../partials/Sidebar";
import {useParams} from "react-router-dom";
import {getWallet} from "../../services/api";
import React from "react";
function WalletEdit() {
    const { id } = useParams();

    const [Wallet, setWallet] = React.useState("")
    const [Type, setType] = React.useState("")
    

    React.useEffect(()=> {
        getWallet(id).then((data)=> {
            setWallet(data.Wallet)
            setType(data.Type)
            
        })
    })
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form

                          wallet={wallet}
                          type={type}
                          

                          id={id}
                    />
                </div>
            </main>
        </div>
    </div>)
}

export default WalletEdit