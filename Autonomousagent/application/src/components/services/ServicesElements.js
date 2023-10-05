import styled from "styled-components";

export const ServicesContainer = styled.div`
    min-height: 800px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #010606;
    padding: 50px 0;

    @media screen and (max-width: 768px) {
        min-height: 1100px;
    }

    @media screen and (max-width: 480px) {
        min-height: 1300px;
    }
`;

export const ServicesWrapper = styled.div`
display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: repeat(2, 1fr);
grid-column-gap: 5px;
grid-row-gap: 4px;
  width: 100%;
  max-width: 1200px;



  @media screen and (max-width: 1000px) {
    grid-template-columns: 1fr 1fr;
    padding: 20px 50px;
}

@media screen and (max-width: 768px) {
    grid-template-columns: 1fr;
    //padding: 0 20px;
    padding: 20px 50px;
}
  
  @media screen and (max-width: 480px) {
    grid-template-columns: 1fr;
    padding: 20px 50px;
  }
`;

export const ServicesCard = styled.div`
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
  width: 100%;
  // max-width: 300px; 
  height: 70%;
  margin: 30px;
  padding: 30px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease-in-out;

  &:hover {
    transform: scale(1.02);
    transition: all 0.3s ease-in-out;
  }
  @media screen and (max-width: 960px) {
  display: flex;
  height: 90%;
    flex-direction: column;
    margin: 0px;
  }
  
  @media screen and (max-width: 768px) {
  display: flex;
  margin: 0px;

    flex-direction: column;
    height: 90%;

  }
  
  @media screen and (max-width: 480px) {
  display: flex;

    flex-direction: column;
    max-width: 300px;
    height: 90%;
    margin: 0px;

  }
`;



export const ServicesH1 = styled.h1`
    font-size: 2.5rem;
    color: #fff;
    margin-bottom: 64px;
    text-decoration: none;
    @media screen and (max-width: 480px) {
        font-size: 2rem;
    }

`

export const ServicesIcon = styled.img`
  height: 80px;
  width: 80px;
  margin-bottom: 10px;
`;

export const ServicesH2 = styled.h2`
    color:black;
  font-size: 1.5rem;
  margin-bottom: 10px;
  
`;

export const ServicesP = styled.p`
color:#B05FFB;
  font-size: 1rem;
  text-align: center;
  max-width:300px;
`;
export const ServiceButtons = styled.div`
  display: flex;
  margin-bottom: 20px;
`


export const ServiceButton = styled.button`
  background-color: ${({ selected }) => (selected ? "#010606" : "white")};
  color: ${({ selected }) => (selected ? "white" : "#010606")};
  border: 2px solid #010606;
  padding: 10px 20px;
  font-size: 1rem;
  margin-right: 10px;
  cursor: pointer;

  &:hover {
    background-color: #010606;
    color: white;
  }
`
