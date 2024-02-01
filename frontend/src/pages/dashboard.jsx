import React from 'react'
import Header from '../partials/Header'
import Sidebar from '../partials/Sidebar'
function Dashboard() {
  React.useEffect(() => {
  },[])
  return (
    <div className="flex h-[100vh] overflow-hidden"> {/* Fix typo: Change h-[100dvh] to h-[100vh] */}
      <Sidebar />
      {/* Content area */}
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        {/* Site header */}
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <div className="grid grid-cols-12 gap-6">
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
