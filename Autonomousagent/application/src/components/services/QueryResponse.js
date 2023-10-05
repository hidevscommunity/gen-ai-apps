
import styled from 'styled-components';

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { MdEmail } from 'react-icons/md';
import { AiOutlineLoading3Quarters } from 'react-icons/ai';

// Styled components
const Container = styled.div`
    width: 100%;
    max-height: 400px;
    width: 1100px;
    padding: 20px;
    overflow-y: scroll;
    background-color: #B05FFD;
    border-radius: 8px;
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
    color:white
`;

const InputContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
    @media (min-width: 768px) {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
`;

const Input = styled.input`
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-bottom: 10px;
    @media (min-width: 768px) {
        margin-bottom: 0;
        width: 60%;
    }
`;

const EmailInput = styled.input`
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-bottom: 10px;
    @media (min-width: 768px) {
        width: 35%;
        margin-left: 20px;
    }
`;

const SubmitButton = styled.button`
border: none;
background-color: white !important;
color: #B05FF;
padding: 8px 12px;
border-radius: 5px;
cursor: pointer;
margin-top: 10px; 
`;

const Loading = styled.p`
    font-style: italic;
    color: #777;
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

const ResponsesList = styled.div`
    flex: 1;
    margin-right: 20px;
    max-width: 400px;
    @media (min-width: 768px) {
        flex: none;
        margin-right: 0;
    }
`;

const ResponseContent = styled.div`
    flex: 2;
    max-width: 400px;
    margin-top: 20px;
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

const EmailNotifyButton = styled.button`
    background-color: white;
    color: #B05FFD;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
`;

const EmailModal = styled.div`
    width: 100%;
    max-width: 400px;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
`;

const EmailModalContent = styled.div`
    h2 {
        font-size: 18px;
        margin-bottom: 10px;
    }

    p {
        font-size: 14px;
        margin-bottom: 20px;
    }
`;

const SendButton = styled.button`
    border: none;
    background-color: white !important;
    color: #B05FF;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px; 
`;



const Support = () => {
    const [query, setQuery] = useState('');
    const [responses, setResponses] = useState([]);
    const [selectedResponse, setSelectedResponse] = useState('');
    const [responseContent, setResponseContent] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // New states for email notification
    const [emailModalOpen, setEmailModalOpen] = useState(false);
    const [userEmail, setUserEmail] = useState('');



    const fetchResponses = async () => {
        setIsLoading(true);
        try {
            const response = await axios.get('https://muzammil002.pythonanywhere.com/responses');
            setResponses(response.data.result);
        } catch (error) {
            console.error("Error fetching responses:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchResponseContent = async (responseName) => {
        setIsLoading(true);
        try {
            const response = await axios.get(`https://muzammil002.pythonanywhere.com/responses/${responseName}`);
            if (response.data.status === "success") {
                setResponseContent(response.data.result);
            } else {
                setResponseContent("Response not found");
            }
        } catch (error) {
            console.error("Error fetching response content:", error);
            setResponseContent("An error occurred while fetching response");
        } finally {
            setIsLoading(false);
        }
    };


    const handleQueryChange = (event) => {
        setQuery(event.target.value);
    };



    const handleSupportRequest = async () => {
        setIsLoading(true);
        const response = await axios.post('https://muzammil002.pythonanywhere.com/support', { query, email: userEmail });
        fetchResponses(); // This will fetch and update the responses



    };

    // Handler for opening the email modal
    const handleEmailModalOpen = () => {
        setEmailModalOpen(true);
    };

    // Handler for submitting email and sending notification
    const handleEmailSubmit = async () => {
        setIsLoading(true);
        setEmailModalOpen(false);
        // Add logic to send the email here if needed
        setIsLoading(false);
    };

    const ref = useRef(null);
    const scrollToBottom = () => {
        const lastChildElement = ref.current?.lastElementChild;
        lastChildElement?.scrollIntoView({ behavior: 'smooth' });
    };
    useEffect(() => {
        fetchResponses();
        scrollToBottom();
    }, []);

    return (
        <Container ref={ref}>
            {/* <ResponsiveContainer> */}

            <Title>Autonomous Customer Support</Title>
            <InputContainer>
                <Input
                    type="text"
                    value={query}
                    onChange={handleQueryChange}
                    placeholder="Enter a customer query"
                />
                <EmailInput
                    type="email"
                    value={userEmail}
                    onChange={(e) => setUserEmail(e.target.value)}
                    placeholder="Enter your email (optional)"
                />
            </InputContainer>
            <SubmitButton onClick={handleSupportRequest}>
                {isLoading ? (
                    <AiOutlineLoading3Quarters className="loading-icon" />
                ) : (
                    "Submit Request"
                )}
            </SubmitButton>
            {isLoading && <Loading>Loading...</Loading>}

            <ResponsesContainer>
                <ResponsesList>
                    <h2 style={{ color: "white" }}>Recently Answered</h2>
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
                    <h2 style={{ color: "white" }}>Response</h2>
                    {isLoading ? (
                        <Loading>Loading response...</Loading>
                    ) : (
                        <>
                            <p>{responseContent}</p>
                            {responseContent !== "Response not found" && (
                                <EmailNotifyButton onClick={handleEmailModalOpen}>
                                    <MdEmail className="email-icon" />
                                    Notify Me by Email
                                </EmailNotifyButton>
                            )}
                        </>
                    )}
                </ResponseContent>

                {emailModalOpen && (
                    <EmailModal>
                        <EmailModalContent>
                            <h2>Get Email Notification</h2>
                            <p>Enter your email address to receive a notification when your query is answered:</p>
                            <EmailInput
                                type="email"
                                value={userEmail}
                                onChange={(e) => setUserEmail(e.target.value)}
                                placeholder="Enter your email"
                            />
                            <SendButton onClick={handleEmailSubmit}>Send Notification</SendButton>
                        </EmailModalContent>
                    </EmailModal>
                )}
            </ResponsesContainer>

            {/* </ResponsiveContainer> */}
        </Container>
    );
};

export default Support;