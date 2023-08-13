import Form from "../../components/users/from"
import Sidebar from "../../partials/Sidebar";
import {useParams} from "react-router-dom";
import {getUser, getOTP} from "../../services/api";
import React from "react";
import Header from "../../partials/Header";
function UsersEdit() {
    const { id } = useParams();
    const [full_name, setFullName] = React.useState("")
    const [email, setEmail] = React.useState("")
    const [is_active, setIsActive] = React.useState(false)
    const [is_superuser, setIsSuperUser] = React.useState(false)
    const [autotransfer, setAutoTransfer] = React.useState(false)
    const [otp, setOTP] = React.useState("")
    const [first_time, setFirstTime] = React.useState(false)
    React.useEffect(()=> {
        getUser(id).then((data)=> {
            if (!first_time) {
                setFullName(data.full_name)
                setEmail(data.email)
                setIsActive(data.is_active)
                setIsSuperUser(data.is_superuser)
                setAutoTransfer(data.autotransfer)
                setFirstTime(true)
            }
        }, [])
    })
    React.useEffect( ()=> {
        getOTP(email).then(data=> {
            if (data.code != "ERR_BAD_RESPONSE") {
                console.log("Image", data)
                setOTP(data)
            }
        })
    }, [email])
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <Header />
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form name={full_name}
                          email={email}
                          is_active={is_active}
                          is_superuser={is_superuser}
                          auto={autotransfer}
                          otp={otp}
                          id={id}
                    />
                </div>
            </main>
        </div>
    </div>)
}

export default UsersEdit