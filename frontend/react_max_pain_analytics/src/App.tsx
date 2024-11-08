import React, { useState, useEffect } from "react";

import "./style.css";


function App() {
  const [ticker, setTicker] = useState("")
  const [response, setResponse] = useState("")

  const url = "http://localhost:8000/main_app/"
  
  useEffect(() => {
    fetchData()
    console.log(ticker)
  }, [ticker])


  const fetchData = () => {
    fetch(url)
      .then((res) => {
        return res.json()
      })
      .then((data) => {
        setResponse(data["message"])
      })
      .catch((error) => console.error("Error fetcing data:", error))
  }

  return (
      <div className="grid grid-cols-3 gap-4 w-screen h-screen box-border">
        <div className="bg-blue-400 w-full h-full p-2 ">
          <h1>ticker search</h1>
          <div className="p-2 w-full border-2 rounded-sm border-black bg-slate-50">
            <input className="w-full bg-slate-50 p-2" type="text" onChange={e => setTicker(e.target.value)} value={ticker}/>
          </div>
          <h1>{response}</h1>
        </div>
      
        <div className="bg-green-400"></div>
        <div className="bg-red-400"></div>
      </div>
  );
}

export default App;
