import AuthDecoration from "../images/auth-decoration.png"
import AuthImage from "../images/auth-image.jpg"
import React from "react"
import { Login } from "../services/api"; // Replace with the correct path
import { saveToken } from "../services/token"; // Replace with the correct path
import { showError } from "../utils"; // Replace with the correct path

function Signin() {
  const refEmail = React.useRef();
  const refPassword = React.useRef();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const authenticate = {
      'username': refEmail.current.value,
      'password': refPassword.current.value
    };

    let response = await Login(authenticate);
    if (response.status === 200) {
      saveToken(response.data.access_token);
      window.location.pathname = '/';
    } else {
      console.log(response);
    }

    return false;
  };

  return (
    <main className="bg-white dark:bg-slate-900">
      <div className="relative md:flex">
        {/* Content */}
        <div className="md:w-1/2">
          <div className="min-h-[100dvh] h-full flex flex-col after:flex-1">
            <div className="max-w-sm mx-auto w-full px-4 py-8">
              <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Welcome back! ✨</h1>
              {/* Form */}
              <form onSubmit={handleSubmit} method="POST">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1" htmlFor="email">Email Address</label>
                    <input id="email" className="form-input w-full" type="email" ref={refEmail} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1" htmlFor="password">Password</label>
                    <input id="password" className="form-input w-full" type="password" ref={refPassword} />
                  </div>
                </div>
                <div className="flex items-center justify-between mt-6">
                  <button className="btn btn-primary">Sign In</button>
                </div>
              </form>
            </div>
          </div>
        </div>
        {/* Image */}
        <div className="hidden md:block absolute top-0 bottom-0 right-0 md:w-1/2" aria-hidden="true">
          <img className="object-cover object-center w-full h-full" src={AuthImage} width="760" height="1024" alt="Authentication" />
          <img className="absolute top-1/4 left-0 -translate-x-1/2 ml-8 hidden lg:block" src={AuthDecoration} width="218" height="224" alt="Authentication decoration" />
        </div>
      </div>
    </main>
  );
}

export default Signin;
