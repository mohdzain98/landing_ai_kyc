import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UserState from "./context/UserState";
import Navbar from "./components/Navbar";
import Alert from "./components/Alert";
import Scrolltotop from "./components/Scrolltotop";
import Home from "./pages/home/Home";
import About from "./pages/About";
import Outcomes from "./pages/Outcomes";

function App() {
  const [alert, setAlert] = useState(null);

  const showAlert = (message, type) => {
    setAlert({
      msg: message,
      type: type,
    });
    setTimeout(() => {
      setAlert(null);
    }, 3500);
  };
  return (
    <>
      <UserState prop={{ showAlert }}>
        <Router>
          <Navbar />
          <Scrolltotop />
          <Alert alert={alert} />
          <Routes>
            <Route
              exact
              path="/"
              element={<Home prop={{ showAlert }} />}
            ></Route>
            <Route
              exact
              path="/about"
              element={<About prop={{ showAlert }} />}
            ></Route>
            <Route
              exact
              path="/outcomes"
              element={<Outcomes prop={{ showAlert }} />}
            ></Route>
          </Routes>
        </Router>
      </UserState>
    </>
  );
}

export default App;
