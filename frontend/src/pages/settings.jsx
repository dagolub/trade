import React, { useRef, useEffect } from 'react';
import Header from '../partials/Header';
import Sidebar from '../partials/Sidebar';
import { getSetting, putSetting } from '../services/api';

function Settings() {
  const usdt = useRef('');

  const onSubmit = async (e) => {
    e.preventDefault();
    await putSetting({ data: { usdt: usdt.current.value } });
    window.location.reload();
  };

  useEffect(() => {
    async function fetchSetting() {
      const data = await getSetting();
      usdt.current.value = data.data.usdt;
    }
    fetchSetting();
  }, []);

  return (
    <div className="flex h-[100vh] overflow-hidden">
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

                </div>
              </div>

              <div className="m-1.5">
                <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">
                  Update
                </button>
              </div>
            </form>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Settings;
