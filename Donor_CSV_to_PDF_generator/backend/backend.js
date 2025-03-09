const express = require("express");
const multer = require("multer");
const { exec } = require("child_process");
const cors = require("cors");
const path = require("path");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(cors());
app.use(express.json());

app.post("/upload", upload.single("csvFile"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ success: false, error: "No file uploaded." });
  }

  const filePath = path.join(__dirname, req.file.path);

  // Run Python script to generate PDFs
  exec(`python3 generate_pdf.py ${filePath}`, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ success: false, error: stderr });
    }
    res.json({ success: true, message: "PDFs generated!", output: stdout });
  });
});

app.listen(5000, () => console.log("Server running on port 5000"));
