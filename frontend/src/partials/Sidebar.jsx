import React, {useEffect, useState} from 'react'
import {NavLink} from 'react-router-dom'
import {getUserMe} from "../services/api"

function Sidebar() {
    const div_class =
        'flex flex-col absolute z-40 left-0 top-0 lg:static lg:left-auto lg:top-auto lg:translate-x-0 h-[100vh] overflow-y-scroll lg:overflow-y-auto no-scrollbar w-64 lg:w-20 lg:sidebar-expanded:!w-64 2xl:!w-64 shrink-0 bg-slate-800 p-4 transition-all duration-200 ease-in-out';

    const a_class =
        'block transition duration-150 truncate text-slate-400 hover:text-slate-200';
    const span_class =
        'text-sm font-medium lg:sidebar-expanded:opacity-100 2xl:opacity-100 duration-200';
    const li_class = 'mb-1 last:mb-0';
    const [superuser, setSuperUser] = useState();
    useEffect(() => {
        getUserMe().then(data => {
            if (data.hasOwnProperty('is_superuser')) {
                setSuperUser(data["is_superuser"])
            }
        })
    }, []);

    return (
        <div className="min-w-fit" style={{width: '150px'}}>
            <div id="sidebar" className={div_class} style={{width: '150px'}}>
                <NavLink end to="/" className="block">
                    <table width="100px">
                        <tbody>
                        <tr>
                            <td>PDF MAX</td>
                            <td>
                                <img
                                    src="/imgs/cp.svg"
                                    width="24px"
                                    height="24px"
                                    alt="Logo"
                                />
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </NavLink>
                <div className="space-y-8">
                    <ul className="mt-3">
                        {superuser &&
                            <li className={li_class}>
                                <NavLink to="/users/list" className={a_class}>
                                    <span className={span_class}>Users</span>
                                </NavLink>
                            </li>}
                        <li className={li_class}>
                            <NavLink to="/documents/list" className={a_class}>
                                <span className={span_class}>Documents</span>
                            </NavLink>
                        </li>
                        <li className={li_class}>
                            <NavLink to="/folders/list" className={a_class}>
                                <span className={span_class}>Folders</span>
                            </NavLink>
                        </li>

                    </ul>
                </div>
            </div>
        </div>
    );
}

export default Sidebar;
