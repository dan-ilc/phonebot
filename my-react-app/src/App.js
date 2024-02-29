import React, { useState, useEffect } from 'react';

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
    const apiURL = `http://localhost:8000/voicecall?destination_number=${encodeURIComponent(enteredPhoneNumber)}&message=${encodeURIComponent(messageContent)}`;
    console.log('API URL:', apiURL);
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
    <div className="SayItApp" style={{ backgroundColor: '#673AB7', padding: '20px' }}>
      <h1>Say It!</h1>
      <form onSubmit={handleSayItClick}>
        <label htmlFor="phone-number">Phone Number:</label>
        <input
          type="tel"
          id="phone-number"
          value={enteredPhoneNumber}
          onChange={(event) => setEnteredPhoneNumber(event.target.value)}
          required
        />
        <br />
        <label htmlFor="message">Message:</label>
        <textarea
          id="message"
          value={messageContent}
          onChange={(event) => setMessageContent(event.target.value)}
          required
        />
        <br />
        <button
          type="submit"
          style={{ backgroundColor: '#800080', color: 'white', padding: '10px 20px', fontSize: '18px' }}
        >
          Say it!
        </button>
      </form>
      {apiResponse === 200 && <p style={{ color: 'green' }}>Success!</p>}
      {apiResponse !== 200 && apiResponse !== null && (
        <p style={{ color: 'red' }}>Error: {apiResponse.message}</p>
        
      )}
    </div>
  );
}

export default SayItApp;
