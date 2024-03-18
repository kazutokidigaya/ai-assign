import React, { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";
import { PDFDocument } from "pdf-lib";
import "./App.css";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<
    { type: "question" | "answer"; content: string }[]
  >([]);

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files ? event.target.files[0] : null;
    if (!selectedFile) {
      toast.error("No file selected.");
      return;
    }
    if (selectedFile.size > 10 * 1024 * 1024) {
      // 10 MB
      toast.error("File size should not exceed 10 MB.");
      return;
    }

    try {
      const arrayBuffer = await selectedFile.arrayBuffer();
      const pdfDoc = await PDFDocument.load(arrayBuffer);
      const numberOfPages = pdfDoc.getPageCount();

      if (numberOfPages > 10) {
        toast.error("PDF should not have more than 10 pages.");
        return;
      }

      setFile(selectedFile); // File is valid, update the state
      toast.success("PDF uploaded successfully.");
    } catch (error) {
      console.error("Error processing PDF:", error);
      toast.error("Failed to process the PDF file.");
    }
  };

  const handleQuestionChange = (event: ChangeEvent<HTMLInputElement>) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file || !question) {
      toast.error("Please select a file and enter a question.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    setChatHistory((prev) => [
      ...prev,
      { type: "question", content: question },
    ]);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setChatHistory((prev) => [
        ...prev,
        { type: "answer", content: response.data.result },
      ]);
    } catch (error) {
      console.error("Error:", error);
      toast.error("Failed to get an answer. Please try again.");
    }
  };

  return (
    <div className="App">
      <Toaster position="top-right" />
      <h1>Chat Bot</h1>
      <form onSubmit={handleSubmit} className="form">
        <div>
          <label htmlFor="file">Upload PDF:</label>
          <input
            type="file"
            id="file"
            accept="application/pdf"
            onChange={handleFileChange}
          />
        </div>
        <div>
          <label htmlFor="question">Question:</label>
          <input
            type="text"
            id="question"
            value={question}
            onChange={handleQuestionChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      <div className="chat-history">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
