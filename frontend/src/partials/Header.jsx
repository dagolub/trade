import React, {useEffect, useState} from 'react';
import ThemeToggle from '../components/ThemeToggle';
import UserMenu from '../components/DropdownProfile';
import {deleteToken} from "../services/token";
import {getUserMe} from "../services/api";

function Header() {
    const [full_name, setFullName] = useState();
    const [email, setEmail] = useState();
    const [user_id, setUserId] = useState();

    useEffect(() => {
        getUserMe().then(data => {
            if (data.hasOwnProperty('response') && data.response.status === 403) {
                window.location.href = "/signin"
            } else if (data.hasOwnProperty('response') && data.response.status === 404) {
                    setFullName("404");
                    setEmail(data["404"]);
                    setUserId(data["404"]);
            } else {
                if (data) {
                    setFullName(data["full_name"]);
                    setEmail(data["email"]);
                    setUserId(data["id"]);
                } else {
                    alert("Before delete")
                    deleteToken();
                }
            }
        })
    }, []);
    return (
        <header
            className="sticky top-0 bg-white dark:bg-[#182235] border-b border-slate-200 dark:border-slate-700 z-30">
            <div className="px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16 -mb-px">
                    <div className="flex"></div>
                    <div className="flex items-center space-x-3">
                        <ThemeToggle/>
                        <hr className="w-px h-6 bg-slate-200 dark:bg-slate-700 border-none"/>
                        <UserMenu align="right" full_name={full_name}/>
                    </div>
                </div>
            </div>
        </header>
    );
}

export default Header;
