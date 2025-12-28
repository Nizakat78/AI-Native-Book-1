import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chatbot from '@site/src/components/Chatbot/Chatbot';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <Chatbot apiUrl="http://localhost:8000/api/v1/query" initialContextMode="full_book" />
    </>
  );
}