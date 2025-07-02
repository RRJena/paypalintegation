import { useEffect, useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export default function App() {
  const [amount, setAmount] = useState('5.00');
  const [currency, setCurrency] = useState('USD');

  //Automatically capture payment after approval
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const success = params.get("success");
    const token = params.get("token");

    if (success === "true" && token) {
      console.log("Payment approved. Capturing...");

      axios.post(`${API_BASE}/pay/capture/${token}`)
        .then(res => {
          console.log("Payment Captured:", res.data);
          alert("Payment Captured Successfully!");
        })
        .catch(err => {
          console.error("Capture Failed:", err);
          alert("Payment Capture Failed!");
        });

      //Clean the URL
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  const handleOneTimePayment = async () => {
    const res = await axios.post(`${API_BASE}/pay/one-time`, {
      amount: parseFloat(amount),
      currency,
      return_url: window.location.href + '?success=true',
      cancel_url: window.location.href + '?cancel=true'
    });
    const approvalUrl = res.data.links.find(l => l.rel === 'approve')?.href;
    window.location.href = approvalUrl;
  };

  const handleSubscription = async () => {
    const res = await axios.post(`${API_BASE}/pay/recurring`, {
      plan_name: '1-Minute Demo Plan',
      price: parseFloat(amount),
      currency,
      return_url: window.location.href + '?success=true',
      cancel_url: window.location.href + '?cancel=true'
    });
    const approvalUrl = res.data.links.find(l => l.rel === 'approve')?.href;
    window.location.href = approvalUrl;
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white shadow-lg rounded-xl p-6 max-w-md w-full space-y-4">
        <h1 className="text-xl font-bold text-center">PayPal Payment</h1>
        <div>
          <label className="block mb-1 font-medium">Amount:</label>
          <input
            type="number"
            value={amount}
            onChange={e => setAmount(e.target.value)}
            className="w-full border p-2 rounded"
            step="0.01"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Currency:</label>
          <select
            value={currency}
            onChange={e => setCurrency(e.target.value)}
            className="w-full border p-2 rounded"
          >
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="INR">INR</option>
          </select>
        </div>
        <div className="flex flex-col gap-2">
          <button
            onClick={handleOneTimePayment}
            className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Pay One-Time
          </button>
          <button
            onClick={handleSubscription}
            className="bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Subscribe (1-Minute Plan)
          </button>
        </div>
      </div>
    </div>
  );
}
