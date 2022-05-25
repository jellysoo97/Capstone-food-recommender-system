import React, { useEffect, useState } from "react"
import axios from "axios"
import "../../../index.css"

function Table(props) {
  const unable = props.unable
  const grouplist = props.grouplist
  const ingrelist = props.ingrelist
  const getSelectedGroupValue = props.getSelectedGroupValue
  const getSelectedIngre = props.getSelectedIngre
  const cell_group = document.getElementsByClassName("group")
  const cell_ingre = document.getElementsByClassName("ingre")
  const [selected_ingre, setSelectedIngre] = useState([])
  let userIdx = window.localStorage.getItem("idx")
  let user = window.localStorage.getItem("userId")

  const clickIngreGroup = (e, index) => {
    e.preventDefault()
    getSelectedGroupValue(index)

    // 기존에 선택한 재료면 clicked된 상태로 만드는 수정 필요
    for (let i = 0; i < cell_ingre.length; i++) {
      cell_ingre[i].classList.value = "tableCell ingre"
    }
    if (e.target.classList.contains("clicked")) {
      e.target.classList.remove("clicked")
    } else {
      for (let i = 0; i < cell_group.length; i++) {
        cell_group[i].classList.value = "tableCell group"
      }
      e.target.classList.add("clicked")
    }
  }

  const insertIngre = (e) => {
    e.preventDefault()

    // selected_ingre 삭제 수정 필요
    if (e.target.classList.contains("clicked")) {
      e.target.classList.remove("clicked")
      selected_ingre.filter((el) => el !== e.target.innerText)
    } else {
      e.target.classList.add("clicked")
      selected_ingre.push(e.target.innerText)
    }
    console.log(selected_ingre)
  }

  function sendSelectedIngre() {
    // getSelectedIngre(selected_ingre)
    // console.log(selected_ingre)
    axios
      .post(`http://localhost:8000/selectIngre/bestcombi/${userIdx}`, {
        selected_ingre: selected_ingre,
      })
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  useEffect(() => {
    function changeValue() {
      setSelectedIngre(selected_ingre)
    }
    changeValue()
  }, [selected_ingre])

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
            <strong>땅콩, 복숭아</strong>가 포함된 메뉴를 제외하고
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
                {grouplist
                  ? grouplist.map((el, index) => (
                      <tr key={index} className="tableRowItems">
                        <td
                          className="tableCell group"
                          onClick={(e) => {
                            clickIngreGroup(e, index)
                          }}
                        >
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
                {ingrelist
                  ? ingrelist.map((el, index) => (
                      <tr key={index} className="tableRowItems">
                        <td className="tableCell ingre" onClick={insertIngre}>
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
          <button
            type="button"
            className="sl-table-btn"
            href={"#"}
            onClick={sendSelectedIngre}
          >
            해당 재료로 추천 받기
          </button>
        </div>
      </div>
    </div>
  )
}

export default Table
