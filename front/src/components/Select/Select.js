import React, { useState, useEffect } from "react"
import axios from "axios"

import TableData from "./Table/TableData.js"

function Select() {
  const [userId, setUserId] = useState("")
  const [userIdx, setUserIdx] = useState()
  const [inedible, setInedible] = useState([])
  const [grouplist, setGrouplist] = useState([])
  const [ingrelist, setIngrelist] = useState([])
  const [selected_group_value, setSelectedGroupValue] = useState("")
  let get_group_data = []
  let group_data_list = []
  let get_ingre_data = []
  let ingre_data_list = []

  // 유저의 못먹는 재료 리스트 불러오기
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

  // 재료군 불러오기
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

  // 선택된 재료군 idx 불러오기
  const getSelectedGroupValue = (selected_group_value) => {
    setSelectedGroupValue(parseInt(selected_group_value) + 1)
  }

  // 선택된 재료군에 속한 재료들 불러오기
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
      <TableData
        userId={userId}
        userIdx={userIdx}
        inedible={inedible}
        grouplist={grouplist}
        getSelectedGroupValue={getSelectedGroupValue}
        ingrelist={ingrelist}
      />
    </div>
  )
}

export default Select
