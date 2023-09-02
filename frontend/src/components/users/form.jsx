import React from 'react';
import { updateUser, createUser } from '../../services/api'; // Make sure to provide the correct path to your API methods

function Form({
  name = '',
  email = '',
  is_active = false,
  is_superuser = false,
  id = '',
  auto = false,
  otp = ''
}) {
  const refName = React.useRef('');
  const refEmail = React.useRef('');
  const refPassword = React.useRef('');
  const refActive = React.useRef(false);
  const refSuperuser = React.useRef(false);
  const [autotransfer, setAutoTransfer] = React.useState(false);
  const [first_time, setFirstTime] = React.useState(false);

  const setResp = (resp) => {
    if (resp.email === refEmail.current.value) {
      window.location.href = '/users/list';
    } else {
      alert(resp.response.data.detail);
    }
  };

  const submitHandler = async (e) => {
    e.preventDefault();

    if (id) {
      const r = await updateUser(
        id,
        refName.current.value,
        refEmail.current.value,
        refPassword.current.value,
        refActive.current.checked,
        refSuperuser.current.checked,
        autotransfer
      );
      setResp(r);
    } else {
      const r = await createUser(
        refName.current.value,
        refEmail.current.value,
        refPassword.current.value,
        refActive.current.checked,
        refSuperuser.current.checked,
        autotransfer
      );
      setResp(r);
    }
  };

  React.useEffect(() => {
    if ((name || email || is_active || is_superuser || auto) && !first_time) {
      refName.current.value = name;
      refEmail.current.value = email;
      refActive.current.checked = is_active;
      refSuperuser.current.checked = is_superuser;
      setAutoTransfer(auto);
      setFirstTime(true);
    }
  });

    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">User</h1>
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
                <div className="m-3 w-24">
                    <div>
                        <div className="text-slate-800 dark:text-slate-100 font-semibold"
                             style={{"width": "200px"}}>Auto Transfer
                        </div>

                    </div>
                    <div className="flex items-center">
                        <div className="form-switch">
                            <input type="checkbox" id="switch-1" className="sr-only" checked={autotransfer}
                                   onChange={() => setAutoTransfer(!autotransfer)}/>
                            <label className="bg-slate-400 dark:bg-slate-700" htmlFor="switch-1">
                                <span className="bg-white shadow-sm" aria-hidden="true"></span>
                                <span className="sr-only">Switch label</span>
                            </label>
                        </div>
                        <div
                            className="text-sm text-slate-400 dark:text-slate-500 italic ml-2">{autotransfer ? 'On' : 'Off'}</div>
                    </div>
                </div>
                <img src={"/" + otp} />
                <div className="m-1.5">
                    <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Form;