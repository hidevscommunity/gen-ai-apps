
import styled from 'styled-components';
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { AiOutlineLoading3Quarters } from 'react-icons/ai';
const Container = styled.div`
// width: 100%;
height: 400px;

width: 1100px;
padding: 20px;
overflow-y: scroll;
background-color: #B05FFD;
border-radius: 16px;
display: flex;
flex-direction: column;
// align-items: center;
margin: 0 auto;
@media (max-width: 1200px) {
  width: 100%;
}
`;

const Title = styled.h1`
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
`;

const InputContainer = styled.div`
display: flex;
flex-direction: column;
align-items: center;
margin-bottom: 20px;
width: 100%;

`;

const Input = styled.input`
padding: 10px;
border: 1px solid #ccc;
border-radius: 4px;
margin-bottom: 10px;
width: 100%;
@media (min-width: 768px) {
  width: 60%;
  margin-bottom: 0;
}
`;

const SubmitButton = styled.button`
border: none;
background-color: white !important;
color: #B05FF;
padding: 8px 12px;
border-radius: 5px;
cursor: pointer;
margin: 20px;
width:250px;
display: flex;
// align-items: center;
justify-content: center;
.loading-icon {
  margin-right: 5px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
`;

const Loading = styled.p`
  font-style: italic;
  color: #777;
  height: 40px;
`;

const ResponsesList = styled.div`
flex: 1;
margin-right: 0;
margin-bottom: 20px;
  @media (min-width: 768px) {
    flex: none;
    margin-right: 20px;
    margin-bottom: 0;
  }
`;

const ResponseContent = styled.div`
  flex: 2;
 
  width:50%
  @media (min-width: 768px) {
    flex: none;
    margin-top: 0;
  }
`;

const ResponseItem = styled.p`
cursor: pointer;
margin-bottom: 10px;
${(props) =>
  props.selected &&
  `
    text-decoration: underline;
    color: #007bff;
`}
`;
const ResponsesContainer = styled.div`
margin-top: 50px;
width: 100%;
display: flex;
flex-direction: column;
align-items: center;
justify-content:space-between;


@media (min-width: 768px) {
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
}
`;



const ResearchApp = () => {
  const [query, setQuery] = useState('');
  const [responses, setResponses] = useState([]);
  const [responseContent, setResponseContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedResponse, setSelectedResponse] = useState('');


  const fetchResearchResults = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('https://muzammil002.pythonanywhere.com/researched');
      if (response.status === 200) {
        setResponses(response.data.result);
        console.log('Fetched responses:', response.data.result);
      } else {
        console.error('Received unexpected response:', response);
      }
    } catch (error) {
      console.error('Error fetching research results:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchResponseContent = async (responseName) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`https://muzammil002.pythonanywhere.com/researched/${responseName}`);
      if (response.data.status === 'success') {
        setResponseContent(response.data.result);
        console.log('Fetched response content:', response.data.result);
      } else {
        setResponseContent('Response not found');
      }
    } catch (error) {
      console.error('Error fetching response content:', error);
      setResponseContent('An error occurred while fetching response');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const performResearch = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post('https://muzammil002.pythonanywhere.com/research', { research: query });
      if (response.data.status === 'success') {
        setResponseContent(response.data.result);
      } else {
        setResponseContent('No research results found');
      }
    } catch (error) {
      console.error('Error performing research:', error);
      setResponseContent('An error occurred while performing research');
    } finally {
      setIsLoading(false);
    }
  };

  const ref = useRef(null);
  const scrollToBottom = () => {
    const lastChildElement = ref.current?.lastElementChild;
    lastChildElement?.scrollIntoView({ behavior: 'smooth' });
  };
  useEffect(() => {
    fetchResearchResults();
    scrollToBottom();
  }, []);

  return (
    <Container ref={ref}>
      <InputContainer>
      <Title>Market Research Product</Title>

        <Input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Enter a product category"
        />
      <SubmitButton onClick={performResearch}>
        {isLoading ? (
          <AiOutlineLoading3Quarters className="loading-icon" />
        ) : (
          'Fetch Responses'
        )}
      </SubmitButton>
      </InputContainer>

       {/* <ContentContainer> */}
        <ResponsesContainer>
          <ResponsesList>
          <h2 style={{ color: "white" }}>Recently Research</h2>
          {responses.map((response) => (
                        <ResponseItem
                            key={response}
                            onClick={() => fetchResponseContent(response)}
                            selected={response === selectedResponse}
                        >
                            {response}
                        </ResponseItem>
                    ))}
          </ResponsesList>
         <ResponseContent>
         <h2 style={{ color: "white" }}>Research</h2>
            {isLoading ? (
              <Loading>Loading response content...</Loading>
            ) : (
              <p>{responseContent}</p>
            )}
          </ResponseContent>
         </ResponsesContainer>
      {/* </ContentContainer>  */}
    </Container>
  );
};

export default ResearchApp;
