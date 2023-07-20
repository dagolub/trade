import React from 'react';
import {createUser, updateUser} from "../../services/api";

function Form({name = "", email = "", is_active = false, is_superuser = false, id = ""}) {
    const refName = React.useRef("")
    const refEmail = React.useRef("")
    const refPassword = React.useRef("")
    const refActive = React.useRef(false)
    const refSuperuser = React.useRef(false)


    const setResp = (resp) => {
        if( resp.email ==  refEmail.current.value ) {
            window.location.href = "/users/list"
        } else {
            alert(resp.response.data.detail)
        }
    }
    const submitHandler = async (e) => {
        e.preventDefault()

        if (id) {
            const r = await updateUser(id, refName.current.value, refEmail.current.value, refPassword.current.value,
                refActive.current.checked, refSuperuser.current.checked)
            setResp(r)
        } else {
            const r = await createUser(refName.current.value, refEmail.current.value, refPassword.current.value,
                refActive.current.checked, refSuperuser.current.checked)
            setResp(r)
        }
    }
    React.useEffect(()=> {
        if (name || email || is_active || is_superuser) {
            refName.current.value = name
            refEmail.current.value = email
            refActive.current.checked = is_active
            refSuperuser.current.checked = is_superuser
        }

    })
    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Ceating User</h1>
            <form onSubmit={submitHandler} method="POST">

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Name
                        </label>
                        <input id="supporting-text" className="form-input w-full" type="text" ref={refName}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            E-Mail
                        </label>
                        <input id="email" className="form-input w-full" type="email" ref={refEmail}/>
                    </div>
                </div>

                <div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="supporting-text">
                            Password
                        </label>
                        <input id="supporting-text" className="form-input w-full" type="password" ref={refPassword}/>
                    </div>
                </div>

                <div className="m-3">
                    <label className="flex items-center">
                        <input type="checkbox" className="form-checkbox" name="is_active" ref={refActive}/>
                        <span className="text-sm ml-2">Is Active</span>
                    </label>
                </div>

                <div className="m-3">
                    <label className="flex items-center">
                        <input type="checkbox" className="form-checkbox" name="is_superuser" ref={refSuperuser}/>
                        <span className="text-sm ml-2">Is Superuser</span>
                    </label>
                </div>

                <div className="m-1.5">
                      <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Form;