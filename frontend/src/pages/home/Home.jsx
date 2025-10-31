import React from "react";
import Main from "./components/Main";
import Task from "./components/Task";
import Footer from "./components/Footer";

const Home = (props) => {
  const { showAlert } = props.prop;
  return (
    <>
      <Main prop={{ showAlert }} />
      <Task prop={{ showAlert }} />
      <Footer />
    </>
  );
};

export default Home;
