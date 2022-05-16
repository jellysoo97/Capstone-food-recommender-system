import React, { useState } from "react"
import "../../../index.css"

function Table(props) {
  const user = props.user
  const unable = props.unable
  const group = props.group
  const [click, setClick] = useState(false)
  const [clickbox, setClickbox] = useState("")

  const handleClick = (e) => {
    click ? setClick(false) : setClick(true)
    console.log(click)
    click
      ? (e.target.className = "tableRowItems sl-clicked")
      : (e.target.className = "tableRowItems")
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
                {group
                  ? group.map((el, index) => (
                      <tr
                        className="tableRowItems"
                        key={index}
                        onClick={handleClick}
                      >
                        <td className="tableCell">{el}</td>
                      </tr>
                    ))
                  : ""}
              </tbody>
            </table>
          </div>
          <div className="sl-table-box">
            <table className="table table-hover">
              <tbody>
                {/* {datalist\
                  ? datalist.map((el, index) => (
                      <tr key={index} className="tableRowItems">
                        <td className="tableCell">{el.id}</td>
                      </tr>
                    ))
                  : ""} */}
              </tbody>
            </table>
          </div>
          <div className="sl-table-box">3</div>
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
