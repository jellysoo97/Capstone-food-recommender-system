import React, { useEffect, useState } from "react"
import axios from "axios"
import "../../../index.css"

function Table(props) {
  const userId = props.userId
  const userIdx = props.userIdx
  const inedible = props.inedible
  const grouplist = props.grouplist
  const ingrelist = props.ingrelist
  const getSelectedGroupValue = props.getSelectedGroupValue
  const getSelectedIngre = props.getSelectedIngre

  const cell_group = document.getElementsByClassName("group")
  const cell_ingre = document.getElementsByClassName("ingre")
  const [selected_ingre, setSelectedIngre] = useState(new Set())
  const [isChecked, setisChecked] = useState(false)
  const [checkedItems, setCheckedItems] = useState(new Set())

  const clickIngreGroup = (e, index) => {
    e.preventDefault()
    getSelectedGroupValue(index)

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

  const checkHandler = (e, el, index) => {
    const td = document.getElementById(`td${index}`)
    setisChecked(!isChecked)
    if (e.target.checked) {
      checkedItems.add(el)
      setCheckedItems(checkedItems)
      td.classList.remove("inedible")
      selected_ingre.add(td.innerText)
      setSelectedIngre(selected_ingre)
    } else if (!e.target.checked && checkedItems.has(el)) {
      checkedItems.delete(el)
      setCheckedItems(checkedItems)
      td.classList.add("inedible")
      selected_ingre.delete(td.innerText)
      setSelectedIngre(selected_ingre)
    }
    console.log(checkedItems)
    console.log(selected_ingre)
  }

  const insertIngre = (e) => {
    // e.preventDefault()
    // selected_ingre 삭제 수정 필요
    if (e.target.classList.contains("clicked")) {
      e.target.classList.remove("clicked")
      selected_ingre.delete(e.target.innerText)
      setSelectedIngre(selected_ingre)
    } else {
      e.target.classList.add("clicked")
      selected_ingre.add(e.target.innerText)
      setSelectedIngre(selected_ingre)
    }
    console.log(selected_ingre)
  }

  function sendSelectedIngre() {
    // getSelectedIngre(selected_ingre)
    // console.log(selected_ingre)
    axios
      .post(`http://localhost:8000/selectIngre/bestcombi/${userIdx}`, {
        selected_ingre: [...selected_ingre],
      })
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  return (
    <div className="container-fluid py-5">
      <div className="row text-center mb-2">
        <div className="col-12">
          <h3>
            <strong>{userId}님, 냉장고 속 재료로 메뉴 추천받기</strong>
          </h3>
        </div>
      </div>
      <div className="row text-center mb-4">
        <div className="col-12">
          <h5>
            선택하신 식재료가 포함된 메뉴 중
            <br />
            <strong>영양소 균형 정도가 높은 순</strong>으로 추천됩니다.
            <br />*<strong>대체식품</strong>을 원하시면 체크해주세요.
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
                  ? ingrelist.map((el, index) => {
                      if (inedible.includes(el)) {
                        return (
                          <tr key={index} className="tableRowItems">
                            <td
                              className="tableCell ingre inedible"
                              id={`td${index}`}
                            >
                              {el}
                              <input
                                type="checkbox"
                                className="form-check-input mx-2"
                                onChange={(e) => checkHandler(e, el, index)}
                              ></input>
                            </td>
                          </tr>
                        )
                      } else {
                        return (
                          <tr key={index} className="tableRowItems">
                            <td
                              className="tableCell ingre"
                              onClick={insertIngre}
                            >
                              {el}
                            </td>
                          </tr>
                        )
                      }
                    })
                  : ""}
              </tbody>
            </table>
          </div>
          <div className="sl-table-box">
            <table className="table table-hover">
              <tbody>
                {selected_ingre
                  ? [...selected_ingre].map((el, index) => (
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
