// import React from "react";
import React, { useState } from "react";

const App = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("csvFile", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        setMessage("File uploaded! PDFs generated successfully.");
      } else {
        setMessage("Error: " + data.error);
      }
    } catch (error) {
      setMessage("Upload failed.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Upload a CSV File</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
        Upload
      </button>
      <p>{message}</p>
    </div>
  );
};

export default App;
