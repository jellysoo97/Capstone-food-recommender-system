import React, { useState } from "react"
import "../../../index.css"

function Table(props) {
  const user = props.user
  const unable = props.unable
  const datalist = props.datalist
  const getIngreGroup = props.getIngreGroup
  const getSelectedIngre = props.getSelectedIngre
  const [selected_ingre, setSelectedIngre] = useState([])

  const ingre_list = [
    "감자 및 전분류",
    "견과류",
    "곡류",
    "과실류",
    "난류",
    "당류",
    "두류",
    "버섯류",
    "어패류 및 수산물",
    "유제품류",
    "유지류",
    "육류",
    "음료류",
    "조리가공품류",
    "조미료류",
    "주류",
    "차류",
    "채소류",
    "해조류",
    "갑각류",
    "두족류",
    "수산가공품",
    "어류",
  ]

  const clickIngreGroup = (e) => {
    e.preventDefault()
    getIngreGroup(e.target.innerText)
  }

  const insertIngre = (e) => {
    e.preventDefault()
    setSelectedIngre(selected_ingre.concat(e.target.innerText))
    console.log("child:", selected_ingre)
    getSelectedIngre(selected_ingre)
  }

  return (
    <div className="container-fluid py-5">
      <div className="row text-center mb-2">
        <div className="col-12">
          <h3>
            <strong>{user}님, 냉장고 속 재료로 메뉴 추천받기</strong>
          </h3>
        </div>
      </div>
      <div className="row text-center mb-4">
        <div className="col-12">
          <h5>
            <strong>{unable}</strong>가 포함된 메뉴를 제외하고
            <br />
            <strong>영양성분이 우수한 순으로</strong> 추천됩니다.
          </h5>
        </div>
      </div>
      <div className="row mb-3">
        <div className="d-flex flex-row justify-content-center">
          <div className="sl-table-box">
            <table className="table table-hover">
              <tbody>
                {ingre_list
                  ? ingre_list.map((el, index) => (
                      <tr key={index} className="tableRowItems">
                        <td className="tableCell" onClick={clickIngreGroup}>
                          {el}
                        </td>
                      </tr>
                    ))
                  : ""}
              </tbody>
            </table>
          </div>
          <div className="sl-table-box">
            <table className="table table-hover">
              <tbody>
                {datalist
                  ? datalist.map((el, index) => (
                      <tr key={index} className="tableRowItems">
                        <td className="tableCell" onClick={insertIngre}>
                          {el["fields"]["ingre_group_1"]}
                        </td>
                      </tr>
                    ))
                  : ""}
              </tbody>
            </table>
          </div>
          <div className="sl-table-box">
            <table className="table table-hover">
              <tbody>
                {selected_ingre
                  ? selected_ingre.map((el, index) => (
                      <tr key={index} className="tableRowItems">
                        <td className="tableCell">{el}</td>
                      </tr>
                    ))
                  : ""}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-12 text-center">
          <button type="button" className="sl-table-btn" href={"#"}>
            해당 재료로 추천 받기
          </button>
        </div>
      </div>
    </div>
  )
}

export default Table
