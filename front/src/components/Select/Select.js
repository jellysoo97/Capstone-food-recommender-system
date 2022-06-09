import React, { useState, useEffect } from "react"
import axios from "axios"

import Table from "./Table/Table.js"

function Select() {
  const [userId, setUserId] = useState("")
  const [userIdx, setUserIdx] = useState()
  const [inedible, setInedible] = useState([])
  const [grouplist, setGrouplist] = useState([])
  const [ingrelist, setIngrelist] = useState([])
  const [selected_group_value, setSelectedGroupValue] = useState("")
  const [selected_ingre, setSelectedIngre] = useState([])
  let get_group_data = []
  let group_data_list = []
  let get_ingre_data = []
  let ingre_data_list = []

  const getSelectedGroupValue = (selected_group_value) => {
    setSelectedGroupValue(parseInt(selected_group_value))
  }

  const getSelectedIngre = (selected_ingre) => {
    setSelectedIngre(selected_ingre)
  }

  useEffect(() => {
    setUserId(window.localStorage.getItem("userId"))
    setUserIdx(window.localStorage.getItem("idx"))
    console.log(userId, userIdx)

    function getInedible() {
      axios
        .get(`http://localhost:8000/selectIngre/inedible/${userIdx}`)
        .then((response) => {
          setInedible([...response.data])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    userIdx !== undefined ? getInedible() : console.log("비로그인 상태")
  }, [userIdx])

  useEffect(() => {
    function getGroup() {
      axios
        .get("http://localhost:8000/selectIngre/group")
        .then((response) => {
          get_group_data = [...response.data]
          get_group_data.map((el) => {
            group_data_list.push(el.fields.group)
          })
          setGrouplist(group_data_list)
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getGroup()
  }, [])

  useEffect(() => {
    function getSub() {
      axios
        .get(`http://localhost:8000/selectIngre/group/${selected_group_value}`)
        .then((response) => {
          get_ingre_data = [...response.data]
          get_ingre_data.map((el) => {
            ingre_data_list.push(el.fields.sub_igrdt)
          })
          ingre_data_list[0] = ingre_data_list[0].replaceAll("'", '"')
          let list = JSON.parse("[" + ingre_data_list[0] + "]")
          setIngrelist(list[0])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    typeof selected_group_value == "number"
      ? getSub()
      : console.log("선택된 재료군 없음")
  }, [selected_group_value])

  return (
    <div>
      <Table
        userId={userId}
        userIdx={userIdx}
        inedible={inedible}
        grouplist={grouplist}
        getSelectedGroupValue={getSelectedGroupValue}
        ingrelist={ingrelist}
        getSelectedIngre={getSelectedIngre}
      />
    </div>
  )
}

export default Select
