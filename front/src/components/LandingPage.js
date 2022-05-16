import React from "react"
import "../index.css"

const cardImg1 = require("../images/card_nutrient.png")
const cardImg2 = require("../images/card_vegi.png")
const cardImg3 = require("../images/card_recipe.png")

function LandingPage() {
  const CardRow = () => {
    const Row = ({ src, alt, title, desc1, desc2, desc3 }) => {
      return (
        <div className="col-4 lp-card-box text-center">
          <div className="lp-card-img">
            <img src={src} alt={alt} width={"100%"} height={"100%"} />
          </div>
          <div className="lp-card-body">
            <p className="lp-card-title">{title}</p>
            <div className="card-text">{desc1}</div>
            <div className="card-text">{desc2}</div>
            <div className="card-text">{desc3}</div>
          </div>
        </div>
      )
    }
    return (
      <>
        <div className="row text-center lp-card-top">
          <div>영양성분, 남은 재료, 사용자의 성향까지 고려한 맞춤형 레시피</div>
        </div>
        <div className="row text-center lp-card-bottom">
          <Row
            src={cardImg1}
            alt={"영양성분"}
            title={"영양소 균형잡힌 메뉴 추천"}
            desc1={"- 입력한 재료로 조리가능한 메뉴 선별"}
            desc2={"- 영양성분을 고려하여"}
            desc3={"가장 영양가 있는 메뉴 추천"}
          />
          <Row
            src={cardImg2}
            alt={"알레르기"}
            title={"사용자 성향을 고려한 메뉴 추천"}
            desc1={"- 비슷한 성향의 사용자들이"}
            desc2={"선호하는 메뉴 추천"}
            desc3={""}
          />
          <Row
            src={cardImg3}
            alt={"레시피"}
            title={"전메뉴 레시피 및 영양성분 제공"}
            desc1={"- 추천받은 메뉴에 대한"}
            desc2={"레시피 및 영양성분 제공"}
            desc3={""}
          />
        </div>
      </>
    )
  }
  return (
    <div className="container-fluid p-0">
      <div className="container-fluid lp-bg d-flex align-items-center justify-content-center">
        <div className="d-inline-block">
          <div className="row text-center">
            <div className="col-12">
              <div className="lp-title">나는 뭐 먹지</div>
            </div>
          </div>
          <div className="row text-center">
            <div className="col-12">
              <div className="lp-desc">
                개인 맞춤형 메뉴 추천 서비스
                <br />
                비건, 알레르기 등 사용자 성향을 고려한 메뉴를 추천받고 싶다면?
              </div>
            </div>
          </div>
          <div className="row text-center">
            <div className="col-12">
              <a href="#">
                <button type="button" className="lp-regi">
                  회원가입
                </button>
              </a>
            </div>
          </div>
        </div>
      </div>
      <div className="container-fluid lp-card">
        <div>
          <CardRow />
        </div>
      </div>
      <div
        className="container-fluid d-flex align-items-center justify-content-center"
        style={{ height: "calc(30vh)", background: "#A8BA88" }}
      >
        <div className="d-inline-block" style={{ width: "calc(100vw)" }}>
          <div className="row text-center">
            <div className="col lp-third">
              총 레시피 수<br />
              1,000
            </div>
            <div className="col lp-third">
              총 사용자 수<br />
              100
            </div>
            <div className="col lp-third">
              총 선호도 평가 수<br />
              200
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
