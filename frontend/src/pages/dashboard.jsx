import React from 'react'; // Import React
import Currency from '../partials/dashboard/Currency'; // Import Currency component
import Header from '../partials/Header'; // Import Header component
import Sidebar from '../partials/Sidebar'; // Import Sidebar component

function Dashboard() {
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
              <Currency currency="BTC" amount={0} />
              <Currency currency="LTC" amount={0} />
              <Currency currency="BCH" amount={0} />
              <Currency currency="USDT" amount={0} />
              <Currency currency="ETC" amount={0} />
              <Currency currency="ETH" amount={0} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
