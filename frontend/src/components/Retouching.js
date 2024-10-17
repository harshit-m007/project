import React, { useState } from 'react';
import "./Retouching.css";
import axios from 'axios';

const UploadForm = () => {
  const [pdf, setPdf] = useState(null);
  const [question, setQuestion] = useState('');
  const [summary, setSummary] = useState('');
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const [answer, setAnswer] = useState('');

  const handlePdfChange = (e) => {
    setPdf(e.target.files[0]);
  };

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!pdf) {
      alert('Please upload a PDF');
      return;
    }

    const formData = new FormData();
    formData.append('pdf', pdf);
    formData.append('question', question);

    try {
      const response = await axios.post('http://localhost:9000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSummary(response.data.summary);
      setSuggestedQuestions(response.data.suggested_questions);
      setAnswer(response.data.answer || '');
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <h1>Upload PDF and Ask a Question</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handlePdfChange} />
        <input
          type="text"
          placeholder="Enter your question (optional)"
          value={question}
          onChange={handleQuestionChange}
        />
        <button type="submit">Submit</button>
      </form>
      {summary && (
        <div>
          <h2>Summary:</h2>
          <p>{summary}</p>
        </div>
      )}
      {suggestedQuestions.length > 0 && (
        <div>
          <h2>Suggested Questions:</h2>
          <ul>
            {suggestedQuestions.map((q, index) => (
              <li key={index}>{q}</li>
            ))}
          </ul>
        </div>
      )}
      {answer && (
        <div>
          <h2>Answer:</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default UploadForm;






