import React, { useState, useEffect } from "react"
import axios from "axios"

import Table from "./Table/Table.js"

function Select() {
  const [grouplist, setGrouplist] = useState([])
  const [ingrelist, setIngrelist] = useState([])
  const [selected_group_value, setSelectedGroupValue] = useState("")
  let get_group_data = []
  let group_data_list = []
  let get_ingre_data = []
  let ingre_data_list = []

  const getSelectedGroupValue = (selected_group_value) => {
    setSelectedGroupValue(parseInt(selected_group_value))
  }

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
    getSub()
  }, [selected_group_value])

  return (
    <div>
      <Table
        grouplist={grouplist}
        getSelectedGroupValue={getSelectedGroupValue}
        ingrelist={ingrelist}
      />
    </div>
  )
}

export default Select
