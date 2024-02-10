import React from 'react';
import {updateFolder, createFolder} from '../../services/api'; // Make sure to provide the correct path to your API methods
import showError from "../showError";

function Form({
                  name = '',
                  folder_id = 0,
                  id = '',
              }) {

    const refName = React.useRef('');
    const refFolderId = React.useRef('');


    const [loading, setLoading] = React.useState(false);


    const setResp = (resp) => {
        if (resp.name === refName.current.value) {
            window.location.href = '/folders/list';
        } else {
            showError(resp);
            setLoading(false)
        }
    };
    const submitHandler = async (e) => {
        e.preventDefault();

        if (!loading) {
            if (id) {
                const r = await updateFolder(
                    id,
                    refName.current.value,
                    refFolderId.current.value,


                );
                setResp(r);
            } else {
                const r = await createFolder(
                    refName.current.value,
                    refFolderId.current.value,

                );
                setResp(r);
            }
            setLoading(true)
        }
    };

    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">User</h1>
            <form onSubmit={submitHandler} method="POST">

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Name: {name}
                        </label>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Folder Id: {folder_id}
                        </label>
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