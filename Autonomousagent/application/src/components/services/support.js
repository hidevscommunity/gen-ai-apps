import React, { useState } from "react";
import { Navbar } from "../navbar";
import { Sidebar } from "../sidebar";
import styled from "styled-components";
// import Chatbot from "./Chatbot";
import Video from "../../videos/bgvideo.mp4"
// import Icon2 from "../images/online.svg"
import QueryResponse from "./QueryResponse"

const Support = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
    <Sidebar isOpen={isOpen} toggle={toggle} />
    <Navbar toggle={toggle} />
    <HeroContainer>
      <HeroBg>
        <VideoBg autoPlay loop muted src={Video} type="video/mp4" />
      </HeroBg>
      <HeroContent>
      
        <ServicesContainer id="services">
          
          {/* {selectedService === "callagent" && <h1>Call Agent</h1>} */}
          <QueryResponse />
        </ServicesContainer>
      </HeroContent>
    </HeroContainer>
  </div>


  );
};



const HeroContainer = styled.div`
  background: #0c0c0c;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 30px;
  height: 100vh;
  position: relative;
  z-index: 1;

  &:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: linear-gradient(
        180deg,
        rgba(0, 0, 0, 0.2) 0%,
        rgba(0, 0, 0, 0.6) 100%
      ),
      linear-gradient(180deg, rgba(0, 0, 0, 0.2) 0%, transparent 100%);
    z-index: 2;
  }
`;

const HeroContent = styled.div`
  z-index: 3;
  max-width: 1200px;
  position: absolute;
  padding: 8px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const HeroBg = styled.div`
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
`;

const VideoBg = styled.video`
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #232a34;
  opacity: 0.5;
`;

const ServicesContainer = styled.div`
  min-height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 50px 0;

  @media screen and (max-width: 768px) {
    min-height: 1100px;
  }

  @media screen and (max-width: 480px) {
    min-height: 1300px;
  }
`;

const ServiceButtons = styled.div`
  display: flex;
  margin-top: 30px;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
  }
`;

const ServiceButton = styled.button`
  background-color: ${({ selected }) => (selected ? "#B05FFD" : "white")};
  color: ${({ selected }) => (selected ? "white" : "#010606")};
  border: 2px solid #010606;
  padding: 10px 20px;
  font-size: 1rem;
  margin-top: 70px;
  cursor: pointer;

  &:hover {
    background-color: #B05FFD;
    color: white;
  }

  @media (max-width: 768px) {
    margin: 5px 0;
  }
`;



export default Support;
