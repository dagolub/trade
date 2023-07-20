import React from 'react';
import { NavLink } from 'react-router-dom';

import SidebarLinkGroup from './SidebarLinkGroup';

function Sidebar() {
    const a_class = 'block transition duration-150 truncate text-slate-400 hover:text-slate-200';
    const span_class = "text-sm font-medium lg:opacity-0 lg:sidebar-expanded:opacity-100 2xl:opacity-100 duration-200"
    const li_class = "mb-1 last:mb-0"
    const div_class = "flex flex-col absolute z-40 left-0 top-0 lg:static lg:left-auto lg:top-auto lg:translate-x-0 h-[100dvh] overflow-y-scroll lg:overflow-y-auto no-scrollbar w-64 lg:w-20 lg:sidebar-expanded:!w-64 2xl:!w-64 shrink-0 bg-slate-800 p-4 transition-all duration-200 ease-in-out"
  return (
    <div className="min-w-fit">
      <div id="sidebar" className={div_class}>
         <NavLink end to="/" className="block">
           <table width="100px">
             <tbody>
             <tr>
               <td>Cryptex</td>
               <td><img src="/imgs/cp.svg"  width="24px" height="24px" alt="Logo" /></td>
             </tr>
             </tbody>
           </table>
          </NavLink>
        <div className="space-y-8">
          <div>
            <ul className="mt-3">
              <SidebarLinkGroup>
                {() => {
                  return (
                    <React.Fragment>
                      <div className="lg:hidden lg:sidebar-expanded:block 2xl:block">
                        <ul className={`pl-9 mt-1`}>

                            <li className={li_class}><a href="/users/list" className={a_class}><span className={span_class}>Users</span></a></li>
<li className={li_class}>
    <a href="/wallets/list" className={a_class}>
        <span className={span_class}>
            Wallets
        </span>
    </a>
</li>
<li className={li_class}>
    <a href="/transactions/list" className={a_class}>
        <span className={span_class}>
            Transactions
        </span>
    </a>
</li>
<li className={li_class}>
    <a href="/deposits/list" className={a_class}>
        <span className={span_class}>
            Deposits
        </span>
    </a>
</li>


                        </ul>
                      </div>
                    </React.Fragment>
                  );
                }}
              </SidebarLinkGroup>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;