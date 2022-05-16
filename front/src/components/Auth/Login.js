import React from "react"

function Login() {
  return (
    <div className="container-fluid d-flex lg-bg">
      <div className="lg-box">
        <div className="lg-title text-center mb-5">로그인</div>
        <div className="lg-form">
          <form className="needs-validation">
            <div className="row mb-4 text-center justify-content-center">
              <label for="inputId" className="col-2 col-form-label">
                아이디
              </label>
              <div className="col-8">
                <input
                  type="text"
                  className="form-control"
                  id="inputId"
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
                  type="password"
                  className="form-control"
                  id="inputPassword"
                  required
                />
              </div>
              <div className="invalid-feedback">비밀번호를 입력해주세요.</div>
            </div>
            <div className="row text-center">
              <div className="col-12">
                <button type="submit" className="lg-btn">
                  로그인
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login
