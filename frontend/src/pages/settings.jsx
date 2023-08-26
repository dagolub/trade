import "../services/api"
import '../partials/Header'
import '../partials/Sidebar'
import 'react'
import Header
import putSetting}
import React
import Sidebar
import {getSetting

function Settings() {
  const usdt = React.useRef()

  const onSubmit = (e) => {
    e.preventDefault()
    putSetting({"data": {"usdt": usdt.current.value}})
    sleep
    window.location.reload()
  }
  React.useEffect(()=>{
    getSetting().then((data)=>{
      usdt.current.value = data["data"]["usdt"]
    })
  }, [])

  return (
    <div className="flex h-[100dvh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <div className="sm:flex sm:justify-between sm:items-center mb-5">
              <div className="mb-4 sm:mb-0">
                <h1 className="text-2xl md:text-3xl text-slate-800 dark:text-slate-100 font-bold">Settings ✨</h1>
              </div>
            </div>
            <form onSubmit={onSubmit} method="POST">
            <div>
              <div>
                <label className="block text-sm font-medium mb-1" htmlFor="small">
                  USDT
                </label>
                <input id="small" className="form-input w-full px-2 py-1" type="text"  ref={usdt}/>
              </div>
            </div>

            <div className="m-1.5">
              <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type={"submit"}>Update</button>
            </div>
              </form>
          </div>
        </main>

      </div>

    </div>
  );
}

export default Settings;