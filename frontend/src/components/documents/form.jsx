import React from 'react';
import {createDocument, updateDocument} from '../../services/api'; // Make sure to provide the correct path to your API methods
import showError from "../showError";

function Form({
                  name = '',
                  file = '',
                  ext = false,
                  id = '',
              }) {
    const refName = React.useRef('');
    const refFile = React.useRef('');
    const refExt = React.useRef('');
    const [document, setDocument] = React.useState(File|null)
    const [loading, setLoading] = React.useState(false);


    const setResp = (resp) => {
        if (resp.name === refName.current.value) {
            window.location.href = '/documents/list';
        } else {
            showError(resp);
            setLoading(false)
        }
    };
    const handleFileChange = (e) => {
        if (e.target.files) {
            setDocument(e.target.files[0]);
        }
      };
    const submitHandler = async (e) => {
        e.preventDefault();

        if (!loading) {
            if (id) {
                const r = await updateDocument(id, document);
                setResp(r);
            } else {
                const r = await createDocument(document);
                setResp(r);
            }
            setLoading(true)
        }
    };


    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Document</h1>
            <form onSubmit={submitHandler} method="POST">
                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Name: {name}
                        </label>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            File: {file}
                        </label>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Ext: {ext}
                        </label>
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                        File
                        </label>
                        <input id="supporting-text" className="form-input w-full" type="file"
                               style={{"width": "100px"}} onChange={handleFileChange}/>
                    </div>
                </div>


                <div className="m-1.5">
                    <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Form;