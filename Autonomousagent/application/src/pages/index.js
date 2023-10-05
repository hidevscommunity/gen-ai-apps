import React, { useState } from "react";
import HeroSection from "../components/heroSection";
import InfoSection from "../components/infoSection";
import { Navbar } from "./../components/navbar";
import { Sidebar } from "./../components/sidebar";

import Image1 from "../images/design-notes.svg";
import Image2 from "../images/space.svg";
import InfoSectionLight from "../components/infoSectionLight";
import Services from "../components/services";
import Footer from "../components/footer";

export const Home = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    // <>
    //   <Sidebar isOpen={isOpen} toggle={toggle} />
    //   <Navbar toggle={toggle} />
    //   <HeroSection />
    //   <InfoSection
    //     image={Image1}
    //     id="about"
    //     subtitle="Mauris tempor interdum"
    //     title="Proin condimentum diam"
    //     text="In luctus nibh nec metus placerat consectetur. Maecenas odio mi, ullamcorper at porta non, egestas vitae velit. Donec lacinia porta tristique. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis nec arcu nec diam posuere tincidunt. Nulla dignissim enim id nibh luctus, ullamcorper sagittis eros semper."
    //     btnText="Start today"
    //   />
    //   <InfoSectionLight
    //     image={Image2}
    //     id="discover"
    //     subtitle="Morbi iaculis enim"
    //     title="In hac habitasse"
    //     text="Phasellus porta sagittis sapien. Nam quis odio eu libero tempus rutrum. Suspendisse nec eros eget ex cursus rhoncus. Proin at velit quis ante pretium porta. Quisque pulvinar, elit et tincidunt ultricies, mauris odio luctus risus, vitae auctor elit risus a tortor. Nunc pulvinar purus id est rutrum vulputate. Mauris venenatis lectus vel nisi semper scelerisque."
    //     btnText="Explore"
    //   />
    //   <Services />
    //   <InfoSectionLight
    //     image={Image1}
    //     id="#"
    //     subtitle="Duis et lectus accumsan"
    //     title="Quisque dui justo"
    //     text="Cras et ligula eget neque ornare tempor et vitae est. Duis et lectus accumsan, mollis dui a, finibus metus. Quisque dui justo, ullamcorper eget luctus id, consectetur eget nunc. In quis arcu erat. Morbi consequat imperdiet lorem, porta porta erat hendrerit vel. Aliquam dignissim purus at dolor posuere euismod."
    //     btnText="Read more"
    //   />
    //   <Footer />
    // </>
    <>
      <Sidebar isOpen={isOpen} toggle={toggle} />
      <Navbar toggle={toggle} />
      <HeroSection />
      <InfoSection
        image={Image1}
        id="about"
        subtitle="AI-Powered Excellence Unleashed"
        title="Empower Your Business with Integrated AI Solutions"
        text="Experience the future of business transformation through our Integrated Business Intelligence and Customer Support Platform. Harnessing the power of AI, we seamlessly combine cutting-edge customer support, market research, and executive assistance to elevate your customer interactions, decode market trends, and revolutionize decision-making. From tailored support to data-driven insights, our platform empowers your business at every step. Welcome to a new era of efficiency, collaboration, and success.
  
  
  
  
  
          "
        btnText="Start today"
      />
      <InfoSectionLight
        image={Image2}
        id="discover"
        subtitle="Delve into Our Integrated AI Solution"
        title="Explore the Possibilities"
        text="Embark on a journey of discovery with our Integrated Business Intelligence and Customer Support Platform. Immerse yourself in the synergy of AI-driven customer support, market insights, and executive assistance. Uncover the realm where customer engagement meets informed decision-making, and where market trends reveal new pathways to success. Your business evolution starts here."
        btnText="Explore"
      />
      <Services />
      <InfoSectionLight
        image={Image1}
        id="benefits"
        subtitle="Unlock the Value"
        title="Maximize Your Business Potential"
        text="Elevate your business to new heights with our Integrated Business Intelligence and Customer Support Platform. Seamlessly combining AI-driven customer support, market research, and executive assistance, our platform empowers your teams to excel. Experience improved customer satisfaction, data-driven decision-making, streamlined collaboration, and enhanced operational efficiency. Discover a world where innovation meets success."
        btnText="Learn more"
      />

      <Footer />
    </>
  );
};
