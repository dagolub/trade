import React from 'react'; // Import React
import Currency from '../partials/dashboard/Currency'; // Import Currency component
import Header from '../partials/Header'; // Import Header component
import Sidebar from '../partials/Sidebar'; // Import Sidebar component
import {getUserMe} from  '../services/api'
function Dashboard() {
  const [btc, setBTC] = React.useState(0)
  const [ltc, setLTC] = React.useState(0)
  const [usdt, setUSDT] = React.useState(0)
  const [eth, setETH] = React.useState(0)

  React.useEffect(() => {
    getUserMe().then((data)=>{
      if ( data.bal ) {
        setBTC(data.bal["btc"])
        setLTC(data.bal["ltc"])
        setUSDT(data.bal["usdt"])
        setETH(data.bal["eth"])
      }
    })
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
              <Currency currency="BTC" amount={btc} />
              <Currency currency="LTC" amount={ltc} />
              <Currency currency="USDT" amount={usdt} />
              <Currency currency="ETH" amount={eth} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
