import React, { useState, useEffect } from "react";

function ProcessingBlink() {
  const [dots, setDots] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length < 6 ? prev + "." : ""));
    }, 500); // changes every 500ms

    return () => clearInterval(interval); // cleanup on unmount
  }, []);

  return <div className="text-info fw-semibold">Processing{dots}</div>;
}

export default ProcessingBlink;
