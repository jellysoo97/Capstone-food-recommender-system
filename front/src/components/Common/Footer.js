import React from "react"

function Footer() {
  return (
    <div
      className="container-fluid p-4"
      style={{ background: "rgba(233, 220, 205, 0.5)" }}
    >
      <div className="container">
        <div className="row">
          <div className="col-4">
            <h5>
              <strong>Address</strong>
            </h5>
            <p>02450 서울특별시 동대문구 이문로 107</p>
          </div>
          <div className="col-4">
            <h5>
              <strong>Contact</strong>
            </h5>
            <p>Tel. 82-2-2173-2114</p>
          </div>
          <div className="col-4">
            <h5>
              <strong>ABOUT US</strong>
            </h5>
            <p>2022-1 종합설계 A4팀 Tech4All</p>
            <p>박소연, 신정현, 이수연, 하유정, 황정연</p>
          </div>
        </div>
        <div className="row">
          <div className="col-12">Copyright 2022 Tech4All</div>
        </div>
      </div>
    </div>
  )
}

export default Footer
