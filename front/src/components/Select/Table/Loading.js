import React from "react"
import ScaleLoader from "react-spinners/ScaleLoader"

function Loading() {
  return (
    <div>
      <div
        style={{
          position: "fixed",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
        }}
      >
        <ScaleLoader
          color="#7ED321"
          height={35}
          width={4}
          radius={2}
          margin={2}
        />
      </div>
    </div>
  )
}

export default Loading
