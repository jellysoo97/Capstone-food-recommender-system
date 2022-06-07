import React, { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import axios from "axios"
import "../../../index.css"
import Table from "./Table"

function TableData(props) {
  const userId = props.userId
  const userIdx = props.userIdx
  const inedible = props.inedible
  const grouplist = props.grouplist
  const ingrelist = props.ingrelist
  const getSelectedGroupValue = props.getSelectedGroupValue

  const cell_group = document.getElementsByClassName("group")
  const cell_ingre = document.getElementsByClassName("ingre")
  const [selected_ingre, setSelectedIngre] = useState([])
  const [isChecked, setisChecked] = useState(false)
  const [checkedItems, setCheckedItems] = useState(new Set())
  let cate = useParams()

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
      selected_ingre.push(td.innerText)
      setSelectedIngre([...selected_ingre])
    } else if (!e.target.checked && checkedItems.has(el)) {
      checkedItems.delete(el)
      setCheckedItems(checkedItems)
      td.classList.add("inedible")
      selected_ingre.splice(selected_ingre.indexOf(e.target.innerText), 1)
      setSelectedIngre([...selected_ingre])
    }
    console.log(selected_ingre)
  }

  const insertIngre = (e) => {
    e.preventDefault()
    // selected_ingre 삭제 수정 필요
    if (e.target.classList.contains("clicked")) {
      e.target.classList.remove("clicked")
      selected_ingre.splice(selected_ingre.indexOf(e.target.innerText), 1)
      setSelectedIngre([...selected_ingre])
    } else {
      e.target.classList.add("clicked")
      selected_ingre.push(e.target.innerText)
      setSelectedIngre([...selected_ingre])
    }
    console.log(selected_ingre)
  }

  function sendSelectedIngre() {
    axios
      .post(
        `http://localhost:8000/selectIngre/bestcombi/${cate.cate}/${userIdx}`,
        {
          selected_ingre: [...selected_ingre],
        }
      )
      .then((response) => {
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  return (
    <div>
      <Table
        userId={userId}
        grouplist={grouplist}
        ingrelist={ingrelist}
        inedible={inedible}
        selected_ingre={selected_ingre}
        clickIngreGroup={clickIngreGroup}
        checkHandler={checkHandler}
        insertIngre={insertIngre}
        sendSelectedIngre={sendSelectedIngre}
      />
    </div>
  )
}

export default TableData
