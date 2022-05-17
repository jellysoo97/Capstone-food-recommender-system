import React, { useState, useEffect } from "react"
import axios from "axios"

import Table from "./Table/Table.js"

function Select() {
  const [datalist, setDatalist] = useState()
  const [selected_ingre_group, setSelectedIngreGroup] = useState("")
  const [selected_ingre, setSelectedIngre] = useState([])

  const getIngreGroup = (selected_ingre_group) => {
    setSelectedIngreGroup(selected_ingre_group)
    console.log(selected_ingre_group)
  }

  const getSelectedIngre = (selected_ingre) => {
    setSelectedIngre(selected_ingre)
    console.log("parent:", selected_ingre)
  }

  useEffect(() => {
    function getData() {
      axios
        .get(`http://localhost:8000/recommend/select/${selected_ingre_group}`)
        .then((response) => {
          // console.log(response.data)
          setDatalist([...response.data])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getData()
  }, [selected_ingre_group])

  return (
    <div>
      <Table
        datalist={datalist}
        selected_ingre_group={selected_ingre_group}
        getIngreGroup={getIngreGroup}
        selected_ingre={selected_ingre}
        getSelectedIngre={getSelectedIngre}
      />
    </div>
  )
}

export default Select
