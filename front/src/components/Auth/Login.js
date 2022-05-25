import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"

function Login() {
  const url = "http://127.0.0.1:8000/user/login"
  const [logindata, setlogindata] = useState({
    user_id: "",
    password: "",
  })
  const navigate = useNavigate()

  function handle(e) {
    const newlogindata = { ...logindata }
    newlogindata[e.target.id] = e.target.value
    setlogindata(newlogindata)
  }

  function submit(e) {
    e.preventDefault()
    axios
      .post(url, {
        user_id: logindata.user_id,
        password: logindata.password,
      })
      .then((res) => {
        console.log(res.data)
        navigate("/")
        window.localStorage.setItem("idx", res.data.idx)
        window.localStorage.setItem("userId", res.data.userId)
      })
  }

  return (
    <div className="container-fluid d-flex lg-bg">
      <div className="lg-box">
        <div className="lg-title text-center mb-5">로그인</div>
        <div className="lg-form">
          <form onSubmit={(e) => submit(e)} className="needs-validation">
            <div className="row mb-4 text-center justify-content-center">
              <label for="inputId" className="col-2 col-form-label">
                아이디
              </label>
              <div className="col-8">
                <input
                  onChange={(e) => handle(e)}
                  value={logindata.user_id}
                  type="text"
                  className="form-control"
                  id="user_id"
                  required
                />
              </div>
              <div className="row">
                <div className="col-12">
                  <div className="invalid-feedback">아이디를 입력해주세요.</div>
                </div>
              </div>
            </div>
            <div className="row mb-5 text-center justify-content-center">
              <label for="inputPassword" className="col-2 col-form-label">
                비밀번호
              </label>
              <div className="col-8">
                <input
                  onChange={(e) => handle(e)}
                  value={logindata.password}
                  type="password"
                  className="form-control"
                  id="password"
                  required
                />
              </div>
              <div className="invalid-feedback">비밀번호를 입력해주세요.</div>
            </div>
            <div className="row text-center">
              <div className="col-12">
                <button className="lg-btn">로그인</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login
