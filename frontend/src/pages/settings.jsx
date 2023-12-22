import React from 'react';
import Header from '../partials/Header';
import Sidebar from '../partials/Sidebar';
import ApiKEY from "../components/apikey"
import ApiKEYEmpty from "../components/apikey_empty"
import "../css/settings.css"
import {getApikeys} from "../services/api";

function Settings() {
    const h1_class = "text-2xl md:text-3xl text-slate-800 dark:text-slate-100 font-bold"
    const [apikeys, setApikeys] = React.useState([])
    React.useEffect(() => {
        getApikeys().then((data) => setApikeys(data))
    }, [])
    return (
        <div className="flex h-[100vh] overflow-hidden">
            <Sidebar/>
            <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                <Header/>
                <main className="grow">
                    <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                        <div className="sm:flex sm:justify-between sm:items-center mb-5">
                            <div className="mb-4 sm:mb-0">
                                <h1 className={h1_class}>Settings ✨</h1>
                            </div>
                        </div>
                        {apikeys.length > 0 &&

                            apikeys.map(entity => {
                                    return (<ApiKEY id={entity.id} key={entity.id} apikey={entity} />)
                                }
                            )
                        }
                        <ApiKEYEmpty />
                    </div>
                </main>
            </div>
        </div>
    );
}

export default Settings;
