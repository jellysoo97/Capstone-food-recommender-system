import React, { useState, useEffect } from "react"

const logoImg = require("../../images/logo.png")

function NavBar() {
  let userId = window.localStorage.getItem("userId")

  useEffect(() => {
    userId = window.localStorage.getItem("userId")
  }, [])
  // const [userId, setUserId] = useState()
  // useEffect(() => {
  //   setUserId(window.localStorage.getItem("userId"))
  //   console.log(typeof userId)
  // }, [userId])

  return (
    <div>
      <nav
        className="navbar navbar-expand-lg navbar-light px-5"
        style={{ background: "#A8BA88" }}
      >
        <div className="container-fluid">
          <a className="navbar-brand" href="/">
            <img
              src={logoImg}
              alt="로고"
              width="30"
              height="30"
              className="d-inline-block align-text-top"
            />
            <strong>나는 뭐 먹지</strong>
          </a>
          <ul className="navbar-nav mb-2 mb-lg-0 justify-content-center">
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <strong>메뉴 추천</strong>
              </a>
              <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                <li>
                  <a className="dropdown-item" href="/select">
                    영양소 균형순으로
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="/select">
                    선호도순으로
                  </a>
                </li>
              </ul>
            </li>
          </ul>
          {userId === null ? (
            <ul className="nav justify-content-end">
              <li className="nav-item">
                <a href={"/login"} className="btn btn-success">
                  로그인
                </a>
              </li>
            </ul>
          ) : (
            <ul className="nav justify-content-end">
              <li className="nav-item">{userId}님</li>
            </ul>
          )}
        </div>
      </nav>
    </div>
  )
}

export default NavBar
