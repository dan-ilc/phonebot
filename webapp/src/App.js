import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function SayItApp() {
  const [enteredPhoneNumber, setEnteredPhoneNumber] = useState('');
  const [messageContent, setMessageContent] = useState('');
  const [apiResponse, setApiResponse] = useState(null);

  const handleSayItClick = async (event) => {
    event.preventDefault();

    if (!enteredPhoneNumber || !messageContent) {
      alert('Please enter both phone number and message.');
      return;
    }
    // hardcoded port
    const apiURL = `http://127.0.0.1:8000/voicecall?destination_number=${encodeURIComponent(enteredPhoneNumber)}&message=${encodeURIComponent(messageContent)}`;
    console.log('API URL:', apiURL);
    // TODO: Catch the errors here instead of logging to console
    // TODO2: catch the case where the API is down
    const response = await fetch(apiURL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phoneNumber: enteredPhoneNumber, message: messageContent }),
    });

    if (response.ok) {
      setApiResponse(response.status);
    } else {
      const errorResponse = await response.json();
      setApiResponse({ status: response.status, message: errorResponse.detail });
    }
  };

  useEffect(() => {
    if (apiResponse !== null) {
      const timeoutId = setTimeout(() => setApiResponse(null), 2000);
      return () => clearTimeout(timeoutId);
    }
  }, [apiResponse]);

  return (
    <div className="container mt-5">
      <h1 className="display-4 mb-4">Call the doctor!</h1>
      <form onSubmit={handleSayItClick}>
        <div className="mb-3">
          <label htmlFor="phone-number" className="form-label">Phone Number:</label>
          <input
            type="tel"
            className="form-control"
            id="phone-number"
            value={enteredPhoneNumber}
            onChange={(event) => setEnteredPhoneNumber(event.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="message" className="form-label">Message:</label>
          <textarea
            className="form-control"
            id="message"
            value={messageContent}
            onChange={(event) => setMessageContent(event.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Say it!
        </button>
      </form>
      {apiResponse === 200 && <p className="text-success mt-3">Success!</p>}
      {apiResponse !== 200 && apiResponse !== null && (
        <p className="text-danger mt-3">Error: {apiResponse.message}</p>
      )}
    </div>
  );
}

export default SayItApp;
