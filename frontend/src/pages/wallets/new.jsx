import Form from "../../components/wallets/form"
import Sidebar from "../../partials/Sidebar";

function WalletsNew() {
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form/>
                </div>
            </main>
        </div>
    </div>)
}

export default WalletsNew