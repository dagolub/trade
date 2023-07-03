import React from 'react';

import UserImage01 from '../../images/user-28-07.jpg';
import UserImage02 from '../../images/user-28-11.jpg';

function Task01() {
  return (
    <div className="bg-white dark:bg-slate-800 shadow-lg rounded-sm border border-slate-200 dark:border-slate-700 p-4">
      {/* Body */}
      <div className="mb-3">
        {/* Title */}
        <h2 className="font-semibold text-slate-800 dark:text-slate-100 mb-1">Managing teams (book)</h2>
        {/* Content */}
        <div>
          <div className="text-sm">#7764 created by <a className="font-medium text-slate-800 hover:underline" href="#0">markus-james</a></div>
        </div>
      </div>
      {/* Footer */}
      <div className="flex items-center justify-between">
        {/* Left side */}
        <div className="flex shrink-0 -space-x-3 -ml-px">
          <a className="block" href="#0">
            <img className="rounded-full border-2 border-white dark:border-slate-800 box-content" src={UserImage01} width="28" height="28" alt="User 07" />
          </a>
          <a className="block" href="#0">
            <img className="rounded-full border-2 border-white dark:border-slate-800 box-content" src={UserImage02} width="28" height="28" alt="User 11" />
          </a>
        </div>
        {/* Right side */}
        <div className="flex items-center">
          {/* Like button */}
          <button className="flex items-center text-slate-400 dark:text-slate-500 hover:text-indigo-500  dark:hover:text-indigo-500 ml-3">
            <svg className="w-4 h-4 shrink-0 fill-current mr-1.5" viewBox="0 0 16 16">
              <path d="M14.682 2.318A4.485 4.485 0 0011.5 1 4.377 4.377 0 008 2.707 4.383 4.383 0 004.5 1a4.5 4.5 0 00-3.182 7.682L8 15l6.682-6.318a4.5 4.5 0 000-6.364zm-1.4 4.933L8 12.247l-5.285-5A2.5 2.5 0 014.5 3c1.437 0 2.312.681 3.5 2.625C9.187 3.681 10.062 3 11.5 3a2.5 2.5 0 011.785 4.251h-.003z" />
            </svg>
            <div className="text-sm text-slate-500 dark:text-slate-400">4</div>
          </button>
          {/* Replies button */}
          <button className="flex items-center text-slate-400 dark:text-slate-500 hover:text-indigo-500  dark:hover:text-indigo-500 ml-3">
            <svg className="w-4 h-4 shrink-0 fill-current mr-1.5" viewBox="0 0 16 16">
              <path d="M8 0C3.6 0 0 3.1 0 7s3.6 7 8 7h.6l5.4 2v-4.4c1.2-1.2 2-2.8 2-4.6 0-3.9-3.6-7-8-7zm4 10.8v2.3L8.9 12H8c-3.3 0-6-2.2-6-5s2.7-5 6-5 6 2.2 6 5c0 2.2-2 3.8-2 3.8z" />
            </svg>
            <div className="text-sm text-slate-500 dark:text-slate-400">7</div>
          </button>
          {/* Attach button */}
          <button className="text-slate-400 dark:text-slate-500 hover:text-indigo-500  dark:hover:text-indigo-500 ml-3">
            <svg className="w-4 h-4 shrink-0 fill-current mr-1.5" viewBox="0 0 16 16">
              <path d="M11 0c1.3 0 2.6.5 3.5 1.5 1 .9 1.5 2.2 1.5 3.5 0 1.3-.5 2.6-1.4 3.5l-1.2 1.2c-.2.2-.5.3-.7.3-.2 0-.5-.1-.7-.3-.4-.4-.4-1 0-1.4l1.1-1.2c.6-.5.9-1.3.9-2.1s-.3-1.6-.9-2.2C12 1.7 10 1.7 8.9 2.8L7.7 4c-.4.4-1 .4-1.4 0-.4-.4-.4-1 0-1.4l1.2-1.1C8.4.5 9.7 0 11 0zM8.3 12c.4-.4 1-.5 1.4-.1.4.4.4 1 0 1.4l-1.2 1.2C7.6 15.5 6.3 16 5 16c-1.3 0-2.6-.5-3.5-1.5C.5 13.6 0 12.3 0 11c0-1.3.5-2.6 1.5-3.5l1.1-1.2c.4-.4 1-.4 1.4 0 .4.4.4 1 0 1.4L2.9 8.9c-.6.5-.9 1.3-.9 2.1s.3 1.6.9 2.2c1.1 1.1 3.1 1.1 4.2 0L8.3 12zm1.1-6.8c.4-.4 1-.4 1.4 0 .4.4.4 1 0 1.4l-4.2 4.2c-.2.2-.5.3-.7.3-.2 0-.5-.1-.7-.3-.4-.4-.4-1 0-1.4l4.2-4.2z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Task01;