import React from "react";
import { ServicesContainer, ServicesH1, ServicesText, ServicesWrapper, ServicesCard, ServicesIcon, ServicesH2, ServicesP } from "./ServicesElements";
import Icon1 from "../../images/space.svg"
import Icon2 from "../../images/online.svg"
import Icon3 from "../../images/real-time.svg"
import { Link } from "react-router-dom";

const Services = () => {
  return (
    <ServicesContainer id="services">
      <ServicesH1>Our Services</ServicesH1>
      <ServicesWrapper>
        <a
          href="https://appuctagent-6wrhtpgivzdlubgcvlu6fs.streamlit.app/"
          style={{ textDecoration: "none", color: "inherit" }}
          target="_blank" rel="noopener noreferrer"
        >
          <ServicesCard>
            <ServicesIcon src={Icon1} />

            <ServicesH2>Product Analyst</ServicesH2>
            <ServicesP>
              AI that Analyze the customer complainst, delivering swift and accurate solutions
            </ServicesP>

          </ServicesCard>
        </a>
        <a
          href="https://research-agent-nnz9dtssqnbb3ymphtb8bz.streamlit.app/"
          style={{ textDecoration: "none", color: "inherit" }}
          target="_blank" rel="noopener noreferrer"
        >
          <ServicesCard>
            <ServicesIcon src={Icon2} />

            <ServicesH2>TrendWise</ServicesH2>
            <ServicesP>
              Get real-time insights on market trends, outpace competitors, and make informed moves that matter.
            </ServicesP>

          </ServicesCard>
        </a>

        {/* <Link to="/ai_agent" style={{ textDecoration: "none" }}> */}
        <a
          href="https://customer-agent-mbzag6si83giqrq6cmcnuk.streamlit.app/"
          style={{ textDecoration: "none", color: "inherit" }}
          target="_blank" rel="noopener noreferrer"
        >
          <ServicesCard>
            <ServicesIcon src={Icon3} />

            <ServicesH2>RealVoice Helper</ServicesH2>
            <ServicesP>
              Your attentive voice assistant that listens, understands, and acts in real-time to meet your needs.
            </ServicesP>
          </ServicesCard>
        </a>

        {/* </Link> */}
        <Link to="/ExecutiveAssistant" style={{ textDecoration: "none" }}>
          <ServicesCard>
            <ServicesIcon src={Icon3} />

            <ServicesH2>Executive Assistant</ServicesH2>
            <ServicesP>
              Boost your business smarts your AI buddy that sharpens tasks and shapes ideas for better decisions.
            </ServicesP>

          </ServicesCard>
        </Link>
      </ServicesWrapper>
    </ServicesContainer>
  );
};

export default Services;

