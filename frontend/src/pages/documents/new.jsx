import React from 'react';
import Sidebar from '../../partials/Sidebar';
import Header from '../../partials/Header';
import {createDocument} from "../../services/api";
import {populateSelect} from "../../utils"
import load from '../../images/load.svg'
import showError from '../../components/showError'
function DepositNew() {

    const [document, setDocument] = React.useState(File|null)
    const [loading, setLoading] = React.useState(false)
    const [error, setError] = React.useState("")
      const handleFileChange = (e) => {
        if (e.target.files) {
            setDocument(e.target.files[0]);
        }
      };
    const submitHandler = (e) => {
        e.preventDefault()
        const formData = new FormData()
        formData.append("document", document)

        if (loading === false) {
            setLoading(true)
            createDocument(formData).then((data) => {
                if (data.id) {
                    window.location.href = "/documents/list"
                } else {
                    setLoading(false)
                    setError(showError(data))

                }
            })
        }
    }

    return (
        <div className="flex h-[100vh] overflow-hidden"> {/* Fixed typo in height */}
            <Sidebar/>
            <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                <Header/>
                <main className="grow">
                    <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                        <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">New document</h1>
                        <form method="POST" onSubmit={submitHandler}>
                            {error}
                            <div>
                                <div>
                                    <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                                        File
                                    </label>
                                    <input id="supporting-text" className="form-input w-full" type="file"
                                           style={{"width": "100px"}} onChange={handleFileChange}/>
                                </div>
                            </div>


                            <div className="m-1.5">
                                <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white"
                                        type="submit">
                                    {loading ? <img src={load} width="24" height="24"/> : ''}
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </main>
            </div>
        </div>
    );
}

export default DepositNew;
